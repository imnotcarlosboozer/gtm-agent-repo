#!/usr/bin/env python3
"""
Quarterly Pipeline Report with Account Context

Generates a comprehensive quarterly pipeline report including:
- Pipeline opportunities table (filtered by rep and quarter)
- Gong call transcripts for each account (filtered to quarter dates)
- Existing research reports (if previously saved)

Usage:
    python quarterly_pipeline_context.py --rep "Vishwa" --quarter "Q1 2026" --fiscal
    python quarterly_pipeline_context.py --rep "vishwa.srinivasan@astronomer.io" --quarter "Q1"
"""

import json
import argparse
import subprocess
import shutil
import os
import time
from datetime import datetime, date
from collections import defaultdict
from pathlib import Path
from typing import Optional, Tuple, List, Dict
from base64 import b64encode

import requests


# Rep name to email mapping
REP_EMAIL_MAP = {
    "vishwa": "vishwa.srinivasan@astronomer.io",
    "vishwa srinivasan": "vishwa.srinivasan@astronomer.io",
}


def parse_rep_name(name: str) -> str:
    """Map rep name to email, allow direct email input."""
    name_lower = name.lower().strip()

    if "@" in name:
        return name  # Already an email

    if name_lower in REP_EMAIL_MAP:
        return REP_EMAIL_MAP[name_lower]

    raise ValueError(f"Unknown rep name: {name}. Add to REP_EMAIL_MAP or provide email directly.")


def parse_quarter_input(quarter_str: str) -> Tuple[int, int]:
    """Parse 'Q1 2026', 'Q1', 'Q1 FY2026' to (quarter_num, year)."""
    quarter_str = quarter_str.strip().upper()

    # Remove 'FY' prefix if present
    quarter_str = quarter_str.replace("FY", "").strip()

    # Split into parts
    parts = quarter_str.split()

    # Extract quarter number
    quarter_num = None
    year = None

    for part in parts:
        if part.startswith("Q"):
            try:
                quarter_num = int(part[1:])
            except ValueError:
                pass
        else:
            try:
                year = int(part)
            except ValueError:
                pass

    if quarter_num is None or quarter_num not in [1, 2, 3, 4]:
        raise ValueError(f"Invalid quarter format: {quarter_str}. Use 'Q1 2026', 'Q1', etc.")

    # Default to current fiscal year if not specified
    if year is None:
        year = 2026

    return quarter_num, year


def parse_closedate(closedate_array):
    """Parse Salesforce CloseDate array [year, month, day] to date object."""
    if not closedate_array or len(closedate_array) != 3:
        return None
    try:
        return date(closedate_array[0], closedate_array[1], closedate_array[2])
    except (ValueError, TypeError):
        return None


def is_in_quarter(close_date, year, quarter, fiscal=False):
    """Check if a date falls within the specified quarter."""
    if not close_date:
        return False

    if fiscal:
        quarter_months = {
            1: (2, 4),
            2: (5, 7),
            3: (8, 10),
            4: (11, 1)
        }

        start_month, end_month = quarter_months[quarter]

        if quarter == 4:
            return ((close_date.year == year and close_date.month >= 11) or
                    (close_date.year == year + 1 and close_date.month == 1))
        else:
            return (close_date.year == year and
                    start_month <= close_date.month <= end_month)
    else:
        quarter_months = {
            1: (1, 3),
            2: (4, 6),
            3: (7, 9),
            4: (10, 12)
        }

        start_month, end_month = quarter_months[quarter]
        return (close_date.year == year and
                start_month <= close_date.month <= end_month)


def get_quarter_date_range(quarter: int, year: int, fiscal: bool = True) -> Tuple[date, date]:
    """Get the start and end date for a quarter."""
    if fiscal:
        fiscal_start_months = {1: 2, 2: 5, 3: 8, 4: 11}
        fiscal_end_months = {1: 4, 2: 7, 3: 10, 4: 1}
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        start_month = fiscal_start_months[quarter]
        end_month = fiscal_end_months[quarter]

        quarter_start = date(year, start_month, 1)

        if quarter == 4:
            quarter_end = date(year + 1, 1, 31)
        else:
            quarter_end = date(year, end_month, days_in_month[end_month - 1])
    else:
        quarter_start = date(year, (quarter - 1) * 3 + 1, 1)
        quarter_end_month = quarter * 3
        quarter_end = date(year, quarter_end_month,
                           [31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][quarter_end_month - 1])

    return quarter_start, quarter_end


def extract_opportunities(calls_data, rep_email, year, quarter, fiscal=False):
    """Extract opportunities from calls where the rep participated."""
    opportunities = {}

    for call in calls_data:
        parties = call.get('parties', [])
        rep_participated = any(
            party.get('emailAddress') == rep_email
            for party in parties
        )

        if not rep_participated:
            continue

        context = call.get('context', [])
        if not context:
            continue

        accounts = {}
        call_opportunities = []

        for ctx in context:
            if not isinstance(ctx, dict):
                continue

            objects = ctx.get('objects', [])
            for obj in objects:
                obj_type = obj.get('objectType')
                obj_id = obj.get('objectId')

                if not obj_type or not obj_id:
                    continue

                fields_dict = {}
                for field in obj.get('fields', []):
                    fields_dict[field['name']] = field['value']

                if obj_type == 'Account':
                    account_name = fields_dict.get('Name')
                    if account_name:
                        accounts[obj_id] = account_name

                elif obj_type == 'Opportunity':
                    closedate_value = fields_dict.get('CloseDate')
                    close_date = parse_closedate(closedate_value)

                    if not is_in_quarter(close_date, year, quarter, fiscal):
                        continue

                    opp_data = {
                        'id': obj_id,
                        'name': fields_dict.get('Name', 'Unknown'),
                        'close_date': close_date,
                        'stage': fields_dict.get('StageName'),
                        'amount': fields_dict.get('Amount'),
                        'probability': fields_dict.get('Probability'),
                        'type': fields_dict.get('Type'),
                        'account_id': fields_dict.get('AccountId')
                    }

                    call_opportunities.append(opp_data)

        for opp_data in call_opportunities:
            opp_id = opp_data['id']

            if opp_data.get('account_id') and opp_data['account_id'] in accounts:
                opp_data['account_name'] = accounts[opp_data['account_id']]

            if opp_id not in opportunities:
                opportunities[opp_id] = opp_data
            elif not opportunities[opp_id].get('account_name') and opp_data.get('account_name'):
                opportunities[opp_id] = opp_data

    return opportunities


def generate_pipeline_report(opportunities, rep_email, year, quarter, output_path, fiscal=False):
    """Generate markdown report from opportunities data."""
    sorted_opps = sorted(
        opportunities.values(),
        key=lambda x: x['close_date'] if x['close_date'] else date.max
    )

    stage_stats = defaultdict(lambda: {'count': 0, 'amount': 0})
    total_amount = 0

    for opp in sorted_opps:
        stage = opp['stage'] or 'Unknown'
        amount = opp['amount'] or 0

        stage_stats[stage]['count'] += 1
        stage_stats[stage]['amount'] += amount
        total_amount += amount

    quarter_start, quarter_end = get_quarter_date_range(quarter, year, fiscal)

    lines = [
        f"# Q{quarter} {year} Pipeline Report",
        f"",
        f"**Rep:** {rep_email}",
        f"**Date Range:** {quarter_start} to {quarter_end}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"## Summary",
        f"",
        f"**Total Opportunities:** {len(opportunities)}",
        f"**Total Pipeline Value:** ${total_amount:,.0f}",
        f"",
        f"### By Stage",
        f""
    ]

    for stage, stats in sorted(stage_stats.items(),
                               key=lambda x: x[1]['amount'],
                               reverse=True):
        lines.append(f"- **{stage}:** {stats['count']} deals, ${stats['amount']:,.0f}")

    lines.extend([
        f"",
        f"## Opportunities",
        f"",
        f"| Account | Opportunity | Close Date | Stage | Amount | Probability | Type | SF ID |",
        f"|---------|-------------|------------|-------|--------|-------------|------|-------|"
    ])

    for opp in sorted_opps:
        account = opp.get('account_name', 'Unknown')
        name = opp['name']
        close_date = opp['close_date'].strftime('%Y-%m-%d') if opp['close_date'] else 'N/A'
        stage = opp['stage'] or 'N/A'
        amount = f"${opp['amount']:,.0f}" if opp['amount'] else 'N/A'
        probability = f"{opp['probability']}%" if opp['probability'] is not None else 'N/A'
        opp_type = opp['type'] or 'N/A'
        opp_id = opp['id']

        lines.append(f"| {account} | {name} | {close_date} | {stage} | {amount} | {probability} | {opp_type} | {opp_id} |")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('\n'.join(lines))

    return output_file, len(opportunities), total_amount, stage_stats


def extract_unique_accounts(opportunities: dict) -> List[Dict[str, str]]:
    """Get unique account names and IDs from opportunities.

    Also updates the opportunities dict with parsed account names.
    """
    accounts = {}

    for opp_id, opp in opportunities.items():
        account_id = opp.get('account_id')
        account_name = opp.get('account_name', 'Unknown')

        # If account_name is Unknown, try to parse from opportunity name
        if account_name == 'Unknown':
            opp_name = opp.get('name', '')
            # Most opportunity names follow pattern: "Account Name - S1" or "Account Name - Renewal..."
            if ' - ' in opp_name:
                account_name = opp_name.split(' - ')[0].strip()
                # Update the opportunity with the parsed account name
                opp['account_name'] = account_name

        if account_name and account_name != 'Unknown':
            # Use account_id as key if available, otherwise use account_name
            key = account_id if account_id else account_name
            accounts[key] = account_name

    return [{"id": aid, "name": name} for aid, name in accounts.items()]


# --- Gong API Configuration ---
ACCESS_KEY = os.environ.get("GONG_ACCESS_KEY", "")
SECRET_KEY = os.environ.get("GONG_SECRET_KEY", "")
BASE_URL = "https://api.gong.io/v2"
RATE_LIMIT_DELAY = 0.35

if ACCESS_KEY and SECRET_KEY:
    auth_string = b64encode(f"{ACCESS_KEY}:{SECRET_KEY}".encode()).decode()
    GONG_HEADERS = {
        "Authorization": f"Basic {auth_string}",
        "Content-Type": "application/json",
    }
else:
    GONG_HEADERS = None


def account_slug(name: str) -> str:
    """Convert account name to filesystem-safe slug."""
    return name.lower().replace(" ", "_").replace(".", "").replace(",", "").replace("/", "_")


def get_crm_account_name(call: dict) -> Optional[str]:
    """Extract CRM account name from call context."""
    for ctx in call.get("context", []):
        for obj in ctx.get("objects", []):
            if obj.get("objectType") == "Account":
                for field in obj.get("fields", []):
                    if field.get("name") == "Name":
                        return field.get("value")
    return None


def filter_calls_by_account_and_date(calls_data: list, account_name: str, from_date: date, to_date: date) -> list:
    """Filter calls by account name and date range."""
    matched = []
    account_lower = account_name.lower()
    from_iso = f"{from_date.isoformat()}T00:00:00Z"
    to_iso = f"{to_date.isoformat()}T23:59:59Z"

    for call in calls_data:
        # Check date range
        call_date = call.get("metaData", {}).get("started", "")
        if not (from_iso <= call_date <= to_iso):
            continue

        # Check if account matches
        crm_name = get_crm_account_name(call)
        if crm_name and account_lower in crm_name.lower():
            matched.append(call)
            continue

        # Also check call title
        title = (call.get("metaData", {}).get("title") or "").lower()
        if account_lower in title:
            matched.append(call)

    return matched


def load_cached_transcripts(cache_dir: Path, slug: str) -> Optional[dict]:
    """Load cached transcripts for an account."""
    acct_dir = cache_dir / "accounts" / slug
    trans_path = acct_dir / "transcripts.json"

    if trans_path.exists():
        with open(trans_path) as f:
            return json.load(f)
    return None


def save_cached_transcripts(cache_dir: Path, slug: str, account_name: str, call_ids: list, transcripts: list):
    """Save transcripts to cache."""
    acct_dir = cache_dir / "accounts" / slug
    acct_dir.mkdir(parents=True, exist_ok=True)

    metadata = {
        "account_name": account_name,
        "last_fetched": datetime.now().isoformat(),
        "call_count": len(call_ids),
        "call_ids": call_ids,
    }

    with open(acct_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    with open(acct_dir / "transcripts.json", "w") as f:
        json.dump(transcripts, f, default=str)


def fetch_transcripts_from_api(call_ids: list) -> list:
    """Fetch transcripts from Gong API."""
    if not GONG_HEADERS:
        return []

    all_transcripts = []
    batch_size = 20

    for i in range(0, len(call_ids), batch_size):
        batch = call_ids[i : i + batch_size]
        try:
            time.sleep(RATE_LIMIT_DELAY)
            resp = requests.post(
                f"{BASE_URL}/calls/transcript",
                headers=GONG_HEADERS,
                json={"filter": {"callIds": batch}},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            all_transcripts.extend(data.get("callTranscripts", []))
        except Exception as e:
            print(f"    ⚠️ Error fetching transcript batch: {str(e)[:80]}")
            continue

    return all_transcripts


def build_speaker_map(calls: list) -> dict:
    """Build map of speaker IDs to speaker info."""
    speaker_map = {}
    for call in calls:
        for party in call.get("parties", []):
            sid = party.get("speakerId")
            if sid:
                speaker_map[sid] = {
                    "name": party.get("name", "Unknown"),
                    "email": party.get("emailAddress", ""),
                    "title": party.get("title", ""),
                    "affiliation": party.get("affiliation", ""),
                }
    return speaker_map


def format_transcript(transcript: dict, speaker_map: dict) -> str:
    """Format transcript as readable text."""
    lines = []
    for segment in transcript.get("transcript", []):
        speaker_id = segment.get("speakerId")
        speaker_info = speaker_map.get(speaker_id, {})
        speaker_name = speaker_info.get("name", f"Speaker {speaker_id}")
        topic = segment.get("topic")

        if topic:
            lines.append(f"\n--- {topic} ---\n")

        for sentence in segment.get("sentences", []):
            lines.append(f"[{speaker_name}]: {sentence.get('text', '')}")

    return "\n".join(lines)


def format_account_markdown(account_name: str, calls: list, transcripts: list, speaker_map: dict) -> str:
    """Format account transcripts as markdown."""
    lines = [
        f"# Gong Transcripts: {account_name}\n",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Total Calls**: {len(calls)}\n",
        "---\n"
    ]

    # Sort calls by date
    sorted_calls = sorted(calls, key=lambda c: c.get("metaData", {}).get("started", ""))

    for call in sorted_calls:
        meta = call.get("metaData", {})
        call_id = meta.get("id")
        transcript = next((t for t in transcripts if t.get("callId") == call_id), None)

        lines.append(f"## {meta.get('title', 'Untitled')}\n")
        lines.append(f"**Date**: {(meta.get('started') or '')[:16]}")

        dur = meta.get("duration")
        if dur:
            lines.append(f"**Duration**: {dur // 60}m {dur % 60}s")

        lines.append(f"**Gong URL**: {meta.get('url', 'N/A')}\n")

        # External participants
        ext = [p for p in call.get("parties", []) if (p.get("affiliation") or "").lower() == "external"]
        if ext:
            lines.append("**External Participants**:")
            for p in ext:
                name = p.get("name") or "Unknown"
                title = f" ({p['title']})" if p.get("title") else ""
                lines.append(f"- {name}{title}")
            lines.append("")

        # Internal participants
        internal = [p for p in call.get("parties", []) if (p.get("affiliation") or "").lower() == "internal"]
        if internal:
            lines.append("**Internal Participants**:")
            for p in internal:
                name = p.get("name") or "Unknown"
                title = f" ({p['title']})" if p.get("title") else ""
                lines.append(f"- {name}{title}")
            lines.append("")

        lines.append("### Transcript\n")
        if transcript:
            lines.append(format_transcript(transcript, speaker_map))
        else:
            lines.append("*No transcript available*")

        lines.append("\n---\n")

    return "\n".join(lines)


def fetch_account_transcripts(account_name: str, from_date: date, to_date: date,
                              calls_data: list, cache_dir: Path, skip_transcripts: bool = False) -> Optional[str]:
    """Fetch or retrieve cached transcripts for an account."""
    if skip_transcripts:
        return None

    # Filter calls for this account and date range
    account_calls = filter_calls_by_account_and_date(calls_data, account_name, from_date, to_date)

    if not account_calls:
        return None

    call_ids = [c.get("metaData", {}).get("id") for c in account_calls if c.get("metaData", {}).get("id")]
    if not call_ids:
        return None

    # Check cache
    slug = account_slug(account_name)
    cached_transcripts = load_cached_transcripts(cache_dir, slug)

    transcripts = []
    if cached_transcripts:
        # Use cached transcripts, but fetch any missing ones
        cached_ids = {t.get("callId") for t in cached_transcripts}
        missing_ids = [cid for cid in call_ids if cid not in cached_ids]

        if missing_ids:
            new_transcripts = fetch_transcripts_from_api(missing_ids)
            transcripts = cached_transcripts + new_transcripts
            save_cached_transcripts(cache_dir, slug, account_name, call_ids, transcripts)
        else:
            transcripts = cached_transcripts
    else:
        # Fetch all transcripts
        transcripts = fetch_transcripts_from_api(call_ids)
        if transcripts:
            save_cached_transcripts(cache_dir, slug, account_name, call_ids, transcripts)

    if not transcripts:
        return None

    # Build speaker map and format output
    speaker_map = build_speaker_map(account_calls)
    markdown = format_account_markdown(account_name, account_calls, transcripts, speaker_map)

    return markdown


def find_existing_research(account_name: str) -> Optional[Path]:
    """Look for existing research files in ~/Account Context/[account_name]/."""
    account_folder = Path.home() / "Account Context" / account_name

    if not account_folder.exists():
        return None

    patterns = ["*Research*.md", "*Exa*.md", "*Comprehensive*.md", "*research*.md"]
    research_files = []

    for pattern in patterns:
        research_files.extend(account_folder.glob(pattern))

    if research_files:
        return max(research_files, key=lambda p: p.stat().st_mtime)

    return None


def organize_outputs(quarter: int, year: int, opportunities: dict, rep_email: str,
                     output_base: str, fiscal: bool, calls_data: list, skip_transcripts: bool = False):
    """Create quarterly folder structure and populate with content."""
    quarter_folder = Path(output_base) / f"Q{quarter}_{year}_Pipeline"
    accounts_folder = quarter_folder / "Accounts"
    accounts_folder.mkdir(parents=True, exist_ok=True)

    # Process each unique account (also updates opportunities dict with parsed account names)
    accounts = extract_unique_accounts(opportunities)

    # Generate main pipeline report (after account names are parsed)
    main_report_path = quarter_folder / f"Q{quarter}_{year}_Pipeline_Report.md"
    generate_pipeline_report(opportunities, rep_email, year, quarter, main_report_path, fiscal)

    # Calculate quarter date range
    from_date, to_date = get_quarter_date_range(quarter, year, fiscal=fiscal)
    results = {
        "transcripts": 0,
        "research": 0,
        "skipped": [],
        "transcript_call_counts": {}
    }

    print(f"\nProcessing {len(accounts)} unique accounts...")

    for i, account in enumerate(accounts, 1):
        account_name = account["name"]

        if not account_name or account_name == "Unknown":
            results["skipped"].append(account_name)
            continue

        print(f"  [{i}/{len(accounts)}] {account_name}...")

        # Create account folder
        account_slug = account_name.replace(" ", "_").replace("/", "_").replace(".", "")
        account_folder = accounts_folder / account_slug
        account_folder.mkdir(exist_ok=True)

        # Fetch Gong transcripts
        if not skip_transcripts:
            cache_dir = Path.home() / "claude-work" / "gong-cache"
            transcripts = fetch_account_transcripts(account_name, from_date, to_date, calls_data, cache_dir, skip_transcripts)
            if transcripts:
                transcript_file = account_folder / "gong_transcripts.md"
                transcript_file.write_text(transcripts)
                results["transcripts"] += 1

                # Count calls in transcript
                call_count = transcripts.count("## ") - 1  # Subtract header
                if call_count > 0:
                    results["transcript_call_counts"][account_name] = call_count
                    print(f"    ✓ Fetched {call_count} calls")

        # Copy existing research if available
        research_file = find_existing_research(account_name)
        if research_file:
            dest_file = account_folder / research_file.name
            shutil.copy(research_file, dest_file)
            results["research"] += 1
            print(f"    ✓ Copied research: {research_file.name}")

    return quarter_folder, results


def main():
    parser = argparse.ArgumentParser(
        description='Generate quarterly pipeline report with account context'
    )
    parser.add_argument('--rep', required=True, help='Rep name or email')
    parser.add_argument('--quarter', required=True, help='Quarter string (e.g., "Q1 2026", "Q1")')
    parser.add_argument('--output-base', default=str(Path.home() / "Account Context"),
                        help='Base output directory')
    parser.add_argument('--fiscal', action='store_true', default=True,
                        help='Use fiscal quarters (Feb=Q1 start)')
    parser.add_argument('--calendar', action='store_true',
                        help='Use calendar quarters instead')
    parser.add_argument('--input',
                        default=str(Path.home() / "claude-work/gong-cache/all_calls/calls.json"),
                        help='Path to cached Gong calls JSON file')
    parser.add_argument('--skip-transcripts', action='store_true',
                        help='Skip fetching Gong transcripts (only create pipeline report and copy existing research)')

    args = parser.parse_args()

    # Parse inputs
    print("Parsing inputs...")
    rep_email = parse_rep_name(args.rep)
    quarter, year = parse_quarter_input(args.quarter)
    fiscal = args.fiscal and not args.calendar

    print(f"  Rep: {rep_email}")
    print(f"  Quarter: Q{quarter} {year} ({'Fiscal' if fiscal else 'Calendar'})")

    # Load global Gong cache
    cache_path = Path(args.input)
    if not cache_path.exists():
        print(f"\nError: Gong cache not found at {cache_path}")
        print("Run the following to sync cache first:")
        print(f"  python3 {Path.home()}/claude-work/gong_account_transcripts.py --sync")
        return 1

    print(f"\nLoading cached Gong data from {cache_path}...")
    with open(cache_path) as f:
        calls_data = json.load(f)
    print(f"  Found {len(calls_data)} calls")

    # Extract opportunities
    print(f"\nExtracting Q{quarter} {year} opportunities for {rep_email}...")
    opportunities = extract_opportunities(calls_data, rep_email, year, quarter, fiscal)

    if not opportunities:
        print(f"\n⚠️  No opportunities found for Q{quarter} {year}")
        return 0

    print(f"  Found {len(opportunities)} unique opportunities")

    # Organize outputs
    print(f"\nGenerating quarterly pipeline report...")
    quarter_folder, results = organize_outputs(
        quarter, year, opportunities, rep_email, args.output_base, fiscal, calls_data, args.skip_transcripts
    )

    # Print summary
    total_amount = sum(opp.get('amount', 0) or 0 for opp in opportunities.values())

    print(f"\n{'='*60}")
    print(f"✓ Q{quarter} {year} Pipeline Report Generated for {rep_email.split('@')[0].title()}")
    print(f"{'='*60}")
    print(f"\n📊 Pipeline Summary:")
    print(f"  • Total Opportunities: {len(opportunities)}")
    print(f"  • Total Pipeline Value: ${total_amount:,.0f}")

    print(f"\n📁 Location: {quarter_folder}")

    print(f"\n📋 Account Context Generated:")
    if args.skip_transcripts:
        print(f"  • Gong transcripts: SKIPPED (--skip-transcripts flag)")
    else:
        print(f"  • {results['transcripts']} accounts with Gong transcripts")
    print(f"  • {results['research']} accounts with existing research (copied)")

    if results['skipped']:
        print(f"  • Skipped: {len(results['skipped'])} accounts (no account name in Salesforce)")

    # Show top accounts with most calls
    if results['transcript_call_counts']:
        print(f"\n🔥 Top Accounts by Call Volume:")
        sorted_accounts = sorted(
            results['transcript_call_counts'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for account, count in sorted_accounts:
            research_indicator = "📄" if find_existing_research(account) else "  "
            print(f"  {research_indicator} {account}: {count} calls")

    return 0


if __name__ == '__main__':
    exit(main())
