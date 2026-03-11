#!/usr/bin/env python3
"""
Gong JSON to Markdown Converter for QMD Integration

Converts cached Gong transcript JSON files to markdown format for QMD semantic search.

Two-tier cache architecture:
1. JSON (source of truth): ~/claude-work/gong-cache/accounts/{slug}/transcripts.json
2. Markdown (QMD index): ~/claude-work/gong-cache/accounts/{slug}/transcripts.md

Usage:
    python gong_json_to_markdown.py --account "Chalice"
    python gong_json_to_markdown.py --all
    python gong_json_to_markdown.py --sync  # Update stale MD files
    python gong_json_to_markdown.py --all --force
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List


# --- Config ---
CACHE_DIR = Path(os.path.expanduser("~/claude-work/gong-cache"))
ACCOUNTS_DIR = CACHE_DIR / "accounts"


def slugify(name: str) -> str:
    """Convert account name to slug (lowercase, spaces → underscores, remove special chars)."""
    slug = re.sub(r'[^a-z0-9_]', '', name.lower().replace(' ', '_').replace('-', '_'))
    return slug or "unknown"


def load_json(path: Path) -> Optional[dict]:
    """Load JSON file if it exists."""
    if not path.exists():
        return None
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}", file=sys.stderr)
        return None


def save_json(path: Path, data: dict):
    """Save JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def is_markdown_stale(account_dir: Path) -> bool:
    """Check if markdown needs regeneration based on metadata timestamps."""
    metadata_path = account_dir / "metadata.json"
    markdown_path = account_dir / "transcripts.md"

    if not markdown_path.exists():
        return True

    metadata = load_json(metadata_path)
    if not metadata:
        return True

    # Check if JSON was updated after markdown generation
    json_updated = metadata.get("last_fetched")
    md_generated = metadata.get("markdown_generated")

    if not md_generated:
        return True

    # Also check call count mismatch
    json_call_count = metadata.get("call_count", 0)
    md_call_count = metadata.get("markdown_call_count", 0)

    if json_call_count != md_call_count:
        return True

    return json_updated and json_updated > md_generated


def format_duration(seconds: Optional[float]) -> str:
    """Format duration in seconds to MM:SS format."""
    if seconds is None or seconds <= 0:
        return "0m 0s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def format_date(iso_date: Optional[str]) -> str:
    """Format ISO date to readable format."""
    if not iso_date:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_date


def extract_crm_context(call_details: List[dict]) -> Optional[Dict]:
    """Extract CRM account information from first call's context."""
    if not call_details:
        return None

    first_call = call_details[0]
    context = first_call.get("context", [])

    for item in context:
        if item.get("system") == "CRM" and item.get("objectType") == "Account":
            objects = item.get("objects", [])
            if objects:
                return objects[0].get("fields", {})

    return None


def extract_opportunities(call_details: List[dict]) -> List[Dict]:
    """Extract active opportunities from CRM context."""
    if not call_details:
        return []

    opps = []
    first_call = call_details[0]
    context = first_call.get("context", [])

    for item in context:
        if item.get("system") == "CRM" and item.get("objectType") == "Opportunity":
            for obj in item.get("objects", []):
                fields = obj.get("fields", {})
                opps.append({
                    "name": fields.get("Name"),
                    "stage": fields.get("StageName"),
                    "amount": fields.get("Amount"),
                    "close_date": fields.get("CloseDate"),
                })

    return opps


def build_speaker_map(call_details: List[dict]) -> Dict[str, str]:
    """Build map of speaker IDs to names from parties data."""
    speaker_map = {}

    for call in call_details:
        for party in call.get("parties", []):
            speaker_id = party.get("speakerId")
            if speaker_id and speaker_id not in speaker_map:
                # Try to get name, fall back to email or ID
                name = party.get("name") or party.get("emailAddress") or f"Speaker {speaker_id}"
                speaker_map[speaker_id] = name

    return speaker_map


def format_transcript_segment(segment: dict, speaker_map: Dict[str, str], current_topic: Optional[str]) -> tuple:
    """Format a transcript segment with speaker name and check for topic changes."""
    speaker_id = segment.get("speakerId")
    speaker_name = speaker_map.get(speaker_id, f"Speaker {speaker_id}")

    # Check if topic changed
    topic = segment.get("topic")
    topic_header = None
    if topic and topic != current_topic:
        topic_header = f"\n--- {topic} ---\n"
        current_topic = topic

    # Format sentences
    sentences = segment.get("sentences", [])
    text_lines = []
    for sentence in sentences:
        text = sentence.get("text", "").strip()
        if text:
            text_lines.append(f"[{speaker_name}]: {text}")

    return topic_header, "\n".join(text_lines), current_topic


def convert_account_to_markdown(account_slug: str, force: bool = False) -> bool:
    """Convert a single account's JSON transcripts to markdown format."""
    account_dir = ACCOUNTS_DIR / account_slug

    if not account_dir.exists():
        print(f"Account directory not found: {account_dir}")
        return False

    # Check if update needed
    if not force and not is_markdown_stale(account_dir):
        return True  # Already up to date

    # Load data
    metadata = load_json(account_dir / "metadata.json")
    transcripts = load_json(account_dir / "transcripts.json")
    call_details = load_json(account_dir / "call_details.json")

    if not metadata or not transcripts:
        print(f"Missing required JSON files for {account_slug}")
        return False

    # Extract account info
    account_name = metadata.get("account_name", account_slug)
    call_count = metadata.get("call_count", 0)

    # Build speaker map
    speaker_map = build_speaker_map(call_details or []) if call_details else {}

    # Extract CRM context
    crm_info = extract_crm_context(call_details) if call_details else None
    opportunities = extract_opportunities(call_details) if call_details else []

    # Start building markdown
    md_lines = [
        f"# {account_name} - Gong Call Transcripts",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Total Calls**: {call_count}",
        f"**Last Updated**: {metadata.get('last_fetched', 'Unknown')}",
        f"**Account Slug**: {account_slug}",
        "",
    ]

    # Add CRM information if available
    if crm_info:
        md_lines.extend([
            "## CRM Account Information",
            ""
        ])
        for key, value in crm_info.items():
            if value:
                md_lines.append(f"- **{key}**: {value}")
        md_lines.append("")

    # Add opportunities if any
    if opportunities:
        md_lines.extend([
            "## Active Opportunities",
            ""
        ])
        for opp in opportunities:
            if opp.get("name"):
                stage = opp.get("stage", "Unknown")
                amount = f"${opp.get('amount', 0):,.0f}" if opp.get("amount") else "N/A"
                close = opp.get("close_date", "N/A")
                md_lines.append(f"- **{opp['name']}** — Stage: {stage}, Amount: {amount}, Close: {close}")
        md_lines.append("")

    md_lines.append("---")
    md_lines.append("")

    # Sort calls chronologically
    transcript_list = sorted(transcripts.items(), key=lambda x: x[1].get("started", ""))

    # Process each call
    for idx, (call_id, transcript) in enumerate(transcript_list, 1):
        # Find matching call details
        call_detail = None
        if call_details:
            call_detail = next((c for c in call_details if c.get("metaData", {}).get("id") == call_id), None)

        # Call header
        title = transcript.get("title", "Untitled Call")
        started = format_date(transcript.get("started"))
        duration = format_duration(transcript.get("duration"))
        url = transcript.get("url", "")

        md_lines.extend([
            f"## Call #{idx}: {title}",
            f"**Date**: {started}",
            f"**Duration**: {duration}",
            f"**Call ID**: {call_id}",
        ])

        if url:
            md_lines.append(f"**Gong URL**: {url}")

        md_lines.append("")

        # External participants
        if call_detail:
            external = [p for p in call_detail.get("parties", []) if p.get("affiliation", "").lower() == "external"]
            if external:
                md_lines.append("### External Participants")
                for p in external:
                    name = p.get("name", p.get("emailAddress", "Unknown"))
                    title = p.get("title")
                    if title:
                        md_lines.append(f"- {name} ({title})")
                    else:
                        md_lines.append(f"- {name}")
                md_lines.append("")

            # Internal participants
            internal = [p for p in call_detail.get("parties", []) if p.get("affiliation", "").lower() == "internal"]
            if internal:
                md_lines.append("### Internal Participants")
                for p in internal:
                    name = p.get("name", p.get("emailAddress", "Unknown"))
                    title = p.get("title")
                    if title:
                        md_lines.append(f"- {name} ({title})")
                    else:
                        md_lines.append(f"- {name}")
                md_lines.append("")

        # Transcript
        md_lines.append("### Transcript")
        md_lines.append("")

        structure = transcript.get("structure", [])
        if structure:
            current_topic = None
            for segment in structure:
                topic_header, segment_text, current_topic = format_transcript_segment(
                    segment, speaker_map, current_topic
                )
                if topic_header:
                    md_lines.append(topic_header)
                if segment_text:
                    md_lines.append(segment_text)
                    md_lines.append("")
        else:
            md_lines.append("*No transcript available*")
            md_lines.append("")

        md_lines.append("---")
        md_lines.append("")

    # Write markdown file
    markdown_path = account_dir / "transcripts.md"
    markdown_content = "\n".join(md_lines)

    try:
        with open(markdown_path, 'w') as f:
            f.write(markdown_content)

        # Update metadata
        metadata["markdown_generated"] = datetime.now().isoformat()
        metadata["markdown_call_count"] = call_count
        save_json(account_dir / "metadata.json", metadata)

        print(f"✓ Generated markdown for {account_name} ({call_count} calls, {len(markdown_content):,} chars)")
        return True

    except Exception as e:
        print(f"✗ Failed to write markdown for {account_slug}: {e}")
        return False


def convert_all_accounts(force: bool = False):
    """Convert all cached accounts to markdown."""
    if not ACCOUNTS_DIR.exists():
        print(f"Accounts directory not found: {ACCOUNTS_DIR}")
        return

    account_dirs = [d for d in ACCOUNTS_DIR.iterdir() if d.is_dir()]

    if not account_dirs:
        print("No cached accounts found")
        return

    print(f"Found {len(account_dirs)} cached accounts")
    print()

    success_count = 0
    skip_count = 0
    fail_count = 0

    for account_dir in sorted(account_dirs):
        account_slug = account_dir.name

        if not force and not is_markdown_stale(account_dir):
            skip_count += 1
            print(f"⊘ Skipped {account_slug} (already up to date)")
            continue

        if convert_account_to_markdown(account_slug, force=force):
            success_count += 1
        else:
            fail_count += 1

    print()
    print(f"Summary: {success_count} converted, {skip_count} skipped, {fail_count} failed")

    if success_count > 0:
        print()
        print("Next steps:")
        print("  1. Index in QMD: npx -y @tobilu/qmd update gong")
        print("  2. Generate embeddings: npx -y @tobilu/qmd embed")
        print("  3. Verify: npx -y @tobilu/qmd status")


def sync_stale_accounts():
    """Update only markdown files that are stale (JSON newer than MD)."""
    if not ACCOUNTS_DIR.exists():
        print(f"Accounts directory not found: {ACCOUNTS_DIR}")
        return

    account_dirs = [d for d in ACCOUNTS_DIR.iterdir() if d.is_dir()]
    stale_accounts = [d for d in account_dirs if is_markdown_stale(d)]

    if not stale_accounts:
        print("All markdown files are up to date")
        return

    print(f"Found {len(stale_accounts)} stale markdown files")
    print()

    success_count = 0
    for account_dir in stale_accounts:
        if convert_account_to_markdown(account_dir.name):
            success_count += 1

    print()
    print(f"Updated {success_count}/{len(stale_accounts)} accounts")


def main():
    parser = argparse.ArgumentParser(description="Convert Gong JSON transcripts to markdown for QMD")
    parser.add_argument("--account", help="Convert specific account by name")
    parser.add_argument("--all", action="store_true", help="Convert all cached accounts")
    parser.add_argument("--sync", action="store_true", help="Update only stale markdown files")
    parser.add_argument("--force", action="store_true", help="Force regeneration even if up to date")

    args = parser.parse_args()

    if args.sync:
        sync_stale_accounts()
    elif args.all:
        convert_all_accounts(force=args.force)
    elif args.account:
        slug = slugify(args.account)
        convert_account_to_markdown(slug, force=args.force)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
