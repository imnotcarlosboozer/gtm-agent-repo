---
name: account-question
description: Answer questions about any account using internal data sources (Snowflake ACCOUNT_360_V, ACCOUNT_NOTES, Gong transcripts, CRM). Use this skill whenever the user asks about an account's calls, what was discussed, pain points, tech stack, stakeholders, deal status, objections, competitors, or anything that would be answered by reviewing internal sales data. Also trigger when the user mentions "Gong", "calls", "transcripts", or asks things like "what did we talk about with [company]", "what's going on with [account]", or "draft an email for [account]". Even if the user doesn't explicitly say "Gong", if they're asking a question about an account that sounds like it needs internal conversation history to answer, use this skill.
---

# Account Question

Answer questions about an account using Snowflake as the primary source of truth — single-query snapshots, interaction history, Gong transcripts, CRM data — plus local fallback files.

## Architecture

- **ACCOUNT_360_V**: Single-query pre-joined account snapshot (ARR, usage, Gong signals, ZD tickets, contacts, research)
- **ACCOUNT_NOTES**: All interaction history — pre-call briefs, email drafts, Claude session notes, cron-generated summaries
- **GONG_CALL_ENRICHMENTS_V + GONG_CALL_TRANSCRIPTS**: Enriched call signals + full transcripts
- **Local fallback**: `~/claude-work/research-assistant/outputs/accounts/<slug>/` (report.md, interactions.md) — check if ACCOUNT_NOTES is sparse

## Input
The user has provided: {{args}}

This could be:
- An account name with a question: "Iron Mountain - what are their pain points?"
- Just an account name: "Iron Mountain" (give a general overview)
- A follow-up question about a previously loaded account

## Steps

### 0. Resolve Account ID

Check the ID cache in SKILL.md first. If found, use `ACCT_ID` directly in all queries (fastest). If not cached, resolve via:
```sql
SELECT ACCT_ID, ACCT_NAME, ORG_ID FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
WHERE ACCT_NAME ILIKE '%{ACCOUNT_NAME}%' LIMIT 1
```

### 1. Full Account Snapshot + Interaction History (run in parallel)

**Query A — ACCOUNT_360_V** (single query, all signals pre-joined):
```sql
SELECT ACCT_NAME, TOTAL_ARR_AMT, USAGE_AMT_30D, CREDIT_BALANCE,
       CONTRACT_END_DATE, DAYS_TO_RENEWAL, USAGE_VS_CONTRACT_TARGET_PCT_30D,
       CREDIT_UTILIZATION_PCT, PROJECTED_FULL_CREDIT_USE_DATE_30D,
       OWNER_NAME, FIELD_ENGINEER, CUST_SUCCESS_MANAGER,
       LAST_CALL_DATE, LAST_GONG_SENTIMENT, LAST_DEAL_RISK, LAST_PAIN_POINTS, CALL_COUNT_90D,
       OPEN_TICKET_COUNT, P1_OPEN_COUNT, LAST_TICKET_DATE, AVG_ZD_SENTIMENT,
       CONTACT_COUNT, PRODUCT_USER_COUNT, DOMAIN_HAS_CERTIFICATION,
       VISITS_30D, LAST_VISIT_DATE,
       RESEARCH_SCORE, RESEARCH_TIER, KEY_SIGNALS
FROM GTM.PUBLIC.ACCOUNT_360_V
WHERE ACCT_ID = '{ACCT_ID}'
```

**Query B — ACCOUNT_NOTES** (all prior interaction history):
```sql
SELECT NOTE_DATE, NOTE_TYPE, SOURCE, CONTENT
FROM GTM.PUBLIC.ACCOUNT_NOTES
WHERE ACCT_ID = '{ACCT_ID}'
ORDER BY NOTE_DATE DESC, CREATED_AT DESC
LIMIT 20
```

Read both. ACCOUNT_NOTES gives you full conversation history — what was discussed, email drafts already sent, pre-call briefs already generated.

### 2. CRM Deep-Dive (run in parallel with Step 3 if needed)

Only run if 360_V doesn't have enough detail on opp or contacts.

**Query 2A — Opportunity history**:
```sql
SELECT o.OPP_NAME, o.CURRENT_STAGE_NAME, o.IS_WON, o.IS_LOST, o.IS_OPEN,
       o.LOSS_REASON, o.LOSS_DETAILS, o.COMPETITION, o.CLOUD_PROVIDER,
       o.AIRFLOW_EXPERIENCE, o.AIRFLOW_COMMITMENT,
       o.CURRENT_AIRFLOW_DEPLOYMENT_MODEL, o.CURRENT_AIRFLOW_VERSIONS,
       o.CREATED_DATE, o.WON_DATE, o.LOST_DATE, o.AMT, o.NEXT_STEPS
FROM HQ.MODEL_CRM.SF_OPPS o
WHERE o.ACCT_ID = '{ACCT_ID}'
ORDER BY o.CREATED_DATE DESC
LIMIT 10
```

**Query 2B — Contacts with intent signals** (use CONTACT_360_V — richer than raw SF_CONTACTS):
```sql
SELECT TITLE, CONTACT_STATUS, LEAD_SCORE_GRADE, IS_PRODUCT_USER,
       LAST_VISITED_PRICING_PAGE_DATE, LAST_VISITED_DEBUGGING_AIRFLOW_PAGE_DATE,
       LAST_MQL_DATE, MQL_COUNT, LAST_MQL_CHANNEL, DOMAIN_HAS_CERTIFICATION,
       IS_OPTED_OUT_OF_EMAIL, CONTACT_URL, LAST_ACTIVITY_TS
FROM GTM.PUBLIC.CONTACT_360_V
WHERE ACCT_ID = '{ACCT_ID}'
ORDER BY LAST_ACTIVITY_TS DESC NULLS LAST
LIMIT 15
```

### 3. Gong Call Detail (if question requires call-level specifics)

**Enrichment summary** (pain points, sentiment, deal risk — last 5 calls):
```sql
SELECT e.CALL_DATE, e.SENTIMENT_SCORE, e.DEAL_RISK,
       e.PAIN_POINTS, e.TECH_STACK, e.COMPETITORS, e.AIRFLOW_TOPICS,
       c.CALL_TITLE, c.CALL_URL, c.CALL_BRIEF, c.CALL_NEXT_STEPS,
       c.PRIMARY_EMPLOYEE, c.CALL_DURATION
FROM GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V e
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON e.CALL_ID = c.CALL_ID
WHERE e.ACCT_ID = '{ACCT_ID}'
  AND c.IS_DELETED = FALSE
ORDER BY e.CALL_DATE DESC
LIMIT 5
```

**Full transcript** (only if user asks "what exactly was said" or needs verbatim quotes):
```sql
SELECT t.CALL_TITLE, t.SCHEDULED_TS, t.CALL_BRIEF, t.CALL_NEXT_STEPS,
       t.ATTENDEES, t.FULL_TRANSCRIPT
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE t.ACCT_NAME ILIKE '%{ACCOUNT_NAME}%'
  AND c.IS_DELETED = FALSE
ORDER BY t.SCHEDULED_TS DESC
LIMIT 3
```

### 4. Local File Fallback

If ACCOUNT_NOTES is empty (account hasn't been discussed in a Claude session yet), also check:
- `~/claude-work/research-assistant/outputs/accounts/<slug>/report.md` — prior research output
- `~/claude-work/research-assistant/outputs/accounts/<slug>/interactions.md` — any legacy local notes

These are secondary. Snowflake is the source of truth going forward.

### 5. Answer the Question

Use all gathered context to answer. Surface the most actionable signals first:
- `LAST_DEAL_RISK` + `LAST_PAIN_POINTS` — what's driving deal risk right now
- `SF_OPPS.AIRFLOW_EXPERIENCE` + `COMPETITION` — what they said in discovery
- `LAST_VISITED_PRICING_PAGE_DATE` on contacts — buying signal (flag if within 30 days)
- Renewal proximity (`DAYS_TO_RENEWAL`) — urgency flag
- Recent ACCOUNT_NOTES entries — what was already discussed / decided

If no specific question was asked, give a brief overview: deal status, key contacts, recent call themes, any risks or signals worth acting on.

### 6. Save Output

After answering, persist the note via:
```bash
source ~/.zshrc && $HOME/.venvs/snowflake/bin/python3 \
  $HOME/claude-work/scripts/write_account_note.py \
  --acct-id "{ACCT_ID}" \
  --acct-name "{ACCT_NAME}" \
  --note-type interaction \
  --content "{markdown_summary_of_session}" \
  --source claude
```

This also writes the local `interactions.md` fallback automatically.

### 7. Stay Ready for Follow-Ups

Data is already in context. Answer follow-up questions directly without re-querying. Save any new outputs (email drafts, action items) to ACCOUNT_NOTES with the appropriate `--note-type`.

---

**Begin:** {{args}}
