---
name: apollo-add-to-sequences
description: >
  Adds prospects from a CSV to Apollo sequences with automatic contact enrichment.
  Triggers when user mentions a CSV file and wants to add contacts to sequences,
  enroll in campaigns, or send outreach. Handles contact creation, sequence assignment,
  and automatic activation.
---

# Apollo Add to Sequences Skill

Add prospects from a CSV file to Apollo sequences with automatic contact enrichment and sequence activation.

## Trigger

Use this skill when the user asks to:
- "add them to sequence" (with CSV mentioned)
- "enroll these in Apollo" (with CSV path)
- "add contacts to sequences" or "add to apollo sequences"
- "process this CSV for Apollo" or "send via Apollo"
- Mentions a CSV file path and any variant of adding/enrolling/sequencing

## Required Information

1. **CSV File Path** - Full path to the CSV file (usually in ~/Downloads/)

The CSV must contain these columns:
- `First Name`
- `Last Name`
- `Email`
- `Recommended Outreach Sequence`
- `Last Activity` (optional - used for webinar ATTENDED/NO SHOW logic)

## How It Works

The script will:
1. **Fetch all sequences** from Apollo (pagination support for 800+ sequences)
2. **Search or create contacts** in Apollo (enrichment happens automatically)
3. **Match sequence names** from the CSV to actual Apollo sequences (exact matching)
4. **Handle webinar variants** automatically (ATTENDED vs NO SHOW based on Last Activity)
5. **Add contacts to sequences** with detailed skip tracking
6. **Activate all sequences** that received new contacts
7. **Report results** with clear success/skip/error counts

## Execution

```bash
cd ~/claude-work/scripts
python3 add_to_apollo_sequences.py /path/to/file.csv
```

The script accepts the CSV path as a command-line argument — no need to edit the script.

## Step-by-Step Process

### 1. Identify the CSV file
Extract the CSV path from the user's message. Common locations:
- `~/Downloads/report*.csv`
- `~/Downloads/[filename].csv`

### 2. Run the script
```bash
cd ~/claude-work/scripts
python3 add_to_apollo_sequences.py ~/Downloads/your_file.csv
```

### 3. Monitor output
The script provides real-time progress:
- Contact search/creation status
- Sequence matching (including ATTENDED/NO SHOW logic)
- Skip reasons (already in sequence, job change detected)
- Activation results per sequence

## Output Format

After completion, present the summary:

```markdown
Apollo Sequence Enrollment Complete

Results:
  - Total prospects: {total}
  - Added to sequences: {added}
  - Not found in Apollo: {not_found}
  - No sequence assigned: {no_sequence}
  - Already in other sequences: {skipped_in_other}
  - Job change detected: {skipped_job_change}
  - Errors: {errors}

Sequences:
  - {sequence_count} sequences used
  - {activated} sequences activated
  - {failed} activation failures

Manual Actions Needed:
[List any contacts that need manual intervention]
```

## Skip Reasons & Actions

### Already in Other Active Sequences
**What happened:** Contact is already enrolled in a different active sequence
**Action needed:** Manually remove from current sequence in Apollo, then re-run

### Job Change Detected
**What happened:** Apollo detected recent employment change
**Action needed:** Review contact details in Apollo and manually add if appropriate

## Webinar Sequence Logic

For sequences containing "Webinar" or "webinar":
- Script looks for `{Sequence Name} ATTENDED` and `{Sequence Name} NO SHOW` variants
- Routes based on `Last Activity` column:
  - **Has activity date** -> ATTENDED sequence
  - **Empty activity** -> NO SHOW sequence
- If only one variant exists, uses that variant
- If neither exist, reports sequence not found

## Setup Requirements

### Script location
`~/claude-work/scripts/add_to_apollo_sequences.py`

### Config file
`~/claude-work/scripts/apollo_config.py` reads from environment variables:
- `APOLLO_API_KEY` — set in `~/.zshrc`
- `EMAIL_ACCOUNT_ID` — defaults to your account ID if not set

### Dependencies
```bash
pip install requests
```

## Troubleshooting

**"Sequence not found" errors:**
- Check sequence name spelling in CSV matches Apollo exactly
- For webinar sequences, ensure ATTENDED/NO SHOW variants exist

**"Contact not found" errors:**
- Email may not exist in Apollo's database
- Try manual search in Apollo to verify

**API errors:**
- Verify `APOLLO_API_KEY` env var is set (`echo $APOLLO_API_KEY`)
- Check Apollo API rate limits haven't been exceeded

## Rate Limiting

- 0.5s delay between contact API calls
- 0.3s delay between sequence page fetches
- Large CSVs may take several minutes
