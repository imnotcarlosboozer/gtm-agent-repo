---
name: account-research
description: Research a company for Astronomer sales fitness using Snowflake (SF_ACCOUNTS, SF_CONTACTS, SF_OPPS, LF_WEBSITE_VISITS, Gong transcripts), web search, and Apollo. Generates a fit score and AE brief. Snowflake is the primary intelligence source — web research fills gaps Snowflake can't answer.
version: 2.0.0
---

# Account Research Orchestrator

> **SOURCE OF TRUTH IS THE DAG**: `~/claude-work/airflow-pipelines/dags/account_research_helpers.py` is the production source of truth. This file is the interactive mirror — **update the DAG helpers first, then reflect changes here immediately after**.
> - Search queries live in `_run_claude_web_research()` (~line 818)
> - ATS detection lives in `get_hiring_signals()` (~line 1365)
> - Sumble enrichment lives in `_run_sumble_enrichment()` (~line 570)
> - Signal/scoring guidance lives in `_SYSTEM_PROMPT` (~line 1557)
>
> **SYNC RULE**: Any time `account_research_helpers.py` is modified (new queries, new data sources, scoring changes, new web search types), update this SKILL.md in the same session before closing.

Research companies for Astronomer (Apache Airflow) sales fitness. Snowflake is the primary data source for CRM intelligence (contacts, buying signals, opp history, Leadfeeder visits, Gong transcripts, scores). Web research is the primary source for tech stack — HG Insights and DataFox signals in Salesforce are unreliable and must not be treated as verified. Always confirm stack via job postings, engineering blog, GitHub, and web search.

## Input
The user has provided: {{args}}

- Single company: `{COMPANY}, {DOMAIN}` (e.g., "Acme Corp, acme.com")
- Batch mode: `batch: /path/to/file.csv` (CSV with columns: company_name, domain)
- Batch force-rerun: `batch: /path/to/file.csv force`

## Constants
- **Prompts Directory**: `~/claude-work/research-assistant/prompts/`
- **Output Directory**: `~/claude-work/research-assistant/outputs/accounts/`
- **Apollo Field ID**: `6998b33edacda9000deb48ca`

---

## SINGLE COMPANY MODE

### Step 1: Parse Input
Extract `COMPANY_NAME` and `DOMAIN`. Strip `http://`, `www.`, trailing slashes. If only a name is given, search for the domain first.

### Step 2: Snowflake Intelligence Dump

Run template check and Apollo key check in bash while simultaneously firing the first Snowflake query:

```bash
for f in ~/claude-work/research-assistant/prompts/01_fit_scoring.md \
          ~/claude-work/research-assistant/prompts/02_account_research.md; do
  [ -f "$(eval echo $f)" ] || { echo "TEMPLATE MISSING: $f — aborting."; exit 1; }
done
echo "TEMPLATES OK"
[ -n "$APOLLO_API_KEY" ] && echo "APOLLO: key set" || echo "APOLLO: no key"
```

**Query A — Account profile** (run immediately, domain match):
```sql
SELECT
  a.ACCT_ID, a.ACCT_NAME, a.ACCT_DOMAIN, a.ACCT_TYPE, a.ACCT_STATUS,
  a.IS_CURRENT_CUST, a.IS_CHURNED_CUST, a.CUSTOMER_SINCE_DATE,
  a.INDUSTRY, a.OWNER_NAME, a.SALES_REGION, a.SEGMENT_PLANNED,
  a.ICP_DESIGNATION_V2, a.ACCT_SCORE, a.ACCT_SCORE_POSITIVE_DRIVERS,
  a.ACCT_SCORE_NEGATIVE_DRIVERS, a.SMOKE_SCORE, a.FIRE_SCORE,
  a.LAST_MQL_DATE, a.LAST_COSMOS_DOC_VIEW_DATE, a.LAST_DAG_FACTORY_DOWNLOAD_DATE,
  a.BILLING_COUNTRY, a.SHIPPING_COUNTRY
FROM HQ.MODEL_CRM.SF_ACCOUNTS a
WHERE LOWER(a.ACCT_DOMAIN) LIKE LOWER('%{DOMAIN}%')
  AND a.ACCT_TYPE NOT IN ('Internal', 'Competitor')
ORDER BY a.IS_CURRENT_CUST DESC, a.ACCT_SCORE DESC NULLS LAST
LIMIT 5
```

Store: `SF_ACCT_ID`, `SF_ACCOUNT_FOUND` (true/false), all signal fields.

**After Query A resolves**, extract `SF_ACCT_ID` and fire Queries B–H in parallel:

**Query B — Contacts with person-level intent signals:**
```sql
SELECT
  c.TITLE, c.LEAD_SCORE_GRADE, c.CONTACT_STATUS,
  c.LAST_VISITED_PRICING_PAGE_DATE,
  c.LAST_VISITED_DEBUGGING_AIRFLOW_PAGE_DATE,
  c.LAST_VISITED_DEBUGGING_DAGS_PAGE_DATE,
  c.LAST_MQL_DATE, c.IS_OPTED_OUT_OF_EMAIL, c.CONTACT_URL,
  c.LAST_ACTIVITY_TS
FROM HQ.MODEL_CRM.SF_CONTACTS c
WHERE c.ACCT_ID = '{SF_ACCT_ID}'
  AND c.IS_DELETED = FALSE
ORDER BY c.LAST_ACTIVITY_TS DESC NULLS LAST
LIMIT 20
```
If `SF_ACCOUNT_FOUND=false`: skip, record "No Salesforce account found — contact intelligence unavailable."

**Query C — Leadfeeder website visits** (replaces entire Leadfeeder MCP):
```sql
SELECT
  v.VISIT_TS, v.LANDING_PAGE, v.PAGE_VIEW_COUNT,
  v.VISIT_DURATION, v.SOURCE, v.MEDIUM, v.CAMPAIGN_NAME,
  p.PAGE_URL, p.PAGE_NAME, p.PAGEVIEW_TS
FROM HQ.MODEL_CRM.LF_WEBSITE_VISITS v
JOIN HQ.MODEL_CRM.LF_PAGE_VIEWS p ON v.LF_VISIT_ID = p.LF_VISIT_ID
WHERE v.SF_ACCT_ID = '{SF_ACCT_ID}'
  AND v.VISIT_TS >= DATEADD(month, -6, CURRENT_DATE)
ORDER BY v.VISIT_TS DESC
LIMIT 200
```
If `SF_ACCOUNT_FOUND=false`: skip, record "No Leadfeeder data — account not in Salesforce."

**Query D — Opportunity history** (Airflow experience, competition, loss reasons):
```sql
SELECT
  o.OPP_NAME, o.CURRENT_STAGE_NAME, o.IS_WON, o.IS_LOST,
  o.LOSS_REASON, o.LOSS_DETAILS, o.COMPETITION, o.CLOUD_PROVIDER,
  o.AIRFLOW_COMMITMENT, o.AIRFLOW_EXPERIENCE,
  o.CURRENT_AIRFLOW_DEPLOYMENT_MODEL, o.CURRENT_AIRFLOW_VERSIONS,
  o.CURRENT_AIRFLOW_ENVIRONMENTS_COUNT, o.AIRFLOW_EXPERIENCE,
  o.CREATED_DATE, o.WON_DATE, o.LOST_DATE, o.TOTAL_ACV, o.NEW_BUSINESS_ACV,
  o.LEAD_SOURCE, o.DISCOVERY_MEETING_DATE
FROM HQ.MODEL_CRM.SF_OPPS o
WHERE o.ACCT_ID = '{SF_ACCT_ID}'
ORDER BY o.CREATED_DATE DESC
LIMIT 15
```
If `SF_ACCOUNT_FOUND=false`: skip, record "No opportunity history."

**Query E-synthesis — Gong cross-call account intelligence (parallel with B–D):**
```sql
SELECT
  KEY_THEMES, RECURRING_PAIN_POINTS, TECH_STACK_CONFIRMED,
  DEAL_RISK_TREND, RECOMMENDED_ANGLE, CALL_COUNT,
  TO_CHAR(DATE_RANGE_START, 'YYYY-MM-DD') AS DATE_RANGE_START,
  TO_CHAR(DATE_RANGE_END, 'YYYY-MM-DD') AS DATE_RANGE_END
FROM GTM.PUBLIC.GONG_ACCOUNT_ENRICHMENTS_V
WHERE ACCT_ID = '{SF_ACCT_ID}'
LIMIT 1
```
Single-row cross-call synthesis produced by Cortex. Use as the top-level Gong summary — `RECOMMENDED_ANGLE` feeds directly into AE brief framing. If no row: fall back to per-call enrichments only.

**Query E — Gong call enrichments (pre-computed Cortex signals, preferred):**
```sql
SELECT
  e.CALL_ID, e.ACCT_NAME, e.CALL_DATE,
  e.SENTIMENT_SCORE, e.DEAL_RISK,
  e.TECH_STACK, e.PAIN_POINTS, e.COMPETITORS, e.AIRFLOW_TOPICS,
  c.CALL_TITLE, c.CALL_URL, c.CALL_BRIEF, c.CALL_NEXT_STEPS,
  c.PRIMARY_EMPLOYEE, c.CALL_DURATION
FROM GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V e
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON c.CALL_ID = e.CALL_ID AND c.IS_DELETED = FALSE
WHERE e.ACCT_ID = '{SF_ACCT_ID}'
ORDER BY e.CALL_DATE DESC
LIMIT 20
```
Set `ENRICHMENTS_FOUND = true` if any rows returned. This replaces reading raw transcripts for all accounts in Joey's book.

**Query E-fallback — Raw Gong transcripts (only if ENRICHMENTS_FOUND=false):**
```sql
SELECT
  t.CALL_ID, t.CALL_TITLE, t.CALL_URL, t.SCHEDULED_TS,
  t.ACCT_NAME, t.OPP_NAME, c.OPP_STAGE_AT_CALL, c.CALL_DURATION,
  t.CALL_BRIEF, t.CALL_NEXT_STEPS, t.ATTENDEES,
  c.PRIMARY_EMPLOYEE, t.FULL_TRANSCRIPT
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE UPPER(t.ACCT_NAME) LIKE UPPER('%{COMPANY_NAME}%')
  AND c.IS_DELETED = FALSE
ORDER BY t.SCHEDULED_TS DESC
```
If count > 20: fetch metadata first (without `FULL_TRANSCRIPT`), then fetch transcripts in parallel batches of 10 CALL_IDs. If no results, try first word of company name or known abbreviations.

**Query F — Zendesk ticket enrichments (parallel with B–E-synthesis):**
```sql
SELECT
  e.TICKET_ID, e.TICKET_DATE, e.PRIORITY, e.STATUS,
  e.SENTIMENT_SCORE, e.ISSUE_CATEGORY, e.URGENCY_SIGNAL,
  e.KEY_PHRASES, e.PRODUCT_AREA
FROM GTM.PUBLIC.ZD_TICKET_ENRICHMENTS_V e
WHERE e.ACCT_ID = '{SF_ACCT_ID}'
ORDER BY e.TICKET_DATE DESC
LIMIT 30
```
If `SF_ACCOUNT_FOUND=false`: skip. If no rows: note "No support tickets found."

**Query G — Astro org / trial history (parallel with B–F):**
```sql
SELECT
  o.ORG_ID, o.ORG_NAME, o.ASTRO_ORG_STATE,
  o.FREE_TRIAL_START_DATE, o.TRIAL_EXPIRED_DATE,
  o.IS_GUIDED_TRIAL_ORG, o.TRIAL_REASON,
  o.AIRFLOW_COMMITMENT, o.AIRFLOW_PAIN,
  o.PROPENSITY_TO_PURCHASE,
  o.DEPLOYMENT_CREATED_DATE, o.FIRST_CODE_PUSH_DATE,
  o.FIRST_TASK_SUCCESS_DATE, o.FIRST_NON_EXAMPLE_DAG_DATE,
  o.CLICKED_INSTALL_CLI_BUTTON_DATE,
  o.ADDED_PAYMENT_METHOD_DATE,
  o.ASTRO_FREE_TRIAL_CREDIT_USAGE, o.ASTRO_FREE_TRIAL_CREDITS_ISSUED,
  o.FIRST_VIEWED_PRICING_PAGE_DATE, o.ASTRO_PLAN_UPGRADE_REQUEST,
  o.CREATED_TS, o.SF_RECORD_URL
FROM HQ.MODEL_CRM.SF_ASTRO_ORGS o
WHERE o.ACCT_ID = '{SF_ACCT_ID}'
ORDER BY o.CREATED_TS DESC
```
If `SF_ACCOUNT_FOUND=false`: skip. If no rows: note "No Astro org / trial history found."
Key fields to surface: `AIRFLOW_COMMITMENT` (self-reported in trial signup — highly reliable), `TRIAL_REASON`, `AIRFLOW_PAIN`, org state, whether they pushed real code and had task success, credit usage vs. issued (low usage = trial stalled).

**Query H — Campaign member history (parallel with B–F):**
```sql
SELECT
  cm.STATUS, cm.HAS_RESPONDED, cm.CREATED_TS, cm.FIRST_RESPONDED_TS,
  cm.JOB_TITLE, cm.COMPANY_OR_ACCOUNT,
  cm.WEBINAR_NAME, cm.FUNNEL_NAME, cm.EBOOK_NAME,
  cm.UTM_SOURCE, cm.UTM_CAMPAIGN,
  cm.MQL_QUALIFICATION_DATE, cm.ASSIGNED_AE_NAME, cm.ASSIGNED_SDR_NAME,
  cm.REPORTING_CHANNEL,
  c.CAMPAIGN_NAME, c.TYPE
FROM HQ.MODEL_CRM.SF_CAMPAIGN_MEMBERS cm
JOIN HQ.MODEL_CRM.SF_CAMPAIGNS c ON cm.CAMPAIGN_ID = c.CAMPAIGN_ID
WHERE cm.ACCT_ID = '{SF_ACCT_ID}'
ORDER BY cm.CREATED_TS DESC
LIMIT 30
```
If `SF_ACCOUNT_FOUND=false`: skip. If no rows: note "No campaign member history found."
Interpret results: webinars attended = active Airflow practitioner, ebooks downloaded = topic interest, free trial campaigns = prior product evaluation, pricing form fills = budget exploration. Note the campaign name verbatim — it reveals exactly what content resonated.

**Query H2 — ARR history 12 months (parallel with B–H, customers only):**
```sql
SELECT
  TO_CHAR(EOM_DATE, 'YYYY-MM') AS MONTH,
  PRODUCT, ARR_AMT, EXPANSION_AMT, DOWNSELL_AMT, CHURN_AMT, NEW_BUSINESS_AMT
FROM HQ.METRICS_FINANCE.CONTRACT_ARR_MONTHLY
WHERE ACCT_ID = '{SF_ACCT_ID}'
  AND EOM_DATE >= DATEADD('month', -12, CURRENT_DATE())
  AND ARR_AMT > 0
ORDER BY EOM_DATE
```
If no rows: omit ARR Trend section from report.

**Query H3 — Customer health snapshot (parallel with B–H, Astro customers only):**
```sql
SELECT
  ACCT_NAME, CONTRACTED_PRODUCT, TOTAL_ARR_AMT, DAYS_TO_RENEWAL,
  TO_CHAR(CONTRACT_END_DATE, 'YYYY-MM-DD') AS CONTRACT_END_DATE,
  USAGE_VS_CONTRACT_TARGET_PCT_30D, USAGE_GROWTH_PCT_30D,
  USAGE_AMT_30D, IS_3M_CONSECUTIVE_USAGE,
  LICENSE_CONSUMED_PCT, CREDIT_BALANCE,
  PROJECTED_OVERAGE_AMT_30D, PROJECTED_FULL_CREDIT_USE_DATE_30D,
  DEPLOYMENT_COUNT, ACTIVE_USER_COUNT_30D, USER_COUNT,
  IS_DOWNGRADE_RISK, ACCT_TAGS,
  SDM_COE, CUST_SUCCESS_MANAGER, FIELD_ENGINEER,
  PS_MIGRATION_STATUS, PS_MIGRATION_STATUS_SUMMARY
FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
WHERE ACCT_ID = '{SF_ACCT_ID}'
```
If no rows: account is not an active Astro customer — omit Customer Health section.

**Query H4 — Top operators by task volume (parallel with B–H, requires ORG_ID from Query G):**
```sql
SELECT OPERATOR, SUM(TASK_SUCCESS_COUNT) AS TASK_COUNT
FROM HQ.METRICS_ASTRO.DEPLOYMENT_OPERATOR_ACTIVITY_MULTI
WHERE ORG_ID = '{ORG_ID}'
  AND TIME_GRAIN = 'day'
  AND DATE >= DATEADD('day', -30, CURRENT_DATE())
GROUP BY OPERATOR
ORDER BY TASK_COUNT DESC
LIMIT 20
```
If no ORG_ID from Query G: skip. If empty: omit Product Usage section. Key operators to flag: `KubernetesPodOperator` (k8s sophistication), `ExternalTaskSensor` (cross-DAG scale), `TriggerDagRunOperator`, any AI/ML operators, custom operators.

**SF MCP Secondary Pass — Queries I, J, K (run AFTER Snowflake queries complete):**

> These three objects have no Snowflake equivalent. Only attempt if `SF_ACCOUNT_FOUND=true`. Run all three in parallel. **Skip the entire pass gracefully if SF MCP auth fails** (AuthDecryptError or similar) — note "SF MCP auth unavailable; re-run `sf org login web --alias joey` to restore." Do not block report generation on SF MCP.

**Query I — Inbound email history (SF MCP — no Snowflake equivalent):**

Use `mcp__salesforce__run_soql_query`:
```sql
SELECT Id, Subject, FromAddress, FromName, ToAddress, MessageDate, TextBody, Status
FROM EmailMessage
WHERE Incoming = true
  AND ActivityId IN (SELECT Id FROM Task WHERE WhatId = '{SF_ACCT_ID}' AND Type = 'Email')
ORDER BY MessageDate DESC
LIMIT 30
```
Also via `RelatedToId`:
```sql
SELECT Id, Subject, FromAddress, FromName, MessageDate, TextBody, Status
FROM EmailMessage
WHERE RelatedToId = '{SF_ACCT_ID}'
  AND Incoming = true
ORDER BY MessageDate DESC
LIMIT 30
```
Combine and deduplicate by `Id`. Store as `EMAIL_HISTORY`. If empty: note "No inbound email history found in Salesforce."

**Query J — Opportunity contact roles (SF MCP — no Snowflake equivalent):**

Use `mcp__salesforce__run_soql_query`:
```sql
SELECT Role, IsPrimary, Contact.Name, Contact.Title, Contact.Email, Opportunity.Name, Opportunity.StageName, Opportunity.CloseDate
FROM OpportunityContactRole
WHERE Opportunity.AccountId = '{SF_ACCT_ID}'
ORDER BY Opportunity.CloseDate DESC
LIMIT 30
```
If empty: note "No opportunity contact roles found." Key signal: IsPrimary=true + Role="Decision Maker" or "Economic Buyer" = budget owner.

**Query K — Activity / task history (SF MCP — no Snowflake equivalent):**

Use `mcp__salesforce__run_soql_query`:
```sql
SELECT Subject, Description, ActivityDate, Status, Type, Who.Name, Who.Title, Owner.Name, CreatedDate
FROM Task
WHERE WhatId = '{SF_ACCT_ID}'
  AND IsDeleted = false
ORDER BY ActivityDate DESC NULLS LAST
LIMIT 30
```
If empty: note "No logged activity history found." Filter out automated Type='Email' tasks — focus on Type='Call', 'Meeting', or non-trivial Description.

**Query L — Account + contact notes + prior research (Snowflake — GTM.PUBLIC, parallel with B–H):**

```sql
SELECT NOTE_ID, NOTE_DATE, NOTE_TYPE, CONTENT, SOURCE, CREATED_AT
FROM GTM.PUBLIC.ACCOUNT_NOTES
WHERE ACCT_ID = '{SF_ACCT_ID}'
ORDER BY NOTE_DATE DESC
LIMIT 30
```

```sql
SELECT NOTE_ID, CONTACT_NAME, NOTE_DATE, NOTE_TYPE, CONTENT, SOURCE, CREATED_AT
FROM GTM.PUBLIC.CONTACT_NOTES
WHERE ACCT_ID = '{SF_ACCT_ID}'
ORDER BY NOTE_DATE DESC
LIMIT 30
```

```sql
SELECT RESEARCH_DATE, SCORE, GRADE, CONFIDENCE, MC_GRADE, DAYS_SINCE_RESEARCH, IS_STALE
FROM GTM.PUBLIC.ACCOUNT_RESEARCH_LATEST_V
WHERE ACCT_ID = '{SF_ACCT_ID}'
```

Combine all three. If `SF_ACCOUNT_FOUND=false`: skip. If notes empty: note "No account/contact notes found in GTM."
Store prior research result as `PRIOR_RESEARCH` (score, grade, confidence, mc_grade, research_date, is_stale). Use in Step 6 changelog diff — compare new score/grade against `PRIOR_RESEARCH` values instead of parsing the local file.
These are Joey's primary interaction log (pre-call briefs, email drafts, meeting summaries) — richer and more reliable than native SF notes.

**Apollo pre-fetch** (parallel with B–F, skip if no key):
```bash
source ~/.zshrc && curl -s -X POST "https://api.apollo.io/v1/accounts/search" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\": \"$APOLLO_API_KEY\", \"q_organization_name\": \"{COMPANY_NAME}\", \"per_page\": 10}" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for a in data.get('accounts', []):
    if '{DOMAIN}'.lower() in (a.get('domain') or '').lower():
        print(f'APOLLO_ID={a[\"id\"]}')
        break
else:
    print('APOLLO_ID=null')
"
```

### Step 3: Research Depth

All accounts always get FULL research depth. Proceed directly to Step 4.

> Note: HG_AIRFLOW, DATAFOX_AIRFLOW, APACHE_AIRFLOW_ROLES, and EVIDENCE_OF_AIRFLOW are unreliable and must not be used for stack confirmation.

### Step 4: Targeted Web Research

Launch a **single web research agent** to run all 7 research items below.

**Context to pass to the agent from Step 2:**
- CRM status, opp history, contact intent signals, any Airflow mentions from Gong discovery. Do NOT pass HG/DataFox/CF stack signals — agent must independently confirm stack via web.

**Use Claude built-in tools for all web research:**
- `WebSearch` — all web searches (standard, date-filtered, domain-restricted)
- `WebFetch` — fetch specific URLs for full page content

Run all 7 searches in parallel. Each search uses `WebSearch` with `max_uses: 2` (two search-and-summarize passes per query). Then run Sumble enrichment as a post-step.

**`FROM_DATE`** = today minus 35 days (ISO format, e.g. `2026-05-19`).

1. **Recent news** — last 35 days only:
   ```
   WebSearch('What is the latest news about "{COMPANY_NAME}" (domain: {DOMAIN}) in the last 35 days? Focus on funding rounds, product launches, leadership changes, or major partnerships. Only return results about this specific company. Date range: after {FROM_DATE}.')
   ```
   After results, run `_filter_to_company` (entity filter — see Step 4b).

2. **Tech stack — first-party evidence** (engineering blogs, GitHub, conference talks):
   ```
   WebSearch('Find engineering blog posts, GitHub repositories, data conference talks, or case studies where {COMPANY_NAME} employees describe their own data infrastructure or workflow orchestration tooling. Their website is {DOMAIN}. I want first-person evidence of what tools they actually run in production today. Include orchestration tools (Airflow, Prefect, Dagster, Temporal), transformation tools (dbt), and workflow automation (n8n, Zapier, Make, Workato, Clay). Not a different company with a similar name.')
   ```

3. **Tech stack — hiring evidence** (present-tense stack language in job postings):
   ```
   WebSearch('Find job postings from {COMPANY_NAME} (domain: {DOMAIN}) for data engineering, platform engineering, ML, finance systems, or RevOps roles that describe their existing technology stack. Look for present-tense language: "our stack includes", "you will work with our existing", or specific tool names in responsibilities. Only results from this specific company.')
   ```

4. **AI / agentic stack** (LLM pipelines, agent frameworks):
   ```
   WebSearch('Find evidence that {COMPANY_NAME} (domain: {DOMAIN}) is building or running AI agents, LLM pipelines, or agentic workflows. Look for: LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, Langfuse, LangSmith, Weights & Biases, MLflow, Vertex AI, Bedrock Agents, OpenAI Assistants, or any orchestration of LLM calls in production. First-person employee evidence preferred. Not a different company with a similar name.')
   ```
   After results, run entity filter.

5. **Workflow automation / competitor orchestration / finance automation**:
   ```
   WebSearch('Find evidence that {COMPANY_NAME} (domain: {DOMAIN}) is using workflow automation or no-code/low-code orchestration tools: n8n, Zapier, Make, Workato, Clay, Retool, Tray.io, Boomi, MuleSoft. Also look for finance automation: Workiva, Anaplan, Planful, month-end close automation, FP&A reporting pipelines, reconciliation workflows. Also look for competitor orchestration: Prefect, Dagster, Temporal, Argo Workflows, Kubeflow Pipelines. First-person employee evidence or job postings only. Not a different company with a similar name.')
   ```
   After results, run entity filter.

6. **Engineering blog** — discovery + fetch:
   ```
   WebSearch('site:{DOMAIN} engineering blog OR data blog after:{FROM_DATE}')
   ```
   (If no domain: `WebSearch('"{COMPANY_NAME}" engineering blog OR data blog after:{FROM_DATE}')`)
   `WebFetch` on top 1-2 post URLs. After results, run entity filter.

7. **M&A signals**:
   ```
   WebSearch('"{COMPANY_NAME}" {DOMAIN} merger OR acquisition OR investment OR bankruptcy OR acquired OR "went public" after:{FROM_DATE}')
   ```
   Determine M&A STATUS: ACQUIRED / MERGER / IPO / BANKRUPTCY / SHUTDOWN / NONE FOUND. Run entity filter.

**Step 4b: Entity filtering and tech stack classification**

After all 7 searches complete:

- For `news`, `engineering_blog`, `ma_signals`, `ai_stack`, `workflow_automation`: filter out sentences/paragraphs that aren't about {COMPANY_NAME} (not a different company with a similar name). If everything filters out, record `(no relevant results)`.
- For `tech_stack_firstparty` + `tech_stack_hiring` + `ai_stack` + `workflow_automation`: classify all technology claims into:
  - **CONFIRMED** — company's own blog/GitHub/recorded talk says they run this tool in production today; OR vendor case study with a named employee quote
  - **SIGNAL** — job posting implying the tool; hiring language without present-tense ownership; evaluating/piloting language
  - **NEGATIVE** — moved away from or evaluated but didn't adopt
  - **IGNORE** — tangential mention; different company; tool mentioned as an alternative they didn't choose

  Apply these rules when writing the Tech Stack section:
  - CONFIRMED → write as fact with source: `Apache Airflow ✓ (company blog, 2026-03-10)`
  - SIGNAL → write as `Apache Airflow — hiring signal (job posting, 2026-05-01)` — NEVER "uses X"
  - NEGATIVE → note what they moved away from
  - Never write "uses X", "likely uses", or "may use" without CONFIRMED evidence

**Step 4c: Sumble enrichment (after web research, before report generation)**

Call Sumble to fill technology gaps not confirmed by web research.

- **Skip Sumble enrich** if web research already CONFIRMED critical technologies (Airflow, dbt, Prefect, Dagster, Temporal, Argo, Kubeflow, LangChain, LangGraph, MLflow, Spark, Kafka) — only call Sumble jobs endpoint for gap technologies.
- **Full Sumble enrich** if web research returned no CONFIRMED tech for those tools — call the enrich endpoint for tech stack + project type signals, then jobs for gap technologies only.

Sumble signal interpretation: treat Sumble tech stack items as **SIGNAL** evidence (equivalent to a hiring signal, not confirmed use). Source tag: `(Sumble)`.

**Workflow automation hiring signals** — treat any of the following as a positive Astronomer fit signal, even without an explicit Airflow mention:
- Roles titled **"AI Ops"**, **"AI Operations"** (any function) → building automated AI workflows at scale
- Roles titled **"GTM Engineer"** or **"Revenue Engineer"** → automating sales/marketing pipelines
- Job descriptions mentioning **Clay, n8n, Zapier, Make, Workato, Tray.io** → workflow complexity graduating to Airflow

**ATS direct lookup (primary hiring signal source, runs in parallel with web research):**

Before or alongside web searches, attempt to detect the company's ATS and fetch job listings directly via API:

1. Check Snowflake cache (`ACCOUNT_ATS_CACHE`) — if hit within 30 days, use cached provider/slug
2. HTTP crawl common careers paths (`/careers`, `/jobs`, `/careers/jobs`, `/company/careers`, `/about/careers`, `/join`) and scan HTML for ATS embed links
3. Slug-guess against Greenhouse, Lever, Ashby, Workable, Recruitee APIs using `{DOMAIN}.split('.')[0]`
4. If Playwright is available and all above fail, use headless Chromium on careers page

Supported ATS with direct API: Greenhouse, Lever, Ashby, Workable, BambooHR, SmartRecruiters, Rippling, Recruitee, Jobvite, Workday, iCIMS, TeamTailor, Personio.

Filter fetched jobs to data/engineering/analytics/finance-systems/RevOps roles. Flag roles mentioning Airflow, orchestration, dbt, dagster, prefect, temporal with 🔥. If ATS returns fewer than 3 data roles, also run a LinkedIn/Glassdoor web search fallback.

If no ATS detected: fall back to LinkedIn/Glassdoor/Indeed web search for hiring signals.

### Step 5: Generate Report Directly

Read both prompt templates:
- `~/claude-work/research-assistant/prompts/01_fit_scoring.md`
- `~/claude-work/research-assistant/prompts/02_account_research.md`

**Delta model**: if a prior report exists in `PRIOR_RESEARCH` (from Query L), pass it as the baseline and instruct the model to only rewrite sections with materially new information. On first run, generate a full initial report.

**Session continuity**: The DAG persists Anthropic message history per account in `GTM.PUBLIC.JK_SEQUENCER_ACCOUNT_SESSIONS`. For interactive use, treat each run as a fresh session (no prior messages) unless you have explicit prior context.

**Do not assemble a RAW INTELLIGENCE intermediate block.** Feed all data directly into a single generation pass:

**Context to the model** (in this order for cache efficiency):
1. Fit scoring rubric (from `~/claude-work/research-assistant/prompts/01_fit_scoring.md`)
2. AE brief template (from `~/claude-work/research-assistant/prompts/02_account_research.md`)
3. Snowflake data block (structured, labeled by source table)
4. Web research findings + Sumble enrichment

**Snowflake data block format** (compact, structured):
```
=== SNOWFLAKE: SF_ACCOUNTS ===
CRM status: {IS_CURRENT_CUST / IS_CHURNED_CUST / prospect}
Owner: {OWNER_NAME} | Region: {SALES_REGION} | Segment: {SEGMENT_PLANNED}
Industry: {INDUSTRY} | Country: {BILLING_COUNTRY}
ICP: {ICP_DESIGNATION_V2} | Acct Score: {ACCT_SCORE} ({ACCT_SCORE_POSITIVE_DRIVERS} / {ACCT_SCORE_NEGATIVE_DRIVERS})
Smoke: {SMOKE_SCORE} | Fire: {FIRE_SCORE}
Last MQL: {LAST_MQL_DATE} | Cosmos doc: {LAST_COSMOS_DOC_VIEW_DATE} | DAG factory: {LAST_DAG_FACTORY_DOWNLOAD_DATE}

=== SNOWFLAKE: SF_CONTACTS (top contacts by recency) ===
[For each contact: Title | Lead score | Pricing page visit: {date or none} | Airflow debug visit: {date or none} | DAG debug visit: {date or none} | MQL: {date or none} | Opted out: {yes/no}]

=== SNOWFLAKE: LF_WEBSITE_VISITS ===
[Total visits (last 6mo): N | First: {date} | Last: {date}]
[Page list: URL | date | duration — flag /pricing, /demo, /astro, /trial as HIGH intent]
[If none: "No Leadfeeder visits — not matched in Salesforce or no visits."]

=== SNOWFLAKE: SF_OPPS ===
[For each opp: Name | Stage | Won/Lost | ACV | Created | Close date]
[Loss reason: {LOSS_REASON} — {LOSS_DETAILS}]
[Competition: {COMPETITION}]
[Airflow experience: {AIRFLOW_EXPERIENCE} | Deployment model: {CURRENT_AIRFLOW_DEPLOYMENT_MODEL} | Versions: {CURRENT_AIRFLOW_VERSIONS} | Env count: {CURRENT_AIRFLOW_ENVIRONMENTS_COUNT}]
[Cloud provider: {CLOUD_PROVIDER}]

=== SNOWFLAKE: GONG_ACCOUNT_ENRICHMENTS (cross-call synthesis) ===
[Found / Not found]
[Key themes: {KEY_THEMES}]
[Recurring pain points: {RECURRING_PAIN_POINTS}]
[Confirmed tech stack: {TECH_STACK_CONFIRMED}]
[Deal risk trend: {DEAL_RISK_TREND}]
[Recommended angle: {RECOMMENDED_ANGLE}]
[Call count: {CALL_COUNT} | Date range: {DATE_RANGE_START} → {DATE_RANGE_END}]

=== SNOWFLAKE: GONG_CALL_ENRICHMENTS (per-call Cortex signals) ===
[Found N enriched calls / No enrichments — falling back to raw transcripts]
[Per call: Date | Sentiment: {score} | Deal risk: {low/medium/high} | Tech stack | Pain points | Competitors | Airflow topics | Brief | Next steps]

=== SNOWFLAKE: ZD_TICKET_ENRICHMENTS (support health signals) ===
[Found N enriched tickets / No tickets]
[Per ticket: Date | Priority | Status | Sentiment: {score} | Urgency: {signal} | Category | Product area | Key phrases]
[If none: "No support tickets for this account."]

=== SNOWFLAKE: SF_ASTRO_ORGS (trial / product history) ===
[Found N orgs / No Astro org history]
[For each org: Org name | State: {ASTRO_ORG_STATE} | Trial: {FREE_TRIAL_START_DATE} → {TRIAL_EXPIRED_DATE}]
[Self-reported at signup: Airflow commitment: {AIRFLOW_COMMITMENT} | Trial reason: {TRIAL_REASON} | Airflow pain: {AIRFLOW_PAIN}]
[Product milestones: Deployment created: {date} | Code pushed: {date} | Task success: {date} | Own DAG: {date} | Payment method: {date or none}]
[Credit usage: {ASTRO_FREE_TRIAL_CREDIT_USAGE} of {ASTRO_FREE_TRIAL_CREDITS_ISSUED} issued | Propensity to purchase: {score}]
[If none: "No Astro org or trial history found."]

=== SNOWFLAKE: SF_CAMPAIGN_MEMBERS (marketing interaction history) ===
[Found N campaign interactions / No campaign history]
[Chronological list, newest first: Date | Campaign name | Type | Status | Responded: yes/no | Job title at time | UTM campaign]
[Flag by type: Free Trial = prior product evaluation | Pricing = budget exploration | Webinar (Attended) = active practitioner | Ebook (Responded) = topic interest | Webinar (Registered, not attended) = weak signal]
[If none: "No campaign member history found."]

=== SNOWFLAKE: GONG_CALL_TRANSCRIPTS (raw fallback — only if no enrichments) ===
[Found N calls / No prior calls — cold outreach]
[For each call: Date | Participants | Brief | Next steps | Full transcript]

=== SNOWFLAKE: ARR HISTORY (CONTRACT_ARR_MONTHLY, 12 months) ===
[Found N months / No ARR data — prospect or not yet a customer]
[Per month: Month | Product | ARR_AMT | Expansion | Downsell | Churn | New Business]
[Call out any month with EXPANSION_AMT > 0 or DOWNSELL_AMT < 0 explicitly]
[If none: omit ARR Trend section from report]

=== SNOWFLAKE: CUSTOMER HEALTH SNAPSHOT (CURRENT_ASTRO_CUSTS) ===
[Found / No data — not an active Astro customer]
[Usage vs target (30d): {USAGE_VS_CONTRACT_TARGET_PCT_30D}% | Growth: {USAGE_GROWTH_PCT_30D}%]
[Credit balance: {CREDIT_BALANCE} | Projected overage: {PROJECTED_OVERAGE_AMT_30D}]
[Projected full credit use: {PROJECTED_FULL_CREDIT_USE_DATE_30D}]
[Deployments: {DEPLOYMENT_COUNT} | Active users (30d): {ACTIVE_USER_COUNT_30D} | Total users: {USER_COUNT}]
[Downgrade risk: {IS_DOWNGRADE_RISK} | Tags: {ACCT_TAGS}]
[CoE: {SDM_COE} | CSM: {CUST_SUCCESS_MANAGER} | FE: {FIELD_ENGINEER}]
[PS migration: {PS_MIGRATION_STATUS} — {PS_MIGRATION_STATUS_SUMMARY}]
[Label each signal 🟢/🟡/🔴 in report]

=== SNOWFLAKE: TOP OPERATORS (DEPLOYMENT_OPERATOR_ACTIVITY_MULTI, last 30 days) ===
[Found N operators / No operator data — no Astro org or org not active]
[Per operator: Operator name | Total task count]
[Flag: KubernetesPodOperator = k8s sophistication | ExternalTaskSensor = cross-DAG scale | TriggerDagRunOperator | custom operators | AI/ML operators]
[If empty: omit Product Usage section]

=== SF EMAIL: INBOUND EMAIL HISTORY (Salesforce MCP — EmailMessage, Incoming=true) ===
[Found N inbound emails / No inbound email history]
[Per email: Date | From: {name} <{email}> | Subject | Body preview (first 300 chars)]
[If none: "No inbound email history found in Salesforce."]

=== SF CRM: OPPORTUNITY CONTACT ROLES (Salesforce MCP — OpportunityContactRole) ===
[Found N contact roles / No contact roles found]
[Per role: Contact name | Title | Email | Role | IsPrimary | Opp name | Stage | Close date]
[Flag: IsPrimary=true + Role=Decision Maker/Economic Buyer = budget owner]
[If none: "No opportunity contact roles found."]

=== SF CRM: ACTIVITY / TASK HISTORY (Salesforce MCP — Task) ===
[Found N tasks / No logged activity]
[Per task: Date | Type | Subject | Owner (Astronomer rep) | Who (contact) + title | Description]
[Skip automated sequence emails — surface manually logged calls, meetings, notes]
[If none: "No logged activity history found in Salesforce."]

=== SNOWFLAKE: ACCOUNT_NOTES + CONTACT_NOTES (GTM.PUBLIC) ===
[Found N account notes / N contact notes / No notes found]
[Per note: Date | Type | Source | Content preview]
[If none: "No account/contact notes found in GTM — no prior interactions logged."]
```

In a single generation pass, produce:
1. Fit score section (using rubric from template 1)
2. Full AE brief (using template 2)

**Web research block** (after Snowflake data block):
```
=== WEB RESEARCH: HIRING SIGNALS (ATS direct or web search fallback) ===
{hiring signals formatted output}

=== WEB RESEARCH: NEWS & FUNDING ===
{news}

=== WEB RESEARCH: TECH STACK EVIDENCE (classified) ===
{classified CONFIRMED/SIGNAL/NEGATIVE claims}

=== WEB RESEARCH: AI / AGENTIC STACK ===
{ai_stack filtered text}

=== WEB RESEARCH: WORKFLOW AUTOMATION / COMPETITOR ORCHESTRATION / FINANCE AUTOMATION ===
{workflow_automation filtered text}

=== WEB RESEARCH: SUMBLE ACCOUNT INTELLIGENCE ===
{sumble_enrichment}

=== WEB RESEARCH: ENGINEERING BLOG ===
{engineering_blog}

=== WEB RESEARCH: M&A SIGNALS ===
{ma_signals}
```

The fit scoring rubric uses tags `[EXA]`, `[LF]`, `[CR]` — map these to `[WEB]`, `[SF-LF]`, `[SF-CR]` respectively when Snowflake is the source.

### Step 6: Compose Final Report

Generate slug: lowercase, spaces → underscores, remove special chars. Check for collision.

Check for existing report at `~/claude-work/research-assistant/outputs/accounts/{SLUG}/report.md`. If found, extract prior score/grade and generate changelog entry if:
- Score changed ≥2 points, grade letter changed
- New LF visits to /pricing, /demo, /astro, /trial
- New SF_CONTACTS pricing page or Airflow debug visits
- New hiring signals mentioning Airflow/orchestration, AI Ops, GTM Engineer, or workflow automation tools (Clay, n8n, Zapier, Make, Workato)
- M&A event detected
- Opp stage changed
- Signal lost (job posting filled, contact departed, HG signal dropped)

```markdown
# Account Research Report: {COMPANY_NAME}

**Generated**: {TODAY_DATE}
**Website**: https://{DOMAIN}
**Sources**: Snowflake (SF_ACCOUNTS ✓/✗ | LF_VISITS ✓/✗ | SF_OPPS ✓/✗ | Gong ✓/✗ | Astro Orgs ✓/✗ | Campaigns ✓/✗) | SF Email ✓/✗ | Claude Web Search ✓

[If M&A STATUS ≠ NONE FOUND:]
> **M&A ALERT: {M&A STATUS}**
> {1-2 sentence impact on outreach}

---
[Fit Score section]

[Account at a Glance — always present, immediately after Fit Score]
**Existing customers**: ARR | Contract End (days to renewal) | Product Tier | AE/CSM/FE | Downgrade Risk | Cloud/Region
**Prospects**: CRM Status | Acct Score (positive/negative drivers) | ICP | Owner

[Overall Assessment — always present, immediately after Account at a Glance]
**Strengths**: 2–4 bullets
**Risks**: 2–4 bullets
**Bottom Line**: 1 sentence

---
[AE Brief section]
---
[Renewal Risk — customers only, from H3 data]
[Feature Adoption — customers only, from H4 operator data]
---
## Changelog
### {TODAY_DATE}
- [change or "First research generated. Grade: {GRADE}, Score: {SCORE}/20, Confidence: {CONFIDENCE}"]
[prior entries preserved, newest first]
```

### Step 7: Save Report

```bash
mkdir -p ~/claude-work/research-assistant/outputs/accounts/{SLUG}/
```
Overwrite: `~/claude-work/research-assistant/outputs/accounts/{SLUG}/report.md`

### Step 8a: Update Apollo

Skip if no `APOLLO_API_KEY`. Use `APOLLO_ID` from Step 2 pre-fetch if found; otherwise search by name + confirm by domain.

```bash
source ~/.zshrc
APOLLO_REPORT=$(python3 -c "
import re, sys
content = open(sys.argv[1]).read()
if len(content) <= 60000:
    print(content); exit(0)
truncated = re.sub(r'(### Full Transcripts\n).*', r'\1[Truncated — see local report.md]', content, flags=re.DOTALL)
if len(truncated) > 60000:
    truncated = truncated[:60000] + '\n\n[Truncated at 60,000 chars for Apollo]'
print(truncated)
" ~/claude-work/research-assistant/outputs/accounts/{SLUG}/report.md)

RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X PUT "https://api.apollo.io/v1/accounts/{APOLLO_ID}" \
  -H "Content-Type: application/json" \
  -d "{\"api_key\": \"$APOLLO_API_KEY\", \"typed_custom_fields\": {\"6998b33edacda9000deb48ca\": $(echo "$APOLLO_REPORT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' )}}")
HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
[ "$HTTP_STATUS" = "200" ] && echo "Apollo: write succeeded" || echo "Apollo: write FAILED — HTTP $HTTP_STATUS"
```

### Step 8b: Sync to Snowflake

Always run this step — it is not conditional on Apollo success. Extract score/grade/confidence/mc_grade directly from the values computed during Step 5 (do not parse the markdown). Build a sources JSON from which queries returned data.

```bash
source ~/.zshrc && /Users/joeykenney/.venvs/snowflake/bin/python3 \
  ~/claude-work/scripts/write_account_research.py \
  --acct-id       "{SF_ACCT_ID}" \
  --acct-name     "{COMPANY_NAME}" \
  --score         {SCORE} \
  --grade         {GRADE} \
  --confidence    {CONFIDENCE} \
  --mc-grade      {MC_GRADE} \
  --sources       '{{"sf_accounts": {SF_ACCOUNT_FOUND}, "lf_visits": {LF_VISITS_FOUND}, "sf_opps": {OPPS_FOUND}, "gong": {GONG_FOUND}, "astro_orgs": {ASTRO_ORGS_FOUND}, "campaigns": {CAMPAIGNS_FOUND}, "web": true, "apollo": {APOLLO_ID_FOUND}}}' \
  --sources-ok    '{SOURCES_OK_JSON}' \
  --sources-failed '{SOURCES_FAILED_JSON}' \
  --runtime-s     {RUNTIME_SECONDS} \
  --report-file   ~/claude-work/research-assistant/outputs/accounts/{SLUG}/report.md
```

Where:
- Each `{X_FOUND}` is `true` or `false` based on whether that query returned rows.
- `{SOURCES_OK_JSON}` is a JSON array of strings for sources that returned data, e.g. `'["snowflake","gong","apollo","web"]'`
- `{SOURCES_FAILED_JSON}` is a JSON array of strings for sources that failed/were unavailable, e.g. `'["salesforce_mcp"]'` (empty array `'[]'` if all sources succeeded)
- `{RUNTIME_SECONDS}` is elapsed wall-clock time from research start to now (integer)
- If `SF_ACCOUNT_FOUND=false`, use `""` for `--acct-id` — the script will still insert (ACCT_ID will be empty — acceptable for new prospects not yet in SF).

Log result: `Snowflake: write succeeded` or `Snowflake: write FAILED — {error}`. Do not block Step 9 on failure.

### Step 9: Present Results

If M&A STATUS ≠ NONE FOUND, output this first before anything else:
```
⚠️  M&A ALERT: {COMPANY_NAME}
{M&A STATUS} — {date}
{Plain-English: what happened, what the rep should do next.}
Source: {URL}
```

Then display the full report. Highlight fit score/grade, top buying signals, and changelog if re-run.

---

### Step 10: Post-Research Action Item Extraction

After the report is displayed, scan the completed report and the data collected during research for any of these triggers. Run this step automatically — do not wait to be asked.

| Trigger | Detection Condition | Draft Type | Note Type |
|---------|---------------------|------------|-----------|
| **Cost spike** | `USAGE_VS_CONTRACT_TARGET_PCT_30D > 110` in ACCOUNT_360_V | Customer cost conversation email | `email_draft` |
| **Bounced emails** | Any contact with `CONTACT_STATUS = 'Bounced'` or bounce signals in SF | Internal note: "Update contact info — bounced emails detected" | `ad_hoc` |
| **Trial expiry** | `ASTRO_ORG_STATE = 'trial'` and `TRIAL_EXPIRED_DATE` within 14 days | Trial-to-paid outreach email | `email_draft` |
| **M&A signal** | M&A STATUS ≠ NONE FOUND in web research | Internal flag note to CSM/AE re: deal routing | `ad_hoc` |
| **Churn risk** | Gong `LAST_GONG_SENTIMENT < -0.3` AND low usage (< 50% of contract target) in ACCOUNT_360_V | Internal escalation note | `ad_hoc` |
| **Bankruptcy / shutdown** | Bankruptcy or shutdown detected in web research | Disqualification note + internal alert | `ad_hoc` |

For **each trigger found**:

1. Draft the appropriate message (1–3 sentences for internal notes, 80–120 words for customer-facing emails).
2. Write to Snowflake:

```bash
source ~/.zshrc && /Users/joeykenney/.venvs/snowflake/bin/python3 \
  ~/claude-work/scripts/write_account_note.py \
  --acct-id   "{SF_ACCT_ID}" \
  --acct-name "{COMPANY_NAME}" \
  --note-type {email_draft|ad_hoc} \
  --source    claude \
  --content   "ACTION ITEM [{TRIGGER_TYPE}] — Urgency: {immediate|this-week|monitoring}

{DRAFT_TEXT}"
```

3. Display each action item after the main report:

```
--- ACTION ITEMS ---
[{TRIGGER_TYPE}] Urgency: {URGENCY}
{DRAFT_TEXT}
Saved to: ACCOUNT_NOTES
```

If no triggers are found, output a single line: `No action items triggered.`

**Do not generate action items for triggers where the supporting data wasn't available** (e.g., don't generate a churn risk note if ACCOUNT_360_V returned no usage data).

---

## BATCH MODE

### Batch Step 1: Load CSV
Columns: `company_name`, `domain`. Flexible with header names. Detect `force` flag.

### Batch Step 2: Bulk Snowflake Pre-fetch

**Skip the Leadfeeder MCP entirely.** Instead, pull SF_ACCOUNTS + LF data for all companies in a single query batch before spawning any subagents.

For each company, generate its slug and check for existing valid report (skip if complete and not force mode).

For the NEEDS_RUN companies, run one batch Snowflake query:
```sql
SELECT
  a.ACCT_ID, a.ACCT_NAME, a.ACCT_DOMAIN, a.ACCT_TYPE, a.ACCT_STATUS,
  a.IS_CURRENT_CUST, a.ICP_DESIGNATION_V2, a.ACCT_SCORE,
  a.SMOKE_SCORE, a.FIRE_SCORE, a.LAST_MQL_DATE,
  a.INDUSTRY, a.OWNER_NAME, a.BILLING_COUNTRY
FROM HQ.MODEL_CRM.SF_ACCOUNTS a
WHERE LOWER(a.ACCT_DOMAIN) IN ({comma-separated lowercased domains})
  AND a.ACCT_TYPE NOT IN ('Internal', 'Competitor')
```
This provides `SF_ACCT_ID` for the individual queries.

Also check Gong call counts for all companies in one query:
```sql
SELECT t.ACCT_NAME, COUNT(*) AS call_count
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE c.IS_DELETED = FALSE
  AND UPPER(t.ACCT_NAME) IN ({comma-separated uppercased names})
GROUP BY t.ACCT_NAME
```

### Batch Step 3: Process Companies (Groups of 5 Simultaneous Subagents)

For each group of up to 5 companies, spawn all subagents simultaneously.

Each subagent task must embed the full Step 2–7 instructions inline (substituting all variables). Pass the pre-fetched Snowflake summary for that company so the subagent can skip Query A (already done) and go straight to Queries B–E.

Key subagent instructions:
- `SF_ACCT_ID` is provided — skip Query A, use it directly for B–E
- All accounts use FULL research depth — run all 7 web research items
- Skip Steps 8a, 8b, and 9 (Apollo, Snowflake, display) — orchestrator handles these
- When finished respond with only: `"{COMPANY_NAME} complete"` or `"{COMPANY_NAME} error: [reason]"`
- Do NOT return the report in the response

**Verify each report** after subagent responds:
```bash
python3 -c "
import os, sys
path = os.path.expanduser('~/claude-work/research-assistant/outputs/accounts/{SLUG}/report.md')
if not os.path.exists(path): print('FAIL: file missing'); exit(1)
content = open(path).read()
missing = [s for s in ['# Account Research Report:', '**Generated**:', '**Sources**:'] if s not in content]
if missing or len(content) < 2000: print(f'FAIL: {missing or \"too short\"}'); exit(1)
print('OK')
" 2>&1
```

Retry once on failure. If still failing, mark FAILED and continue.

**Apollo sync** (orchestrator, after each verification OK):
Use Step 8a with substituted variables. Log result.

**Snowflake sync** (orchestrator, after each verification OK):
Use Step 8b with substituted variables. Log result.

**Append to batch run log**:
```
{TIMESTAMP} | {COMPANY_NAME} | {DOMAIN} | SUCCESS/FAILED | Apollo: ok/failed/skipped | Snowflake: ok/failed
```

Pause 2 seconds between groups. For >50 companies: chunks of 50, pause 10 seconds between chunks.

### Batch Step 4: Batch Summary

Write `~/claude-work/research-assistant/outputs/batch_summary.csv`:
```csv
company,domain,score,grade,confidence,score_change,key_change,research_depth,report_path,last_updated
```

Display: total processed / succeeded / failed, grade distribution, top 10 by score.

For any M&A alerts found across the batch:
```
--- M&A ALERTS ---
- Acme Corp — ACQUIRED by BigCo (March 2025) — may need re-routing
```

For failed companies, write `failed_rerun.csv` and display remediation block.

---

## Graceful Degradation

| Source | Failure Behavior |
|--------|-----------------|
| **SF_ACCOUNTS not found** | RESEARCH_DEPTH=FULL by default; skip Queries B–D; note "New prospect — not yet in Salesforce" |
| **LF_WEBSITE_VISITS empty** | Note "No Leadfeeder visits recorded" — do not attempt Leadfeeder MCP |
| **SF_OPPS empty** | Note "No opportunity history" — cold outreach confirmed |
| **Gong enrichments (no rows)** | Fall back to Query E-fallback (raw transcripts); note "Enrichments not available — using raw transcripts" |
| **Gong (no calls)** | Note "No prior calls — cold outreach" |
| **Web search (no results)** | Note per section; reduce confidence |
| **SF_ASTRO_ORGS empty** | Note "No Astro org or trial history found" — treat as no prior product evaluation |
| **SF_CAMPAIGN_MEMBERS empty** | Note "No campaign history found" — cold from a marketing perspective |
| **GTM.PUBLIC.ACCOUNT_NOTES / CONTACT_NOTES empty** | Note "No account/contact notes found in GTM" — normal for new prospects |
| **GONG_ACCOUNT_ENRICHMENTS_V empty** | Fall back to per-call enrichments only; omit cross-call synthesis section |
| **CONTRACT_ARR_MONTHLY empty** | Omit ARR Trend section — prospect or pre-revenue customer |
| **CURRENT_ASTRO_CUSTS empty** | Omit Customer Health section — not an active Astro customer |
| **DEPLOYMENT_OPERATOR_ACTIVITY_MULTI empty / no ORG_ID** | Omit Product Usage section |
| **Sumble API unavailable / no match** | Skip Sumble enrichment; note "(Sumble: not available)" in Tech Stack section |
| **ATS not detected** | Fall back to LinkedIn/Glassdoor/Indeed web search for hiring signals |
| **SF MCP auth failure (AuthDecryptError)** | Skip Queries I–K entirely; note "SF MCP auth expired — run `sf org login web --alias joey` to restore"; do NOT block report generation |
| **SF EmailMessage (no rows)** | Note "No inbound email history found in Salesforce" — do not error; email logging may not be enabled |
| **SF OpportunityContactRole (no rows)** | Note "No opportunity contact roles found" — common on older opps |
| **SF Task (no rows)** | Note "No logged activity history found" — reps may not log activities manually |
| **Apollo** | Skip write-back; report saves locally |
| **Common Room** | Note "Common Room not available"; SF_CONTACTS covers contact intent signals |

**Do NOT fall back to Leadfeeder MCP** — if the account isn't in Salesforce, it won't be in Leadfeeder either. The MCP is a slower path to the same data.

**Snowflake-first principle**: Snowflake is always available and never requires re-auth. Route every CRM query through Snowflake. SF MCP is only for three objects with no Snowflake equivalent: `EmailMessage`, `Task`, and `OpportunityContactRole`. Everything else — accounts, contacts, opps, campaigns, Gong, Leadfeeder, Zendesk, notes — comes from Snowflake.

---

## Important Guidelines

- Report file must be under 1,000,000 characters.
- Every claim tagged with its source: `(Snowflake)`, `(web: <domain>)`, `(ATS: <provider>)`, `(Sumble)`, or `(prior report — unverified)`. Omit only for universally known facts.
- Preserve all prior changelog entries on re-runs.
- In batch mode, save incrementally after each company completes.
- Slug collision: append `_2`, `_3`, etc.
- **Primary sources of truth** (in order): Gong transcripts (CONFIRMED) > Gong account synthesis > web search CONFIRMED evidence > ATS/Sumble hiring signals > SF first-party CRM (SF_CONTACTS, SF_OPPS).
- All SF 3rd-party enrichment fields (HG_*, CF_*, DATAFOX_*, NUMBER_OF_EMPLOYEES, ANNUAL_REVENUE, APOLLO_INTENT_*) are unreliable — get tech stack from web search + ATS + Sumble instead.
- `SF_OPPS.AIRFLOW_EXPERIENCE` and `CURRENT_AIRFLOW_DEPLOYMENT_MODEL` (human-entered discovery notes) are reliable — lead with them when present.
- SF_CONTACTS pricing page and Airflow debug page visits are person-level buying signals — flag any that occurred in last 30 days as HIGH urgency.
- **Fit scoring** (0–20): confirmed Airflow use +5, confirmed dbt use +4 (direct Cosmos upsell), data engineering team size +3, cloud-native or AI/agentic stack +2 (LangChain/LangGraph/MLflow/Vertex AI etc.), active DE/ML/platform/finance-systems/revops hiring +2, competitor orchestration tool +2 (Prefect/Dagster/Temporal = migration target), growth signals +2, Gong engagement +2, ICP industry match +1, trial/product usage +2, workflow automation graduating to Airflow +1 (n8n/Zapier/Workato/Clay). Do NOT double-count: confirmed Airflow (+5) excludes competitor tool (+2).
- **Grade**: A (14–20), B (9–13), C (5–8), D (0–4). MC Grade = same scale based on market/company health signals.
- **Confidence**: HIGH = 3+ independent sources confirm key signals; MEDIUM = 1–2 sources; LOW = minimal data.
- **Report sections to include when data available**: ARR Trend (H2), Customer Health (H3, with 🟢/🟡/🔴 labels), Product Usage / Top Operators (H4), AI / Agentic Stack subsection inside Tech Stack.
- **Account at a Glance**: Always include immediately after the Fit Score line. Customers: ARR, Contract End + days, Product Tier, AE/CSM/FE, IS_DOWNGRADE_RISK, Cloud/Region. Prospects: CRM status, Acct Score + drivers, ICP designation, Astronomer owner. One compact table — 5-second scanability.
- **Overall Assessment**: Always include immediately after Account at a Glance. Strengths (2–4 green signals), Risks (2–4 red/amber signals), Bottom Line (1-sentence AE action). Sources from all data gathered — Gong, Snowflake health, web. This moves the "so what" to the top.
- **Renewal Risk** (customers only, H3 data): Dedicated table with Days to Renewal, ATR, Risk Level (🔴 if IS_DOWNGRADE_RISK=TRUE, 🟡 if DAYS_TO_RENEWAL < 180 and USAGE_VS_CONTRACT_TARGET_PCT_30D < 60%, else 🟢), Renewal Manager, Last Renewal Touch. Omit for prospects.
- **Feature Adoption** (customers only, H4 operator data): Four-row table — Airflow Core (5 features), Developer Experience (7), Intelligent Infrastructure (7), Observability (5). Grade each 🟢/🟡/🔴. Notable Gaps column = AE upsell targets. Detection rules: Cosmos = DbtTaskGroup/DbtDag operator; Remote Execution = REMOTE_EXECUTION tasks > 0; KubernetesExecutor = KubernetesPodOperator present; Alerts = health alerts > 0. Omit if no H4 data.
- **Key Contacts table** (SF_CONTACTS): Add Email Count column (total SF Tasks with Type='Email' for that contact, from Query K) and Last Inbound column (most recent inbound email date from Query I). These two columns are the relationship-depth signal — 50+ emails = deep relationship, 0 = cold, Last Inbound >60d = going cold.
- **Prior report skepticism**: treat prior report claims as valid only if from Snowflake data, labeled CONFIRMED in prior tech stack, or corroborated by new data. Silently drop unverifiable prior claims.
- **Omit unverifiable claims**: never include any claim that can't be traced to data explicitly in the prompt. When in doubt, leave it out.

---

**Begin research for:** {{args}}
