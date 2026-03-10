---
name: quarterly-pipeline-report
description: Generate quarterly pipeline report with account context. Use when user asks for "quarterly pipeline", "Q1 pipeline with context", "pipeline report for [quarter]", or mentions "pipeline opportunities" with a specific quarter/timeframe.
version: 1.0.0
---

# Quarterly Pipeline Report with Account Context

Generate a comprehensive quarterly pipeline report including:
- Pipeline opportunities table (filtered by rep and quarter)
- Gong call transcripts for each account (filtered to quarter dates)
- Existing research reports (if previously saved)

## Task

The user has requested: {{args}}

Parse the input to extract:
1. **Rep name** (default to "Vishwa" if not provided)
2. **Quarter** (e.g., "Q1", "Q2", etc.)
3. **Year** (default to 2026 if not specified)

## Execution Steps

### Step 1: Parse User Input

Extract the rep name and quarter from the user's request.

Common patterns:
- "Vishwa Q1 2026"
- "Q1 2026" (assumes Vishwa)
- "Q1" (assumes Vishwa and 2026)
- "quarterly pipeline for Q2"

Default values:
- Rep: "Vishwa"
- Year: 2026

### Step 2: Run Pipeline Script

Execute the Python script:

```bash
python3 /Users/vishwasrinivasan/Scripts/quarterly_pipeline_context.py \
  --rep "{{rep_name}}" \
  --quarter "Q{{quarter}} {{year}}" \
  --fiscal
```

The script will:
1. Load cached Gong data from `~/claude-work/gong-cache/all_calls/calls.json`
2. Filter opportunities by rep + quarter using fiscal calendar (Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan)
3. Generate main pipeline report with opportunities table
4. For each unique account:
   - Fetch Gong transcripts filtered to quarter dates (uses `gong_account_transcripts.py`)
   - Copy existing research file if found in `~/Account Context/[Company]/`
5. Create organized folder structure at `~/Account Context/Q{N}_{YEAR}_Pipeline/`
6. Print execution summary

### Step 3: Present Results

After the script completes, show the user a formatted summary:

```markdown
✓ Q{{quarter}} {{year}} Pipeline Report Generated for {{rep_name}}

📊 Pipeline Summary:
  • Total Opportunities: [count]
  • Total Pipeline Value: $[amount]
  • Top Stage: [stage_name] ([count] deals, $[amount])

📁 Location: ~/Account Context/Q{{quarter}}_{{year}}_Pipeline/

📋 Account Context Generated:
  • [X] accounts with Gong transcripts
  • [Y] accounts with existing research (copied)
  • Skipped: [Z] accounts (no account name in Salesforce)

🔥 Top Accounts by Call Volume:
  📄 [Account1]: [X] calls (research available)
  📄 [Account2]: [Y] calls (research available)
     [Account3]: [Z] calls (no prior research)
  ...
```

### Step 4: Offer Follow-Up Actions

Ask the user if they would like to:
- Research any specific account in more detail?
- Draft an email brief for an upcoming meeting?
- Compare to previous quarter's pipeline?
- Generate a specific account deep-dive?

## Important Notes

**Execution Time:** ~10-30 seconds depending on number of accounts

**Fiscal Quarters:**
- Q1 = Feb-Apr
- Q2 = May-Jul
- Q3 = Aug-Oct
- Q4 = Nov-Jan

**Research Files:** Only copies if already exists in account folder. No new web searches are performed by this skill.

**Transcripts:** Uses per-account Gong cache for speed. Date filtering ensures only relevant calls are included.

**Folder Structure:**
```
~/Account Context/Q{N}_{YEAR}_Pipeline/
├── Q{N}_{YEAR}_Pipeline_Report.md
└── Accounts/
    ├── Company_A/
    │   ├── gong_transcripts.md
    │   └── company_research.md (if exists)
    └── Company_B/
        └── gong_transcripts.md
```

## Error Handling

**If rep name not found:** Ask user for email address or add to script's REP_EMAIL_MAP

**If account has no Gong data:** Skip with warning, don't block other accounts

**If quarter parsing fails:** Prompt user for clarification (e.g., "Did you mean Q1 2026 or Q1 2025?")

**If global Gong cache missing:** Instruct user to run sync first:
```bash
python3 ~/claude-work/gong_account_transcripts.py --sync
```

## Example Usage

**User:** "Generate Q1 2026 pipeline report for Vishwa"

**Assistant:** [Runs script with --rep "Vishwa" --quarter "Q1 2026"]

**Output:** Shows formatted summary with pipeline metrics, location, and account context stats.
