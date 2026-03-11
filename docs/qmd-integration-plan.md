# Plan: QMD Integration with /account-research for Faster Gong Transcript Queries

## Context

The `/account-research` skill currently fetches Gong transcripts via API calls, which takes 2-3 seconds per 20 calls due to rate limiting (0.35s per request). While there's a two-tier cache system (414MB global index + per-account JSON transcripts for 33 accounts), each query still requires:

1. Filtering the 414MB calls.json file in memory
2. Making Gong API calls to fetch transcripts for matched calls
3. Waiting for rate limiting between requests

We now have QMD set up with semantic search capabilities, but the `gong` collection is empty because transcripts are stored as JSON files, and QMD only indexes `**/*.md` files.

**The Opportunity**: Convert cached JSON transcripts to markdown format, index them in QMD, and enable instant semantic retrieval for cached accounts + cross-account intelligence queries.

## Proposed Solution

### Architecture: Dual-Format Strategy

Maintain both JSON (programmatic access) and Markdown (semantic search) with automated sync:

```
~/claude-work/gong-cache/accounts/{slug}/
├── metadata.json (existing + new tracking fields)
├── transcripts.json (existing - source of truth)
└── transcripts.md (NEW - QMD-indexable format)
```

**Key Decision**: One markdown file per account (not per call) to keep QMD index manageable (33 files vs 200+ calls).

### Markdown Format

```markdown
# {Account Name} - Gong Call Transcripts

**Generated**: {timestamp}
**Total Calls**: {count}
**Account Slug**: {slug}

## CRM Account Information
- **Name**: {crm_name}
- **Website**: {website}
- **Subscription ARR**: {arr}
[...]

## Active Opportunities
- **{opp_name}** — Stage: {stage}, Amount: ${amount}

---

## Call #1: {Call Title}
**Date**: {YYYY-MM-DD HH:MM}
**Duration**: {MM}m {SS}s
**Call ID**: {gong_call_id}
**Gong URL**: {url}

### External Participants
- {Name} ({Title})

### Internal Participants
- {Name} ({Title})

### Transcript

--- {Topic Name} ---

[{Speaker Name}]: {sentence text}
[{Speaker Name}]: {sentence text}

---

[Repeat for each call chronologically]
```

## Implementation Plan

### Phase 1: Core Conversion Script (4-6 hours)

**Create**: `~/claude-work/gong_json_to_markdown.py`

```python
#!/usr/bin/env python3
"""
Convert Gong transcript JSON to QMD-indexable markdown.

Usage:
    python gong_json_to_markdown.py --account "Chalice"
    python gong_json_to_markdown.py --all
    python gong_json_to_markdown.py --sync  # Update stale MD files
    python gong_json_to_markdown.py --all --force
"""
```

**Core Functions**:
1. **Staleness Detection**: Compare `metadata.json` timestamp with `transcripts.md` mtime
2. **Speaker Resolution**: Build speaker map from global `calls.json` parties data
3. **CRM Context Extraction**: Parse first call's context array for Account/Opportunity objects
4. **Markdown Generation**: Template-based with speaker attribution, topic markers, chronological ordering
5. **Batch Processing**: `--all` mode with progress reporting and error handling

**Enhanced metadata.json**:
```json
{
  "account_name": "Chalice",
  "last_fetched": "2026-03-06T01:16:28.323956+00:00",
  "call_count": 15,
  "call_ids": [...],
  "cache_version": 2,
  "markdown_generated": "2026-03-11T10:30:00+00:00",  // NEW
  "markdown_call_count": 15  // NEW: for staleness detection
}
```

**Testing**:
- Small account: "acelab" (1 call, 46KB JSON)
- Large account: "cherre" (62 calls, 2.6MB JSON)
- Verify markdown format, speaker names, chronological ordering

### Phase 2: Batch Processing & Initial Index (2-3 hours)

1. **Convert All Cached Accounts**:
   ```bash
   cd ~/claude-work
   python gong_json_to_markdown.py --all
   ```
   Expected: ~10-15MB total markdown across 33 accounts

2. **Index in QMD**:
   ```bash
   npx -y @tobilu/qmd update gong
   npx -y @tobilu/qmd embed
   npx -y @tobilu/qmd status  # Verify 33 files indexed
   ```

3. **Test Semantic Queries**:
   ```bash
   npx -y @tobilu/qmd query "Kubernetes migration challenges" -c gong
   npx -y @tobilu/qmd query "pricing objections" -c gong
   npx -y @tobilu/qmd search "Dagster" -c gong
   ```

### Phase 3: Skill Integration (3-4 hours)

**Modify**: `/Users/vishwasrinivasan/.claude/skills/gong-account-research/SKILL.md`

**Add QMD Check at Start** (before existing Gong API calls):

```markdown
### Step 1: Check QMD Cache First

Try semantic search via QMD MCP tools:

1. Search for account in gong collection:
   - Use ReadMcpResourceTool or qmd CLI
   - Query: "qmd://gong/accounts/{slug}/transcripts.md"

2. If found:
   - Use markdown content directly
   - Skip API calls (saves 2-3 seconds)

3. If not found or stale:
   - Proceed to Step 2 (existing API workflow)
   - After fetching, convert JSON to markdown
   - Update QMD index

### Step 2: Fetch from Gong API (EXISTING FLOW)

[Preserve current implementation as fallback]
```

**Add Flags**:
- `--skip-qmd`: Force API path (for testing)
- `--qmd-only`: Fail if QMD unavailable (validation mode)

**Testing**:
- Cached account query (should use QMD)
- New account query (should use API + generate MD)
- QMD unavailable (should fallback gracefully)

### Phase 4: Automated Sync (1-2 hours)

**Update Cron Job**: `~/.cron/gong-sync.sh` (or create if doesn't exist)

```bash
#!/bin/bash
cd ~/claude-work

# Existing: Update global call index
python3 gong_account_transcripts.py --sync

# NEW: Convert stale JSON to markdown
python3 gong_json_to_markdown.py --sync

# NEW: Refresh QMD index
cd ~/.cache/qmd
npx -y @tobilu/qmd update gong

# Log completion
echo "$(date): Gong sync completed" >> ~/claude-work/gong-cache/sync.log
```

**Schedule**: Leverage existing 6 AM daily cron (or add new entry)

**On-Demand Sync**: Add hook to `gong_account_transcripts.py`:
```python
# After saving transcripts.json
subprocess.run([
    "python3",
    "~/claude-work/gong_json_to_markdown.py",
    "--account", account_slug
])
```

### Phase 5: Cross-Account Intelligence (Future Enhancement)

**New Capability**: Semantic queries across all accounts

Examples:
- "Show all accounts discussing Kubernetes scaling issues"
- "Which accounts mentioned Dagster as a competitor?"
- "Find accounts with pricing objections related to support tiers"

**Implementation**: Can be added as new skill `/gong-cross-account` or integrated into existing skills.

## Critical Files

**Reference Implementation**:
- `/Users/vishwasrinivasan/claude-work/gong_account_transcripts.py` - JSON structure, speaker mapping, CRM context extraction
- `/Users/vishwasrinivasan/Account Context/HappyRobot/Gong_Call_History.md` - Markdown format pattern
- `/Users/vishwasrinivasan/claude-work/gong-cache/accounts/cherre/transcripts.json` - Largest JSON (62 calls) for testing

**Files to Modify**:
- `/Users/vishwasrinivasan/.claude/skills/gong-account-research/SKILL.md` - Add QMD check with fallback

**Files to Create**:
- `~/claude-work/gong_json_to_markdown.py` - Core conversion script
- `~/.cron/gong-sync.sh` - Enhanced sync script (if doesn't exist)

## Success Metrics

**Performance**:
- QMD retrieval: <500ms (vs API: 2-3s) → **4-6x faster**
- Cache hit rate: >90% of queries use QMD
- Daily sync: <60s for all accounts

**Quality**:
- 100% JSON data represented in markdown
- >95% speakers have names (not IDs)
- <1% markdown files >24h stale

## Benefits

1. **Speed**: Eliminate API calls for 33+ cached accounts (instant vs 2-3s)
2. **Intelligence**: Cross-account semantic queries ("all accounts mentioning Airflow alternatives")
3. **Relevance**: Vector search matches concepts, not just keywords/CRM names
4. **Reliability**: Graceful fallback to API maintains existing workflow
5. **Future-Ready**: Foundation for advanced analytics (sentiment, competitive intel, win/loss patterns)

## Risk Mitigation

**Stale Data**: Automated daily sync + on-demand conversion when JSON updates
**Index Corruption**: JSON remains source of truth; can regenerate markdown anytime
**Performance**: Tested with large account (62 calls); chunking available for 100+ call accounts
**Breaking Changes**: API fallback always available; feature flag to disable QMD path

## Verification Plan

After implementation:

1. **Test Conversion**:
   ```bash
   python gong_json_to_markdown.py --account "Chalice"
   cat ~/claude-work/gong-cache/accounts/chalice/transcripts.md
   ```

2. **Test QMD Index**:
   ```bash
   npx -y @tobilu/qmd ls gong
   npx -y @tobilu/qmd status
   ```

3. **Test Semantic Search**:
   ```bash
   npx -y @tobilu/qmd query "data orchestration pain points" -c gong -n 5
   ```

4. **Test Skill Integration**:
   - Query cached account via `/account-research` (should use QMD)
   - Query new account (should use API + generate MD)
   - Verify results match existing format

5. **Test Sync**:
   ```bash
   # Trigger new transcript fetch
   python gong_account_transcripts.py "NewAccount"

   # Verify markdown auto-generated
   ls ~/claude-work/gong-cache/accounts/newaccount/transcripts.md

   # Verify QMD updated
   npx -y @tobilu/qmd query "NewAccount" -c gong
   ```

## Rollback Plan

If issues arise:
- **Immediate**: Add `--skip-qmd` flag to skill, force API path
- **Short-term**: Remove QMD check from skill (revert to original)
- **Long-term**: Keep markdown for manual exploration; don't integrate with skill

Low-risk because JSON cache unchanged (source of truth) and API workflow fully preserved.
