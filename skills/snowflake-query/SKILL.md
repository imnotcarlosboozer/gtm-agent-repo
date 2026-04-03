---
name: snowflake-query
description: Query Astronomer's Snowflake data warehouse efficiently. Use when the user asks questions that require Snowflake data — customer usage, costs, billing, product metrics, org/user lookups, ARR, or any analytical question about Astronomer customers. Knows the full table map, join patterns, and optimization rules so queries are fast and correct on the first try.
---

# Snowflake Query

Query Astronomer's Snowflake data warehouse using the MCP tools (`mcp__snowflake__*`). This skill provides the schema map, join patterns, and optimization rules needed to write efficient queries without trial and error.

## Input
The user has asked: {{args}}

---

## Connection & Warehouse

- **Account**: `fy02423-gp21411`
- **User**: `JOSEPHKENNEY`
- **Default warehouse**: `HUMANS` (X-Small, auto-suspend 60s) — **only valid warehouse; `ANALYST_WH` does not exist**
- **Primary database**: `HQ`
- **Auth**: RSA key pair via `PRIVATE_KEY_PASSPHRASE` env var (already configured)

---

## Account ID Cache (Joey Kenney's Book of Business)

Skip the `ACCT_NAME LIKE '%..%'` CTE lookup for these accounts — use IDs directly.

| Account | ORG_ID | METRONOME_ID | ARR | Contract End |
|---|---|---|---|---|
| Third Point | `cl6e1hc82009l0s0ebuei60ec` | `406e7187-2fae-45d5-b96f-1c893bbf0e30` | $136K | 2026-05-15 |
| Go Sonar (FreightWaves) | `cl8ub8vd001xe0uxz950r9c35` | `2d68588a-b985-43f8-a60f-75403ddcec18` | $78K | 2026-09-28 |
| Advanced Symbolics | `clmz6bi9e00fm01hywjtgaj68` | `4441d863-d407-47dc-aa31-0171a3c78f40` | $54K | — |
| Surge AI | `clthudyr0011301nzy9gvdtq1` | `33adbe27-fc52-4edb-bd06-d886927feed3` | $52K | — |
| Boothbay Fund Management | `cmeohlt941c4f01pepwpyksne` | `1db2ab6c-8e65-408c-aaa0-cac2bcfce465` | $49K | — |
| Premier Truck Rental LLC | `cmhbcy7ah01yj01nc3tmfooy5` | `6787d2e9-29cb-45ac-8452-15061763d15f` | $48K | 2026-10-31 |
| MileIQ | `cm7wlc62d15j701q9oxzboucl` | `2816a23e-11e6-4818-a6b9-fb47a94ac20e` | $37K | 2026-04-06 |
| Pulumi | `cmbz9v67x1tg201iyoi3kxpi2` | `cd3a1bf7-271b-499c-aaa2-7d7e9a4d4260` | $37K | 2026-08-18 |
| Together Computer | `cmianzvn30dvy01kcmdamoe1q` | `e32e8a06-b47a-4453-b556-7e809ec7215c` | $36K | 2027-01-04 |
| SpringWorks Therapeutics | `cm850f59l035g01ktwh5iwzpe` | `2c568dd9-ab11-4c29-a029-b8af1b7666a9` | $35K | 2026-04-13 |
| Cordada | `clcuypvia0qe20t3d6c1if8ws` | `d83a4268-9deb-4369-b23f-2c56e728bab5` | $35K | 2027-01-04 |
| Differential | `cljsvo6na00y101lvx7i51kjm` | `8e2c81c8-d8e6-4ab4-ba8b-3c28aeb1d581` | $35K | 2026-11-03 |
| USAFacts | `clk31o2l600fs01hkyyw98pwt` | `4070cbd8-5721-46f6-8212-24d09dff4d49` | $32K | 2026-04-08 |
| DLR | `cmc4xg1ih178v01ihhft678xg` | `2689990c-0ecc-486d-81cd-0ea4b12a3ba5` | $32K | 2026-07-24 |
| Crexi | `cmhtofqia161w01me3veevo66` | `a2dd259a-1309-42ad-bc2a-89594808c2c8` | $30K | 2027-01-04 |
| Rithm Capital | `cmf5gimkj3ls501psapalaz63` | `25f75fcb-5dc8-42d1-bbf3-898bf043e0f3` | $28K | 2028-10-31 |
| GlossGenius | `cllmjc18y000801fgr9ehz27g` | `e3cfb8e8-d632-40ec-a9dd-8f1f12456298` | $28K | 2026-10-31 |
| Parafin | `cljpyvrn4020t01lt2igt3kdo` | `ff00fbd8-f00c-4801-b7ef-29a34315557a` | $28K | 2026-08-22 |
| Behaviour Interactive | `cl6fd5hg9010c0tzphpmgftz3` | `b658958a-42a3-4f14-b758-0f405ec50091` | $26K | 2026-10-10 |
| Pretto | `cmk6y0dsn03dy01psb8earfkl` | `da14d290-2260-489c-9e3b-097636683397` | $25K | 2027-02-12 |
| Pivotal Life Sciences | `clgzuej0u006t01lmwj6gigt3` | `9f55545c-61b7-4f36-8ae4-1ac8405f6020` | $25K | 2026-04-30 |
| Ace 1 Media | `cly3qqsky145801k2ulltysqu` | `4a594f96-3f2a-4c11-a032-26305a8ee03f` | $25K | 2026-07-17 |
| New Orleans Pelicans | `cm1du2l6y0zfs01j5dbi5wnxt` | `3a6ae7ce-859b-44c8-a9ce-e993d33727cb` | $24K | 2026-10-06 |
| Saatchi Art | `cljsnv8kz00ut01gi8a2xpfcy` | `d28b22cf-e45a-42e4-af1c-f17e39249108` | $23K | 2027-01-29 |
| Updater Inc. | `cloqcobtl003401kby4esrrmp` | `62b61b9d-ea01-41ea-a188-dc7c133fc839` | $22K | 2026-10-30 |
| Middle Seat | `cmbqzrnkj1rge01lh73hyvhbl` | `9d7aa215-15a1-450b-b01d-5d0e4e2d6a68` | $21K | — |
| NYCSBUS | `cl1w5kbm301ya0rzo0pyb7v1k` | `54369b0a-754c-4fa8-9004-7e7d291b781e` | $20K | 2026-03-31 |
| NOW Insurance | `cloolp7z201yw01jhymmhlwwb` | `bc45e0fa-45ef-435b-8dfe-f570716b8512` | $18K | — |
| Spoiler Alert | `cm6fgnbcj1ep501l3ilxb1xgj` | `4420b6b3-e761-4425-973b-25a007ec3b80` | $18K | 2027-02-27 |
| JCA | `cmgv7px2p09ko01jxdnra9glk` | `c4392afb-73f5-4c0a-a7d0-a4bd14d20647` | $18K | — |
| Draftea Technologies | `cl4eolzp300l20s0ec9gz9g2m` | `b2cd4ee8-a109-48b8-a93d-241dd73ef804` | $17K | 2026-05-31 |
| Pyx Health | `cm976gqb51ila01madyh6c1mu` | `c6e007af-1a59-4df6-8928-4cada59cb45d` | $15K | — |
| Black Crow AI | `clwqkqwwy0puu01nqtui7xyms` | `26c96d26-7530-4737-9c16-288025d248d7` | $15K | 2026-06-30 |
| Hover | `clmkxwux3003201m2pdvybgtj` | `c9216665-f052-448f-938b-a7345b6ff770` | $14K | — |
| Prizma | `clv5ueo3g054z01or4o0ztkft` | `528793e9-9d24-4891-a638-1be211aa779a` | $14K | — |
| Panther Labs | `cl4rc9hvz004j0txb8jfw88f3` | `9b110534-a066-4740-aaff-a209fb2aaefc` | $13K | 2026-04-26 |
| Huli | `clnmy428c008s01nx7hqs9w1t` | `423c2c9f-434c-4b9b-9f0d-479b9ed9f0a9` | $12K | — |
| Envoy | `cln0iktux00uq01hyw80jht5v` | `583a55ee-5f9d-4936-b487-993ac4049b1d` | $12K | 2027-01-30 |
| Tampa Bay Lightning | `clktxc1lr002401nzzajvletk` | `83b2beb0-d293-4af1-85b2-2789c4844a09` | $12K | 2026-10-30 |
| Orita | `cma2t7w2j20uj01hvc0xjwrei` | `6ed17596-50e7-461f-b13e-14d1017404b2` | $12K | 2026-06-29 |
| Sutco | `cln0nqfcz003x01nhjjv9osld` | `9be3e209-bc2d-4cd1-be7c-3f6ecbec59f8` | $12K | 2027-12-31 |
| Rothy's | `clq0jrgbn00kl01m8ghcmw67f` | `8677403a-c9e3-4800-b2c8-3477df2d064e` | $11K | 2027-02-16 |
| Lemba | `cm3pz2shq06w501np1yuy5iol` | `18c59364-2bc6-499b-a654-4dee8fa62216` | $11K | 2026-10-21 |
| MarginEdge | `cm9n1pmd80ykw01m5bbkdmcv9` | `de1ed4b6-0c01-415c-86fe-5e56634292a9` | $10K | — |
| RaveHealth | `cm05e7u59013n01n352gir6cb` | `9c7513f6-e811-4833-942a-271d414da30e` | $10K | 2026-09-30 |
| MagicSchool AI | `cmfbox58l1icn01nt6bvlwg3n` | `36121aeb-26d0-4d21-8665-fb8595e63006` | $10K | 2026-11-02 |
| PlaneSense | `clt68ead000js01k55vjqtek8` | `9f592c3a-09cc-47c2-829c-1ad2d99c6fc9` | $10K | 2026-04-30 |

> **Note**: Cache generated 2026-04-01. Refresh periodically from `CURRENT_ASTRO_CUSTS WHERE OWNER_NAME ILIKE '%kenney%'`.

---

## Database Architecture (HQ)

The HQ database follows a layered architecture. Always query the highest layer that satisfies the question — it's faster and pre-joined.

```
IN_*        Raw ingested data (Fivetran). Avoid unless you need raw event detail.
MODEL_*     Cleaned, modeled entities. Use for entity lookups and joins.
METRICS_*   Pre-aggregated time-series. Use for trend/cost/activity queries.
MART_*      Business-ready wide tables. Use first — already joined, widened.
REPORTING   Reporting-layer copies of key METRICS_ tables.
```

### Layer 4 — MART (start here)

| Table | What it is | Key columns |
|---|---|---|
| `MART_CUST.CURRENT_ASTRO_CUSTS` | Gold standard customer table. Every active Astro customer with usage, contract, ARR, projections, tags, team assignments. | `ACCT_NAME`, `ORG_ID`, `METRONOME_ID`, `ACCT_ID` (SF), `TOTAL_ARR_AMT`, `USAGE_AMT_1D/7D/30D`, `CONTRACT_END_DATE`, `OWNER_NAME`, `FIELD_ENGINEER`, `CUST_SUCCESS_MANAGER` |
| `MART_CUST.CURRENT_ASTRO_CUSTS_W_CRM` | Same as above but with CRM fields pre-joined. Skip the SF join step. | Same as above minus credit projections |
| `MART_CUST.CURRENT_ASTRO_CUSTS_SNAPSHOTS` | Historical daily snapshots of CURRENT_ASTRO_CUSTS | `DATE`, `ORG_ID` |
| `MART_GTM.SF_ACCT_FEATURE_STORE` | Per-account feature/signal store for GTM. Scored daily. | `DATE`, `ACCT_ID` |
| `MART_GTM.SF_ACCT_SCORES` | Propensity/health scores | `DATE`, `ACCT_ID` |
| `MART_FINANCE.USAGE_PERIODS_LOG` | Contract usage vs. period | `ORG_ID` |

### Layer 3 — METRICS (aggregated time-series)

All `*_MULTI` tables share the same schema pattern:
```
DATE         DATE       -- The period anchor date
TIME_GRAIN   VARCHAR    -- 'day', 'week', 'month' — ALWAYS filter this
START_DATE   DATE       -- Period start
END_DATE     DATE       -- Period end
[grain_key]             -- ORG_ID, DEPLOYMENT_ID, etc.
[metrics]               -- Cost, runtime, count columns
```

| Table | Grain key | Best for |
|---|---|---|
| `METRICS_FINANCE.ORG_COST_MULTI` | `ORG_ID` | Per-org daily/weekly/monthly spend |
| `METRICS_FINANCE.DEPLOYMENT_COST_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Per-deployment cost breakdown |
| `METRICS_FINANCE.DEPLOYMENT_REGION_COST_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Cost by cloud region |
| `METRICS_FINANCE.WORKER_QUEUE_COST_MULTI` | `WORKER_QUEUE_ID`, `ORG_ID` | Worker queue cost |
| `METRICS_FINANCE.CLUSTER_COST_MULTI` | `CLUSTER_ID`, `ORG_ID` | Cluster cost |
| `METRICS_FINANCE.METRONOME_USAGE_MULTI` | `METRONOME_ID` | Credit usage vs contract |
| `METRICS_FINANCE.METRONOME_REVENUE_DAILY` | `METRONOME_ID` | Daily revenue |
| `METRICS_ASTRO.ORG_ACTIVITY_MULTI` | `ORG_ID` | Org-level task/DAG activity |
| `METRICS_ASTRO.DEPLOYMENT_ACTIVITY_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Deployment activity |
| `METRICS_ASTRO.DAG_ACTIVITY_DAILY` | `ORG_ID`, `DATE` | Daily DAG metrics |

### Layer 2 — MODEL (cleaned entities)

| Table | What it is |
|---|---|
| `MODEL_ASTRO.USERS` | All users. Has `USER_ID`, `EMAIL_DOMAIN`, `STATUS`. **No full email stored.** |
| `MODEL_ASTRO.USER_ROLES` | User-org role bindings with `EMAIL_DOMAIN`, `ROLE`, `IS_ACTIVE` |
| `MODEL_ASTRO.ORG_USERS` | User↔org membership with role |
| `MODEL_ASTRO.ORGANIZATIONS` | Org entities keyed on `ORG_ID` |
| `MODEL_ASTRO.DEPLOYMENTS` | All deployments |
| `MODEL_ASTRO.TASK_RUNS` | **7.4B rows / 1TB** — always filter by date |
| `MODEL_ASTRO.DAG_RUNS` | **1.5B rows** — always filter by date |
| `MODEL_CRM.SF_CONTACTS` | Salesforce contacts. Has `ASTRO_USER_ID` link. No email column (privacy) — use Salesforce URL. Has `CONTACT_URL`, `TITLE`, `PRIMARY_DOMAIN`. |
| `MODEL_CRM.SF_ACCOUNTS` | Salesforce accounts. Key columns: `ACCT_NAME`, `ACCT_ID`, `OWNER_NAME`, `SALES_TEAM` (Commercial/Enterprise/Strategic), `SALES_REGION`, `TOTAL_ARR_AMT`, `SMOKE_SCORE`, `ACCT_HEALTH`, `IS_CURRENT_CUST`, `IS_CHURN_RISK`, `NEXT_RENEWAL_DATE`, `HG_AIRFLOW/DATABRICKS/MWAA` (boolean tech flags), `ZD_ORG_ID` (direct Zendesk org ID — shortcut for ZD lookups without MAPS join). **No IS_DELETED column** — filter `ACCT_TYPE NOT IN ('Internal','Competitor')`. |
| `MODEL_CRM.SF_OPPS` | Opportunities. `OPP_TYPE`: New Business/Expansion/Renewal/Guided Trial/Churn/Downsell. Stages: `1-Discovery` → `2-QSO & Demo` → `3-EB Meeting` → `4-Tech Workshop/POV` → `5-Negotiate` → `7-Closed Won`/`8-Closed Lost`. Filter active: `IS_OPEN = TRUE`. Key: `AMT`, `INCREMENTAL_ARR_AMT`, `CLOSE_DATE`, `OWNER_FORECAST_CATEGORY`, `NEXT_STEPS`. |
| `MODEL_CRM.SF_MQLS` | MQL events. One row per MQL — contacts can have multiple. Key: `CONTACT_ID`, `ACCT_ID`, `MQL_TS`, `REPORTING_CHANNEL` (Webinar/Free Trial/Tradeshow/Paid Social/Paid Search/Field Event/etc), `ASSIGNED_AE_NAME`, `ASSIGNED_SDR_NAME`, `DISQUALIFICATION_REASON`. |
| `MODEL_CRM.SF_USERS` | SF users (reps, CSMs, FEs). `IS_ACTIVE`, `IS_ACCT_EXEC`. `ROLE` examples: `Commercial Sales (AE)`, `Enterprise Sales (AE) - East (Ritchie)`, `Field Engineer - Enterprise`, `CSM`. `SEGMENT`: Commercial/Enterprise/Enterprise+. |
| `MODEL_CRM.SF_RENEWALS` | Renewal opp summary. `ATR_AMT`, `RENEWAL_AMT`, `RENEWAL_OUTCOME`, `ATR_DATE`, `IS_PRODUCT_TRANSITION`. |
| `MODEL_CRM.SF_ASTRO_ORGS` | Maps `ORG_ID` → `ACCT_ID`. Also has `METRONOME_ID` — the bridge between product/billing and CRM. |
| `MODEL_CRM.LF_WEBSITE_VISITS` | Leadfeeder web visits. **FK is `SF_ACCT_ID` (not `ACCT_ID`)** — join to SF_ACCOUNTS on `SF_ACCT_ID = ACCT_ID`. Columns: `VISIT_TS`, `LANDING_PAGE`, `PAGE_VIEW_COUNT`, `SOURCE`, `MEDIUM`, `REFERRER`. |
| `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS` | Gong transcript text. Key columns: `CALL_ID`, `ACCT_NAME`, `CALL_TITLE`, `CALL_URL`, `SCHEDULED_TS`, `OPP_NAME`, `CALL_BRIEF`, `CALL_NEXT_STEPS`, `ATTENDEES`, `FULL_TRANSCRIPT`. Join to `GONG_CALLS` on `CALL_ID`. |
| `MODEL_CRM_SENSITIVE.GONG_CALLS` | Gong call metadata. Key columns: `CALL_ID`, `IS_DELETED`, `OPP_STAGE_AT_CALL`, `CALL_DURATION`, `PRIMARY_EMPLOYEE`. Always filter `IS_DELETED = FALSE`. |
| `MODEL_SUPPORT.ZD_TICKETS` | Zendesk tickets. **`ORG_ID` is Zendesk's ORG_ID (NUMBER type), NOT Astro ORG_ID.** Join chain: `ZD_TICKETS.ORG_ID → MAPS.ZD_ORGS.ZD_ORG_ID → ACCT_ID`. Key: `STATUS` (open/pending/hold/solved/closed), `PRIORITY` (p1-p4), `TYPE` (question/incident/problem/task), `PRODUCT`, `IS_ESCALATED`, `BUSINESS_IMPACT`, `CUSTOMER_SENTIMENT`. |
| `MODEL_SUPPORT.ZD_TICKET_COMMENTS` | Ticket thread. `BODY`, `IS_EMPLOYEE`. Join on `TICKET_ID`. Use `IS_EMPLOYEE = FALSE` for customer-only comments. |
| `MODEL_SUPPORT.ZD_ORGS` | Raw Zendesk org data. `ORG_ID`, `ORG_NAME`, `DOMAIN_NAMES` (array — use `LATERAL FLATTEN` for domain matching), `IS_DELETED`. Different schema from `MAPS.ZD_ORGS` — use this for domain-based ZD org resolution. |
| `MODEL_CRM.SF_ACCOUNT_DOMAINS` | Domain→account mapping. `ACCT_ID`, `EMAIL_DOMAIN`, `IS_UNIQUE_DOMAIN`. Use `IS_UNIQUE_DOMAIN = TRUE` to avoid false matches on shared domains (e.g. gmail.com). |
| `MODEL_ASTRO.ORGANIZATIONS` | Org metadata. **FK to SF is `SF_ACCT_ID` (not `ACCT_ID`)** — naming inconsistency vs all other tables. Has `PRODUCT_TIER` (trial/paygo/team/enterprise/etc), `IS_TRIAL`, `IS_POV`, `IS_OBSERVE_ENABLED`, `METRONOME_ID`. Filter `IS_DELETED = FALSE AND IS_INTERNAL = FALSE`. |
| `MODEL_ASTRO.DEPLOYMENTS` | Deployment config. `EXECUTOR` (Celery/Astro/Kubernetes/Stellar), `SCHEDULER_SIZE` (small/medium/large), `CLUSTER_TYPE` (HOSTED/SHARED/BRING_YOUR_OWN_CLOUD), `AIRFLOW_VERSION`, `CLOUD_PROVIDER` (aws/gcp/azure), `IS_REMOTE_EXECUTION_ENABLED`, `HAS_CICD_ENFORCEMENT`. Filter `IS_DELETED = FALSE`. |
| `MODEL_CONTRACTS.SF_CUST_CONTRACTS` | Contract terms per opp. `BASE_RATE`, `ON_DEMAND_RATE`, `RESERVED_CAPACITY`, `IS_ANNUAL`, `IS_M2M`, `ASTRO_ORG_ID`. Filter `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE` for current terms. More granular than `ACCT_PRODUCT_ARR`. |
| `MODEL_ECOSYSTEM.SCARF_COMPANY_ARTIFACT_EVENTS` | OSS download signals by company domain. `COMPANY_NAME`, `COMPANY_DOMAIN`, `ARTIFACT_NAME`, `EVENT_COUNT`, `IS_COSMOS_DOCS_PAGE_VIEW`, `IS_DAG_FACTORY_DOWNLOAD`. No direct SF join — match via domain → `SF_ACCOUNT_DOMAINS`. Good for prospecting. |
| `MODEL_EDU.SKILLJAR_COURSE_PROGRESS` | Training completion. `STUDENT_ID`, `COURSE_NAME`, `IS_COMPLETED`, `IS_CERTIFICATION`, `DAYS_TO_COMPLETE`. Good for onboarding health. |
| `MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES` | **Schema discovery tool.** `TABLE_FQID`, `TABLE_SIZE_GB`, `IS_STALE`, `PRIMARY_KEY`, `FOREIGN_KEY`. Query before running against unknown large tables. |
| `MAPS.ZD_ORGS` | Zendesk org → SF account. `ZD_ORG_ID`, `ZD_ORG_NAME`, `ACCT_ID`, `ACCT_NAME`. Filter `IS_DELETED = FALSE`. |
| `MAPS.ZD_ACCTS` | SF account → Zendesk orgs (reverse). `ACCT_ID`, `ZD_ORG_MAP` (array). |
| `MODEL_FINANCE.METRONOME_CONTRACTS` | Billing contracts. `PLAN_TYPE`: contract/paygo/trial/pov/internal. `IS_ACTIVE`, `START_TS`, `END_TS`, `RATE_CARD_ID`. Join via `METRONOME_ID`. |
| `MODEL_FINANCE.METRONOME_INVOICES` | Invoices. Filter `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE` for real revenue. `INV_TYPE`: usage/plan_arrears/scheduled/credit_purchase. `TOTAL_AMT`, `PERIOD_START_DATE`, `PERIOD_END_DATE`. |
| `MODEL_FINANCE.METRONOME_CREDIT_GRANTS` | Prepaid credits. `GRANTED_AMT`, `CURRENT_BALANCE_AMT`, `EXPIRED_AMT`. `IS_CONTRACT_CREDIT`, `IS_ACTIVE`, `EFFECTIVE_DATE`, `EXPIRATION_DATE`. Links to SF via `SF_OPP_ID`. |
| `MODEL_FINANCE.METRONOME_CREDITS_DAILY` | Daily credit burn. `CREDIT_DATE`, `DEDUCTED_AMT`, `PERIOD_CREDIT_AMT_CUMULATIVE`. Best for burn rate trends. |
| `MODEL_FINANCE.METRONOME_USAGE_DAILY` | Daily usage billing. **Always filter `IS_LATEST = TRUE`** to avoid snapshot double-counting. `USAGE_AMT`, `BILL_AMT`, `PERIOD_USAGE_AMT_CUMULATIVE`. |

### Layer 1 — IN (raw ingested)

| Table | What it is |
|---|---|
| `IN_ASTRO_DB_PROD.ORG_USER_RELATION` | Raw user↔org with `DELETED_AT` |
| `IN_ASTRO_DB_PROD.ORGANIZATION` | Raw org with `BILLING_EMAIL` |
| `IN_ASTRO_DB_PROD.USER_INVITE` | User invite records |

---

## Table Selection Decision Tree

Use this before writing any query. Pick the first table that satisfies the question.

**"What's the current state of an account?"**
→ `MART_CUST.CURRENT_ASTRO_CUSTS` (ARR, usage, credit balance, health, contract dates, team)

**"How has usage/cost trended over time?"**
→ `METRICS_FINANCE.ORG_COST_MULTI` (cost) or `METRICS_ASTRO.ORG_ACTIVITY_MULTI` (tasks/DAGs)  
→ Always add `TIME_GRAIN = 'day'` and a `DATE` range filter

**"What are the deployment-level costs?"**
→ `METRICS_FINANCE.DEPLOYMENT_COST_MULTI` — grain is `DEPLOYMENT_ID`

**"What does the Metronome billing show?"**
→ Credit balance: `MODEL_FINANCE.METRONOME_CREDIT_GRANTS`  
→ Daily burn rate: `MODEL_FINANCE.METRONOME_CREDITS_DAILY`  
→ Usage vs contract: `MODEL_FINANCE.METRONOME_USAGE_DAILY` (filter `IS_LATEST = TRUE`)  
→ Invoices: `MODEL_FINANCE.METRONOME_INVOICES` (filter `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE`)

**"Who are the users on this account?"**
→ `IN_ASTRO_DB_PROD.ORG_USER_RELATION` + `MODEL_ASTRO.USERS` (for email domain)  
→ Then `MODEL_CRM.SF_CONTACTS` if you need title/SF URL (join on `ASTRO_USER_ID`)

**"What's happening in Gong / what was discussed?"**
→ `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS` JOIN `GONG_CALLS` on `CALL_ID`  
→ Always filter `GONG_CALLS.IS_DELETED = FALSE`  
→ Search by `ACCT_NAME ILIKE '%name%'` — no account ID join needed

**"What support tickets does this account have?"**
→ `MODEL_SUPPORT.ZD_TICKETS` — but ZD_ORG_ID ≠ Astro ORG_ID  
→ Bridge: `ZD_TICKETS.ORG_ID → MAPS.ZD_ORGS.ZD_ORG_ID → ACCT_ID`

**"What's in the open sales pipeline?"**
→ `MODEL_CRM.SF_OPPS` with `IS_OPEN = TRUE`  
→ Filter by `OWNER_NAME` for rep-level, `ACCT_ID` for account-level

**"How is this account tracking vs their contract?"**
→ `MART_CUST.CURRENT_ASTRO_CUSTS` — `USAGE_VS_CONTRACT_TARGET_PCT_30D`, `PROJECTED_FULL_CREDIT_USE_DATE_30D`  
→ For historical contract periods: `MODEL_CONTRACTS.SF_CUST_CONTRACTS` (filter `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE`)

**"What are the deployments / infrastructure configs?"**
→ `MODEL_ASTRO.DEPLOYMENTS` (executor, scheduler size, cluster type, Airflow version)  
→ `MODEL_ASTRO.WORKER_QUEUES` for current queue config (billing lags 2-3 days — don't use Metronome for this)

**"What individual tasks ran and how long did they take?"**
→ `MODEL_ASTRO.TASK_RUNS` — **7.4B rows, always filter by date**  
→ Add `IS_TERMINAL = TRUE` and `OPERATOR_CLASS` filter to narrow scope

**"Has this company been downloading Airflow / OSS?"**
→ `MODEL_ECOSYSTEM.SCARF_COMPANY_ARTIFACT_EVENTS` — match on `COMPANY_DOMAIN`

**"What MQLs has this account generated?"**
→ `MODEL_CRM.SF_MQLS` — filter by `ACCT_ID`, check `REPORTING_CHANNEL`

**"Unknown table or column — what exists?"**
→ `MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES` — free discovery, has `TABLE_SIZE_GB`, `PRIMARY_KEY`, `FOREIGN_KEY`

---

## Common Date Range Snippets

Copy-paste these directly into queries — no mental math needed.

```sql
-- Yesterday
DATE = CURRENT_DATE - 1

-- Last 7 days
DATE >= DATEADD('day', -7, CURRENT_DATE)

-- Last 30 days
DATE >= DATEADD('day', -30, CURRENT_DATE)

-- Last 90 days
DATE >= DATEADD('day', -90, CURRENT_DATE)

-- Current calendar month
DATE >= DATE_TRUNC('month', CURRENT_DATE)

-- Last full calendar month
DATE >= DATE_TRUNC('month', DATEADD('month', -1, CURRENT_DATE))
  AND DATE < DATE_TRUNC('month', CURRENT_DATE)

-- Current quarter
DATE >= DATE_TRUNC('quarter', CURRENT_DATE)

-- Last full quarter
DATE >= DATE_TRUNC('quarter', DATEADD('quarter', -1, CURRENT_DATE))
  AND DATE < DATE_TRUNC('quarter', CURRENT_DATE)

-- Current fiscal year (Astronomer FY = Feb 1 – Jan 31)
DATE >= DATE_FROM_PARTS(
    IFF(MONTH(CURRENT_DATE) >= 2, YEAR(CURRENT_DATE), YEAR(CURRENT_DATE) - 1), 2, 1)

-- Since contract start (use with CURRENT_ASTRO_CUSTS join)
DATE >= c.CONTRACT_START_DATE

-- Trailing 12 months
DATE >= DATEADD('month', -12, CURRENT_DATE)
```

---

## Data Freshness / Lag Reference

How stale can data be when you query it? Use this to set expectations and caveat outputs.

| Source | Table(s) | Typical Lag | Notes |
|---|---|---|---|
| Salesforce → Snowflake | `SF_ACCOUNTS`, `SF_OPPS`, `SF_CONTACTS`, `SF_MQLS` | Same day (4–6h) | Fivetran sync runs hourly |
| Astro product DB → Snowflake | `ORGANIZATIONS`, `DEPLOYMENTS`, `WORKER_QUEUES` | ~1h | Near real-time |
| Astro task/DAG events | `TASK_RUNS`, `DAG_RUNS` | 1–2h | High-volume pipeline |
| Metronome billing events | `METRONOME_COMPUTE_EVENTS`, `DEPLOYMENT_COST_MULTI` | **2–3 days** | Billing pipeline lag — don't use to infer current infra state |
| Metronome invoices/credits | `METRONOME_INVOICES`, `METRONOME_CREDIT_GRANTS` | Same day when finalized | Check `IS_FINALIZED` flag |
| Gong calls | `GONG_CALLS`, `GONG_CALL_TRANSCRIPTS` | **~24h** | Transcripts available next day |
| Zendesk tickets | `ZD_TICKETS`, `ZD_TICKET_COMMENTS` | 1–2h | Near real-time |
| Leadfeeder web visits | `LF_WEBSITE_VISITS` | **~48h** | Leadfeeder processing delay |
| HG Insights tech signals | `SF_ACCOUNTS.HG_*` columns | **Weekly** | Refreshed via SF enrichment job |
| MART_CUST aggregates | `CURRENT_ASTRO_CUSTS` | Daily (rebuilt overnight) | Freshest at start of business day |
| MART_GTM scores | `SF_ACCT_SCORES`, `SF_ACCT_FEATURE_STORE` | Daily | |
| Scarf OSS signals | `SCARF_COMPANY_ARTIFACT_EVENTS` | **~1 week** | Batch aggregation |
| INFORMATION_SCHEMA query history | N/A | **45 min** | Use for recent query analysis |

---

## Key Join Patterns

### Pattern 1: Account name → any metric (most common)

Always resolve account name to `ORG_ID` first in a CTE, then join:

```sql
WITH acct AS (
    SELECT ORG_ID, METRONOME_ID, ACCT_NAME
    FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
    WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
)
SELECT a.ACCT_NAME, m.DATE, m.TOTAL_COST
FROM HQ.METRICS_FINANCE.ORG_COST_MULTI m
JOIN acct a ON m.ORG_ID = a.ORG_ID
WHERE m.TIME_GRAIN = 'day'
  AND m.DATE = CURRENT_DATE - 1
```

### Pattern 2: Users for an account

```sql
WITH acct AS (
    SELECT ORG_ID FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
    WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
)
SELECT DISTINCT
    ou.USER_ID, ou.ROLE,
    u.EMAIL_DOMAIN, u.STATUS
FROM HQ.IN_ASTRO_DB_PROD.ORG_USER_RELATION ou
JOIN HQ.MODEL_ASTRO.USERS u ON ou.USER_ID = u.USER_ID
JOIN acct a ON ou.ORGANIZATION_ID = a.ORG_ID
```

For Salesforce contact info (title, URL to get emails):
```sql
SELECT c.CONTACT_URL, c.TITLE, c.PRIMARY_DOMAIN, c.ASTRO_USER_ID
FROM HQ.MODEL_CRM.SF_CONTACTS c
WHERE c.ASTRO_USER_ID IN (<user_ids>)
  AND c.IS_DELETED = FALSE
```

### Pattern 3: Multi-period cost comparison

```sql
SELECT TIME_GRAIN, START_DATE, END_DATE, TOTAL_COST
FROM HQ.METRICS_FINANCE.ORG_COST_MULTI
WHERE ORG_ID = '<org_id>'
  AND TIME_GRAIN = 'month'
  AND DATE >= DATEADD('month', -3, CURRENT_DATE)
ORDER BY DATE
```

### Pattern 4: Usage vs contract target

```sql
SELECT
    c.ACCT_NAME,
    c.USAGE_AMT_30D,
    c.CONTRACT_TARGET_USAGE_AMT_30D,
    c.USAGE_VS_CONTRACT_TARGET_PCT_30D,
    c.CREDIT_BALANCE,
    c.PROJECTED_FULL_CREDIT_USE_DATE_30D
FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS c
WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
```

### Pattern 5: Gong call fetch by account name

Two-step pattern: count check first, then full fetch.

```sql
-- Step 1: confirm calls exist (fast — uses result cache on repeat)
SELECT COUNT(*) AS call_count
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE UPPER(t.ACCT_NAME) LIKE UPPER('%ACCOUNT_NAME%')
  AND c.IS_DELETED = FALSE

-- Step 2: full fetch with all relevant fields
SELECT
    t.CALL_ID, t.CALL_TITLE, t.CALL_URL, t.SCHEDULED_TS,
    t.ACCT_NAME, t.OPP_NAME, c.OPP_STAGE_AT_CALL, c.CALL_DURATION,
    t.CALL_BRIEF, t.CALL_NEXT_STEPS, t.ATTENDEES,
    c.PRIMARY_EMPLOYEE, t.FULL_TRANSCRIPT
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE UPPER(t.ACCT_NAME) LIKE UPPER('%ACCOUNT_NAME%')
  AND c.IS_DELETED = FALSE
ORDER BY t.SCHEDULED_TS DESC
```

### Pattern 6: Zendesk org lookup for an account

```sql
SELECT z.ZD_ORG_ID, z.ZD_ORG_NAME, z.ACCT_NAME
FROM HQ.MAPS.ZD_ORGS z
WHERE z.ACCT_NAME ILIKE '%acme%'
  AND z.IS_DELETED = FALSE
```

### Pattern 7: Metronome credit balance for a customer

```sql
SELECT cg.CREDIT_NAME, cg.GRANTED_AMT, cg.CURRENT_BALANCE_AMT,
       cg.EFFECTIVE_DATE, cg.EXPIRATION_DATE, cg.IS_ACTIVE, cg.IS_EXPIRED
FROM HQ.MODEL_FINANCE.METRONOME_CREDIT_GRANTS cg
JOIN HQ.MODEL_CRM.SF_ASTRO_ORGS o ON o.METRONOME_ID = cg.METRONOME_ID
JOIN HQ.MODEL_CRM.SF_ACCOUNTS a ON a.ACCT_ID = o.ACCT_ID
WHERE a.ACCT_NAME ILIKE '%acme%'
  AND cg.IS_CONTRACT_CREDIT = TRUE
  AND cg.IS_VOIDED = FALSE
ORDER BY cg.EFFECTIVE_DATE DESC
```

### Pattern 8: Daily usage burn vs contract (Metronome)

```sql
SELECT ud.USAGE_DATE, ud.USAGE_AMT, ud.BILL_AMT,
       ud.PERIOD_USAGE_AMT_CUMULATIVE, ud.PLAN_TYPE
FROM HQ.MODEL_FINANCE.METRONOME_USAGE_DAILY ud
JOIN HQ.MODEL_CRM.SF_ASTRO_ORGS o ON o.METRONOME_ID = ud.METRONOME_ID
JOIN HQ.MODEL_CRM.SF_ACCOUNTS a ON a.ACCT_ID = o.ACCT_ID
WHERE a.ACCT_NAME ILIKE '%acme%'
  AND ud.IS_LATEST = TRUE
  AND ud.IS_CONTRACT = TRUE
ORDER BY ud.USAGE_DATE DESC
LIMIT 90
```

### Pattern 9: MQLs for an account with channel breakdown

```sql
SELECT m.MQL_TS, m.REPORTING_CHANNEL, m.UTM_CAMPAIGN,
       m.ASSIGNED_AE_NAME, m.ASSIGNED_SDR_NAME, m.FIRST_POST_MQL_STATUS
FROM HQ.MODEL_CRM.SF_MQLS m
WHERE m.ACCT_ID = (
    SELECT ACCT_ID FROM HQ.MODEL_CRM.SF_ACCOUNTS
    WHERE ACCT_NAME ILIKE '%acme%' LIMIT 1
)
ORDER BY m.MQL_TS DESC
```

### Pattern 10: Open pipeline for a rep

```sql
SELECT ACCT_NAME, OPP_NAME, OPP_TYPE, CURRENT_STAGE_NAME,
       AMT, CLOSE_DATE, OWNER_FORECAST_CATEGORY, NEXT_STEPS
FROM HQ.MODEL_CRM.SF_OPPS
WHERE OWNER_NAME ILIKE '%kenney%'
  AND IS_OPEN = TRUE
ORDER BY CLOSE_DATE
```

---

## Optimization Rules

1. **Always CTE-filter before joining**: Resolve `ACCT_NAME → ORG_ID` in a CTE, then join. Never join first and filter after on large tables.

2. **Always filter `TIME_GRAIN` on `*_MULTI` tables**: These tables store day/week/month rows for every org. Without `TIME_GRAIN = 'day'`, you'll scan 3× the data.

3. **Always add `DATE` filter on time-series tables**: `ORG_COST_MULTI`, `DEPLOYMENT_COST_MULTI`, `DAG_ACTIVITY_DAILY`, etc. are partitioned by date. A missing date filter = full table scan.

4. **Prefer MART over joining MODEL**: `CURRENT_ASTRO_CUSTS` already joins usage, contract, ARR, and team data. Don't replicate that join.

5. **Never `SELECT *` on wide tables**: `CURRENT_ASTRO_CUSTS` has 120+ columns. Select only what you need.

6. **For optimization recommendations, always check `MODEL_ASTRO.TASK_RUNS` for the actual distribution**: Aggregate tables hide bimodal distributions. Example: `DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` showed ExternalTaskSensor avg 32 min, but `TASK_RUNS` revealed 33% of tasks complete in <30s — a distribution that materially changes the recommendation. Always add `IS_TERMINAL = TRUE` and a date filter. **7.4B rows — always filter by date.**

7. **`*_LATEST` tables are pre-filtered**: `SF_ACCT_FEATURE_STORE_LATEST`, `SF_ACCT_SCORES_LATEST`, etc. — no date filter needed.

8. **Use `SAMPLE` for exploration**: `SELECT * FROM big_table SAMPLE (100 ROWS)` to spot-check data without a full scan.

9. **Result cache**: Snowflake caches identical query results for 24h. Keep expensive base CTEs unchanged when iterating — only modify the outer SELECT.

10. **`MODEL_ASTRO.ORGANIZATIONS` uses `SF_ACCT_ID` (not `ACCT_ID`)**: Every other table in HQ uses `ACCT_ID` as the SF account FK. This table uses `SF_ACCT_ID`. Don't mix them up. Prefer `SF_ASTRO_ORGS` for SF joins (consistent naming).

11. **`ZD_TICKETS.ORG_ID` is Zendesk's ORG_ID (NUMBER), not Astro's ORG_ID (VARCHAR)**: The column names collide but they're completely different keys. Always join via `MAPS.ZD_ORGS.ZD_ORG_ID` to get to `ACCT_ID`. Never join directly on ORG_ID between `ZD_TICKETS` and Astro product tables.

12. **`SF_CUST_CONTRACTS` needs `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE`**: The table contains all historical contract periods. Without these filters you'll get duplicate/expired records.

13. **`SNOWFLAKE_CURRENT_TABLES` is a free schema discovery tool**: Before describing a table or guessing column names, query `HQ.MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES` to get `TABLE_SIZE_GB`, `PRIMARY_KEY`, and `FOREIGN_KEY` — saves a describe_table call and warns you before running a full scan on a 100GB table.

14. **Metronome billing lags 2–3 days behind actual config changes**: Do not use `METRONOME_COMPUTE_EVENTS` to infer current infrastructure state. A worker size appearing in billing doesn't mean that queue is still configured that way. Use `MODEL_ASTRO.WORKER_QUEUES` for current config.

15. **`METRONOME_COMPUTE_EVENTS` has no cost column**: Must join to `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH` and compute `COMPUTE_RUNTIME_SECONDS / 3600 * UNIT_PRICE`. Always scope `RATE_CARD_ITEMS` to the customer's specific `RATE_CARD_ID` first — otherwise you pull prices from other rate cards. Use `ASTRO_ORG_ID` (not `ORGANIZATION_ID`) to filter. `METRONOME_RATE_CARD_ITEMS` has a `PRICING_GROUP_OBJECT_DEFINITION` column — use `LIKE '%small%'` (or the desired scheduler size) to filter to specific rates without JSON parsing. `METRONOME_DEPLOYMENT_EVENTS` has both `EVENT_TS` and `START_TIMESTAMP` date columns — both work for date range filtering. `DEPLOYMENT_COST_MULTI` can be filtered by `METRONOME_ID` in addition to `ORG_ID`.

16. **`DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` requires `TIME_GRAIN = 'day'`**: The table stores day, roll_7d, roll_30d, and week rows for every period. Omitting this filter inflates counts by 40–50x. **Always include `TIME_GRAIN = 'day'` (or the intended grain explicitly).**

---

## CURRENT_ASTRO_CUSTS Column Reference

The gold standard customer table (`HQ.MART_CUST.CURRENT_ASTRO_CUSTS`) — 140+ columns. Key groups:

**Identity**
- `ACCT_ID` — Salesforce account ID (primary SF FK)
- `ORG_ID` — Astro organization ID (product system key)
- `METRONOME_ID` — Billing system ID (bridge to Metronome tables)
- `ACCT_NAME`, `ACCT_TYPE`, `ACCT_STATUS`
- `OWNER_NAME`, `FIELD_ENGINEER`, `CUST_SUCCESS_MANAGER`
- `SALES_TEAM` (Commercial/Enterprise/Strategic), `SALES_REGION`

**Contract & Revenue**
- `TOTAL_ARR_AMT`, `ARR_AMT`, `ARR_PLAN_AMT`
- `CONTRACT_START_DATE`, `CONTRACT_END_DATE`
- `DAYS_TO_RENEWAL`, `ATR_AMT`, `ATR_DATE`
- `IS_ANNUAL`, `IS_M2M`, `IS_PRODUCT_TRANSITION`
- `RENEWAL_OUTCOME` (Renewed/Churned/Downsell/Upsell)

**Usage (real-time)**
- `USAGE_AMT_1D`, `USAGE_AMT_7D`, `USAGE_AMT_30D`
- `CONTRACT_TARGET_USAGE_AMT_30D`, `USAGE_VS_CONTRACT_TARGET_PCT_30D`
- `TASK_SUCCESS_COUNT_7D`, `TASK_SUCCESS_COUNT_30D`
- `DISTINCT_DAG_COUNT_30D`, `DISTINCT_USER_COUNT_30D`

**Credit & Billing**
- `CREDIT_BALANCE` — remaining prepaid credit balance
- `PROJECTED_FULL_CREDIT_USE_DATE_30D` — estimated credit exhaustion date
- `PROJECTED_FULL_CREDIT_USE_DATE_7D`
- `IS_OVERAGE_RISK` — approaching credit limit

**Health & Risk**
- `SMOKE_SCORE`, `FIRE_SCORE`
- `IS_DOWNGRADE_RISK`, `IS_EXPANSION_CANDIDATE`
- `P1_TICKET_COUNT`, `P2_TICKET_COUNT`, `P3_TICKET_COUNT`
- `IS_CURRENT_CUST`, `IS_TRIAL`, `IS_POV`
- `ACCT_TAGS` (array) — custom tags e.g. 'High Usage', 'Low Engagement'
- ⚠️ `ACCT_HEALTH` and `IS_CHURN_RISK` are in `SF_ACCOUNTS`, **not** `CURRENT_ASTRO_CUSTS`

**Tech Signals**
- `HG_AIRFLOW`, `HG_DATABRICKS`, `HG_MWAA`, `HG_AZURE_DATA_FACTORY` (boolean — HG Insights flags)
- `IS_REMOTE_EXECUTION_ENABLED`

**Renewal Pipeline**
- `NEXT_RENEWAL_DATE`, `RENEWAL_AMT`
- `DAYS_TO_RENEWAL` — negative = overdue

---

## Enum Quick Reference

Use these to write correct `WHERE` clauses without querying the table first.

**`SF_ACCOUNTS.ACCT_TYPE`** — filter noise: `ACCT_TYPE NOT IN ('Internal', 'Competitor')`
Values: Customer, Prospect, Partner, Internal, Competitor, Other

**`SF_ACCOUNTS.ACCT_STATUS`**
Values: Active, Inactive, Former Customer

**`SF_ACCOUNTS.SALES_TEAM`**
Values: Commercial, Enterprise, Strategic, Growth (PLG), Partner

**`SF_OPPS.OPP_TYPE`**
Values: New Business, Expansion, Renewal, Guided Trial, Churn, Downsell

**`SF_OPPS.CURRENT_STAGE_NAME`** (in order)
1-Discovery → 2-QSO & Demo → 3-EB Meeting → 4-Tech Workshop/POV → 5-Negotiate → 7-Closed Won → 8-Closed Lost

**`SF_OPPS.OWNER_FORECAST_CATEGORY`**
Values: Pipeline, Best Case, Commit, Closed, Omitted

**`SF_MQLS.REPORTING_CHANNEL`**
Values: Webinar, Free Trial, Tradeshow, Paid Social, Paid Search, Field Event, Organic Search, Direct, Partner, Content Syndication, Other

**`METRONOME_CONTRACTS.PLAN_TYPE`**
Values: contract, paygo, trial, pov, internal

**`METRONOME_INVOICES.INV_TYPE`**
Values: usage, plan_arrears, scheduled, credit_purchase

**`METRONOME_INVOICES.INV_STATUS`**
Values: draft, finalized, void — filter `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE` for real revenue

**`ZD_TICKETS.PRIORITY`**
Values: p1, p2, p3, p4 (p1 = critical/outage)

**`ZD_TICKETS.STATUS`**
Values: open, pending, hold, solved, closed

**`ZD_TICKETS.TYPE`**
Values: question, incident, problem, task

**`MODEL_ASTRO.ORGANIZATIONS.PRODUCT_TIER`**
Values: trial, basic_paygo, developer_paygo, team, team_paygo, standard, enterprise, business, pov, inactive, internal

**`MODEL_ASTRO.DEPLOYMENTS.EXECUTOR`**
Values: CeleryExecutor, AstroExecutor, KubernetesExecutor, StellarExecutor

**`MODEL_ASTRO.DEPLOYMENTS.CLOUD_PROVIDER`**
Values: aws, gcp, azure

**`MODEL_ASTRO.DEPLOYMENTS.SCHEDULER_SIZE`**
Values: small, medium, large, extra_large (note: SCHEDULER_CPU and SCHEDULER_RAM are identical for small vs medium — cannot use to estimate cost diff)

**`MODEL_ASTRO.DEPLOYMENTS.CLUSTER_TYPE`**
Values: HOSTED, SHARED, BRING_YOUR_OWN_CLOUD, VIRTUAL_RUNTIMES

---

## Email / Contact Lookup Notes

- **Full user emails are not stored in Snowflake** — privacy policy strips them from all models
- `MODEL_ASTRO.USERS` has `EMAIL_DOMAIN` only (e.g. `huli.io`)
- `MODEL_CRM.SF_CONTACTS` has `ASTRO_USER_ID` link + `CONTACT_URL` (Salesforce link where full email lives)
- To get full emails: join `ORG_USER_RELATION → USERS → SF_CONTACTS`, then use the `CONTACT_URL` to open Salesforce, or enrich via Apollo

---

## Auto-Update Instruction

This skill self-updates via two mechanisms:

**1. On query error (immediate):** A PostToolUse hook fires automatically after any failed `mcp__snowflake__execute_query` call and prompts you to log the fix as soon as it's resolved — don't wait until end of session.

**2. End of session (checklist):** The UserPromptSubmit hook reminds you to log new patterns from the session.

**Log an entry when any of the following occur:**
- A query failed due to a wrong column name, schema path, or join — record the error and fix
- An aggregate result was misleading and a different table/grain told a better story
- A new table, column, or join pattern was used successfully for the first time
- A billing/config discrepancy was discovered
- A filter that's always required was discovered (like `IS_LATEST = TRUE`, `TIME_GRAIN = 'day'`)

**After updating, always sync (local CLI only):**
```bash
cp ~/claude-work/gtm-agent-repo/skills/snowflake-query/SKILL.md \
   ~/.claude/skills/snowflake-query/SKILL.md
```

All schema knowledge is embedded in this file — no local file path dependencies. The CURRENT_ASTRO_CUSTS column reference, enum cheat sheet, and join patterns above are the authoritative reference for cloud sessions.

---

## Learned Patterns Log

Each entry captures a query pattern that was used successfully or a correction to a prior approach.

<!-- PATTERNS_LOG_START -->
**2026-03-27** — Initial schema exploration. Key discoveries:
- `CURRENT_ASTRO_CUSTS` is the gold standard account table; always start here
- `ORG_COST_MULTI` uses `ORG_ID` (not `METRONOME_ID`) as the join key — confirmed via actual query
- `IN_ASTRO_DB_PROD.ORG_USER_RELATION.ORGANIZATION_ID` = `ORG_ID` in other tables (different column name)
- `MODEL_ASTRO.USER_ROLES` IS_DELETED filter returns empty for Huli — use `IN_ASTRO_DB_PROD.ORG_USER_RELATION` + `MODEL_ASTRO.USERS` join instead
- `QUERY_HISTORY` requires `SNOWFLAKE.ACCOUNT_USAGE` schema — not accessible under current role
- `INFORMATION_SCHEMA.QUERY_HISTORY()` table function doesn't support named params in this account config
- No clustering keys are set on any tables — Snowflake relies on micro-partition pruning via natural sort order on date columns

**2026-03-30** — Schema correction from refresh run; no new user queries in past 24h:
- `INFORMATION_SCHEMA.QUERY_HISTORY_BY_USER` does NOT have `PARTITIONS_SCANNED` or `PARTITIONS_TOTAL` columns — those only exist in `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` (requires elevated role). Use `BYTES_SCANNED` as the scan-size proxy when using the `INFORMATION_SCHEMA` table function.

**2026-03-30** — Pulumi usage/cost analysis session. Key discoveries:
- `DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` requires `TIME_GRAIN = 'day'` — omitting it caused a 3% undercount (131,584 vs correct 135,092) because `roll_7d`/`roll_30d` rows partially overlapped the date range
- `METRONOME_COMPUTE_EVENTS`: no cost column — must join `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH`; always scope to customer's `RATE_CARD_ID` first; filter uses `ASTRO_ORG_ID` not `ORGANIZATION_ID`
- Metronome billing lags 2–3 days: Pulumi's default queue showed A40 pods in billing 3 days after they'd already switched to A20. Don't use billing data to infer current queue config — use `MODEL_ASTRO.WORKER_QUEUES`
- `MODEL_ASTRO.TASK_RUNS` has individual task durations and is the right table to check before making optimization recommendations. Aggregates mislead: ExternalTaskSensor avg was 32 min but 33% of tasks complete in <30s (upstream already done when sensor fires). Always check distribution, not just average.
- `WORKER_QUEUES` correct column names: `WORKER_QUEUE_NAME`, `POD_SIZE`, `MIN_WORKER_COUNT`, `MAX_WORKER_COUNT`, `IS_DEFAULT`, `IS_DELETED`
- `DEPLOYMENTS` org filter column is `ORG_ID` (not `ORGANIZATION_ID`)

**2026-03-31** — Session covering rate card analysis and Zendesk/Gong table discovery:
- Four new tables confirmed: `MODEL_CRM.SF_ACCOUNTS` (`OWNER_NAME`, `ZD_ORG_ID`), `MODEL_SUPPORT.ZD_ORG`, and `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS`/`GONG_CALLS` (join on `CALL_ID`; always filter `IS_DELETED = FALSE` on GONG_CALLS; filter by `ACCT_NAME` on transcripts)
- `METRONOME_RATE_CARD_ITEMS` has `PRICING_GROUP_OBJECT_DEFINITION` column — use `LIKE '%small%'` (or scheduler type) to filter scheduler-specific rates without parsing `PRICING_GROUP_KEYS` JSON
- `METRONOME_DEPLOYMENT_EVENTS` has both `EVENT_TS` and `START_TIMESTAMP` date columns (confirmed both work for date range filtering); `DEPLOYMENT_COST_MULTI` can also be filtered by `METRONOME_ID` in addition to `ORG_ID`

**2026-04-01** — 48 queries observed (Gong cron runs + ad-hoc cost analysis):
- `GONG_CALL_TRANSCRIPTS` full column set confirmed: `CALL_ID`, `ACCT_NAME`, `CALL_TITLE`, `CALL_URL`, `SCHEDULED_TS`, `OPP_NAME`, `CALL_BRIEF`, `CALL_NEXT_STEPS`, `ATTENDEES`, `FULL_TRANSCRIPT`; `GONG_CALLS` additional columns: `OPP_STAGE_AT_CALL`, `CALL_DURATION`, `PRIMARY_EMPLOYEE`
- `ANALYST_WH` warehouse does not exist — caused "No active warehouse" failures on 2 Gong queries; always connect with `HUMANS` warehouse, never switch via `USE WAREHOUSE`
- Gong count-then-fetch pattern well-established: count check first (~100-700ms), then full transcript fetch only if calls exist; result cache (BYTES=0) kicks in reliably on repeated identical count queries
**2026-04-01** — Full schema mapping session. Major additions:
- Complete column maps for: `SF_ACCOUNTS` (170+ cols incl. tech signals HG_*, smoke/fire scores, churn flags), `SF_OPPS` (stage names confirmed: 1-Discovery through 7-Closed Won/8-Closed Lost; OPP_TYPE enum), `SF_CONTACTS`, `SF_MQLS`, `SF_USERS`, `SF_RENEWALS`, `SF_DISCOVERY_MEETING`, `SF_ASTRO_ORGS`
- `SF_ACCOUNTS` has **no IS_DELETED column** — was confirmed via query error; use `ACCT_TYPE NOT IN ('Internal','Competitor')` instead
- `LF_WEBSITE_VISITS` FK is `SF_ACCT_ID` not `ACCT_ID` — different from all other CRM tables
- Metronome full chain confirmed: `METRONOME_USAGE_DAILY` requires `IS_LATEST = TRUE`; `METRONOME_INVOICES` filter: `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE`; `METRONOME_CREDIT_GRANTS` filter: `IS_CONTRACT_CREDIT = TRUE AND IS_VOIDED = FALSE`
- Metronome → SF join: `METRONOME_ID → HQ.MODEL_CRM.SF_ASTRO_ORGS.METRONOME_ID → ACCT_ID`
- Zendesk tables moved to `HQ.MAPS.ZD_ORGS` and `HQ.MAPS.ZD_ACCTS` (not `MODEL_SUPPORT.ZD_ORG` as previously logged)
- `GONG_CALLS` has `IS_DELETED` column (confirmed); `GONG_CALL_TRANSCRIPTS` does not
- `ORG_ACTIVITY_MULTI` TIME_GRAIN values: day (10.9M rows), roll_30d (11.7M), roll_7d (11.1M), week (1.6M), month (415K) — always filter `TIME_GRAIN = 'day'`
- Hooks added: PreToolUse injects gotchas before every execute_query; PostToolUse detects errors and triggers immediate skill update
**2026-04-01 (full DB sweep)** — Comprehensive schema mapping of all HQ schemas. Key discoveries:
- `MODEL_SUPPORT.ZD_TICKETS`: `ORG_ID` is Zendesk's NUMBER-type ID, NOT Astro ORG_ID — always bridge via `MAPS.ZD_ORGS.ZD_ORG_ID`. Ticket has `PRIORITY` (p1-p4), `TYPE` (question/incident/problem/task), `BUSINESS_IMPACT`, `CUSTOMER_SENTIMENT`, `IS_ESCALATED`, `IS_SECURITY_INCIDENT`. Massive for customer health context.
- `MODEL_ASTRO.ORGANIZATIONS`: FK to SF is `SF_ACCT_ID` (not `ACCT_ID`) — only table in HQ with this inconsistency. Has `PRODUCT_TIER` enum: trial/basic_paygo/developer_paygo/team/team_paygo/standard/enterprise/business/pov/inactive/internal. Filter `IS_DELETED = FALSE AND IS_INTERNAL = FALSE`.
- `MODEL_ASTRO.DEPLOYMENTS`: `EXECUTOR` values: CeleryExecutor/AstroExecutor/KubernetesExecutor/StellarExecutor. `CLUSTER_TYPE`: HOSTED/SHARED/BRING_YOUR_OWN_CLOUD/VIRTUAL_RUNTIMES. Filter `IS_DELETED = FALSE`.
- `MODEL_CONTRACTS.SF_CUST_CONTRACTS`: has actual `BASE_RATE`, `ON_DEMAND_RATE`, `RESERVED_CAPACITY` — more granular than `ACCT_PRODUCT_ARR`. Filter `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE`.
- `MODEL_ECOSYSTEM.SCARF_COMPANY_ARTIFACT_EVENTS`: OSS download signals by company domain — no direct SF join, match via domain → `SF_ACCOUNT_DOMAINS`. Useful for prospecting.
- `MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES`: query this before running against unknown tables to get `TABLE_SIZE_GB` and declared `PRIMARY_KEY`/`FOREIGN_KEY` — free schema discovery.
- Largest schemas: `IN_SPLUNK` (2.9TB), `IN_CHRONOSPHERE` (2.4TB) — engineering, not accessible. `MODEL_ASTRO` (743GB) — always date-filter. `SEGMENT_EVENTS_PROD.CLOUD_UI` (439 tables, 14GB) — raw events, use `MODEL_WEB.*` instead.
- Hooks confirmed working: PreToolUse fired on all 5 parallel queries in this session.
**2026-04-01 (optimization session)** — 5 improvements added to skill:
- `ACCT_HEALTH` and `IS_CHURN_RISK` are NOT columns in `CURRENT_ASTRO_CUSTS` — query errored; both live in `SF_ACCOUNTS`. Fixed column reference section.
- Account ID cache added for all 75 accounts in Joey's book of business (ORG_ID + METRONOME_ID verified from live query) — skip the ACCT_NAME CTE lookup for these accounts
- Table selection decision tree added — covers all major question types with correct starting table
- Common date range snippets added — last 7/30/90d, current/last month, current/last quarter, FY, trailing 12m
- Data freshness/lag table added — covers all major sources with expected lag times; critical: Metronome billing 2-3 day lag, Gong 24h, Leadfeeder 48h, HG Insights weekly
- PostToolUse hook updated: now also fires on successful queries with >1GB bytes scanned, prompting optimization review
**2026-04-02** — 50 queries observed (monthly report cron + ad-hoc ZD lookup):
- `MODEL_SUPPORT.ZD_ORGS` confirmed as a separate table from `MAPS.ZD_ORGS`: has `ORG_ID`, `ORG_NAME`, `DOMAIN_NAMES` (array — lateral flatten for domain matching), `IS_DELETED`. Use for domain-based ZD org resolution. `MAPS.ZD_ORGS` has `ZD_ORG_ID`/`ZD_ORG_NAME`/`ACCT_ID` (SF linkage); `MODEL_SUPPORT.ZD_ORGS` has the raw ZD data with domain names.
- `SF_ACCOUNTS.ZD_ORG_ID` column confirmed — direct shortcut to Zendesk org ID without needing MAPS lookup. Three-tier ZD account match: (1) `SF_ACCOUNTS.ZD_ORG_ID` direct; (2) `MODEL_SUPPORT.ZD_ORGS.ORG_NAME = ACCT_NAME`; (3) domain fallback via `SF_ACCOUNT_DOMAINS` + `LATERAL FLATTEN(ZD_ORGS.DOMAIN_NAMES)`.
- `MODEL_CRM.SF_ACCOUNT_DOMAINS` confirmed: `ACCT_ID`, `EMAIL_DOMAIN`, `IS_UNIQUE_DOMAIN` — use `IS_UNIQUE_DOMAIN = TRUE` for domain→account resolution to avoid false matches on shared domains.
- `DEPLOYMENT_COST_MULTI` with `TIME_GRAIN = 'month'` and single-date + single-ORG_ID filters still scans ~1.8GB; monthly report cron accepts this but ad-hoc queries should add `METRONOME_ID` filter or use `ORG_COST_MULTI` if deployment breakdown isn't needed.
- Monthly report cron (account research) confirmed running clean: 5-query batch per account (CURRENT_ASTRO_CUSTS + ORG_COST_MULTI + ORG_ACTIVITY_MULTI + METRONOME_CREDIT_GRANTS + DEPLOYMENT_COST_MULTI); subsequent cron runs hit result cache (BYTES_SCANNED=0) for all 5.
**2026-04-03** — 44 queries observed (Gong cron + paygo analysis + account research):
- `GTM.PUBLIC.GONG_CALL_ENRICHMENTS` and `GTM.GONG.GONG_CALLS` do NOT exist — no `GTM` database; Gong call data lives exclusively in `HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS` / `GONG_CALLS`; two failed queries wasted ~5s combined
- `ORG_ACTIVITY_MULTI` has an `ACCT_NAME` column and was filtered by it directly, but missing `TIME_GRAIN = 'day'` caused a 2.7GB scan (Rule #2 violation) — TIME_GRAIN filter is required even when filtering by ACCT_NAME, not just ORG_ID
- New paygo customer lookup pattern confirmed: join `CURRENT_ASTRO_CUSTS c` + `MODEL_ASTRO.ORGANIZATIONS o` ON `c.ORG_ID = o.ORG_ID`, filter `o.PRODUCT_TIER IN ('basic_paygo', 'developer_paygo', 'team_paygo')` — `IN_ASTRO_DB_PROD.ORGANIZATION.BILLING_EMAIL` and `MODEL_ASTRO.DEPLOYMENTS.CLOUD_PROVIDER` (new column, added to schema) used for paygo enrichment; `GONG_CALL_TRANSCRIPTS` fetch-by-CALL_ID pattern confirmed: `WHERE CALL_ID IN ('id1', 'id2', ...)` works as a second-step after resolving IDs via ACCT_NAME
<!-- PATTERNS_LOG_END -->
