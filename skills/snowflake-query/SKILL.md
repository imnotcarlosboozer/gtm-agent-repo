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
- **Default warehouse**: `HUMANS` (X-Small, auto-suspend 60s)
- **Primary database**: `HQ`
- **Auth**: RSA key pair via `PRIVATE_KEY_PASSPHRASE` env var (already configured)

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
| `MODEL_CRM.SF_CONTACTS` | Salesforce contacts. Has `ASTRO_USER_ID` link. No email column (privacy) — use Salesforce URL. |
| `MODEL_CRM.SF_CONTACTS` | Has `CONTACT_URL` (Salesforce link), `TITLE`, `PRIMARY_DOMAIN`, `ASTRO_USER_ID` |

### Layer 1 — IN (raw ingested)

| Table | What it is |
|---|---|
| `IN_ASTRO_DB_PROD.ORG_USER_RELATION` | Raw user↔org with `DELETED_AT` |
| `IN_ASTRO_DB_PROD.ORGANIZATION` | Raw org with `BILLING_EMAIL` |
| `IN_ASTRO_DB_PROD.USER_INVITE` | User invite records |

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

---

## Optimization Rules

1. **Always CTE-filter before joining**: Resolve `ACCT_NAME → ORG_ID` in a CTE, then join. Never join first and filter after on large tables.

2. **Always filter `TIME_GRAIN` on `*_MULTI` tables**: These tables store day/week/month rows for every org. Without `TIME_GRAIN = 'day'`, you'll scan 3× the data.

3. **Always add `DATE` filter on time-series tables**: `ORG_COST_MULTI`, `DEPLOYMENT_COST_MULTI`, `DAG_ACTIVITY_DAILY`, etc. are partitioned by date. A missing date filter = full table scan.

4. **Prefer MART over joining MODEL**: `CURRENT_ASTRO_CUSTS` already joins usage, contract, ARR, and team data. Don't replicate that join.

5. **Never `SELECT *` on wide tables**: `CURRENT_ASTRO_CUSTS` has 120+ columns. Select only what you need.

6. **Avoid `MODEL_ASTRO.TASK_RUNS` and `DAG_RUNS` directly**: Use `METRICS_ASTRO.*` aggregates instead. Only touch raw runs if you need task-level detail, and always filter by a specific date range.

7. **`*_LATEST` tables are pre-filtered**: `SF_ACCT_FEATURE_STORE_LATEST`, `SF_ACCT_SCORES_LATEST`, etc. — no date filter needed.

8. **Use `SAMPLE` for exploration**: `SELECT * FROM big_table SAMPLE (100 ROWS)` to spot-check data without a full scan.

9. **Result cache**: Snowflake caches identical query results for 24h. Keep expensive base CTEs unchanged when iterating — only modify the outer SELECT.

---

## Email / Contact Lookup Notes

- **Full user emails are not stored in Snowflake** — privacy policy strips them from all models
- `MODEL_ASTRO.USERS` has `EMAIL_DOMAIN` only (e.g. `huli.io`)
- `MODEL_CRM.SF_CONTACTS` has `ASTRO_USER_ID` link + `CONTACT_URL` (Salesforce link where full email lives)
- To get full emails: join `ORG_USER_RELATION → USERS → SF_CONTACTS`, then use the `CONTACT_URL` to open Salesforce, or enrich via Apollo

---

## Learned Patterns Log

This section is updated automatically by the daily skill-refresh cron. Each entry captures a query pattern that was used successfully or a correction to a prior approach.

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
<!-- PATTERNS_LOG_END -->
