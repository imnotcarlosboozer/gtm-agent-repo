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
1. **Rep name** (default to "Rep" if not provided)
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
- Rep: "Rep"
- Year: 2026

### Step 2: Run Pipeline Script

Execute the Python script:

```bash
python3 ~/astronomer-claude-skills/scripts/quarterly_pipeline_context.py \
  --rep "{{rep_name}}" \
  --quarter "Q{{quarter}} {{year}}" \
  --fiscal
```

The script will:
1. Load cached Gong data from `~/claude-work/gong-cache/all_calls/calls.json`
2. Auto-resolve rep name to email (e.g., "Rep Name" → "rep@astronomer.io")
3. Validate rep exists in Gong data and has opportunities in the quarter
4. Filter opportunities by rep + quarter using fiscal calendar (Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan)
5. Generate main pipeline report with opportunities table
6. For each unique account:
   - Fetch Gong transcripts filtered to quarter dates (uses cached transcripts)
   - Copy existing research file if found in `~/Account Context/[Company]/`
7. Create organized folder structure at `~/Pipeline Reports/[Rep Name]/Q{N}_{YEAR}/`
8. Print execution summary

### Step 3: Present Results

After the script completes, show the user a formatted summary:

```markdown
✓ Q{{quarter}} {{year}} Pipeline Report Generated for {{rep_name}}

📊 Pipeline Summary:
  • Total Opportunities: [count]
  • Total Pipeline Value: $[amount]
  • Top Stage: [stage_name] ([count] deals, $[amount])

📁 Location: ~/Pipeline Reports/{{rep_name}}/Q{{quarter}}_{{year}}/

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
~/Pipeline Reports/[Rep Name]/Q{N}_{YEAR}/
├── Pipeline_Report.md
└── Accounts/
    ├── Company_A/
    │   ├── gong_transcripts.md
    │   └── company_research.md (if exists)
    └── Company_B/
        └── gong_transcripts.md
```

**Note:** Pipeline Reports are now separate from Account Context:
- `~/Pipeline Reports/` = Temporal quarterly snapshots organized by rep
- `~/Account Context/` = Permanent company research files

## Error Handling

**If rep name not found:** The script auto-constructs emails from names (e.g., "Rep Name" → "rep@astronomer.io") and validates against Gong data. If validation fails, it will show available reps in the system.

**If no opportunities found:** Script validates that rep exists and has opportunities in the quarter. Provides helpful error messages if:
- No calls with this rep in the specified quarter
- Email address is incorrect
- Rep has no opportunities closing in this quarter

**If account has no Gong data:** Skip with warning, don't block other accounts

**If quarter parsing fails:** Prompt user for clarification (e.g., "Did you mean Q1 2026 or Q1 2025?")

**If global Gong cache missing:** Instruct user to run sync first:
```bash
python3 ~/claude-work/gong_account_transcripts.py --sync
```

## Example Usage

**User:** "Generate Q1 2026 pipeline report for Thomas Messana"

**Assistant:** [Runs script with --rep "Rep Name" --quarter "Q1 2026"]

**Script auto-resolves:** "Rep Name" → "rep@astronomer.io"

**Output:** Shows formatted summary with pipeline metrics, location at `~/Pipeline Reports/Thomas Messana/Q1_2026/`, and account context stats.

**User:** "Generate Q1 2026 pipeline report for Vishwa"

**Assistant:** [Runs script with --rep "Rep" --quarter "Q1 2026"]

**Script resolves:** "Rep" → "rep@astronomer.io" (via REP_EMAIL_MAP)

**Output:** Shows formatted summary at `~/Pipeline Reports/Vishwa Srinivasan/Q1_2026/`
