---
name: snowflake-query
description: Query Astronomer's internal Snowflake data warehouse (HQ database). Use the moment the user asks anything about internal sales data — book of business, my accounts, show me all customers, pipeline, usage trends, DAG counts, ARR, billing costs, renewal dates, days to renewal, credit balance, which accounts are at risk, org/user lookups, product metrics, "how many", "find customers", "show me Z", "who uses X". Also use for account-specific metrics (usage, spend, compute) even when an account is named. Knows the full table map, join patterns, and optimization rules. SCOPE: Astronomer's internal GTM data only — for Airflow pipeline questions use data:/data-engineering: skills instead.
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

| Account | ACCT_ID (SF) | ORG_ID | METRONOME_ID | ARR | Contract End |
|---|---|---|---|---|---|
| Third Point | `0014x00000I7ph6AAB` | `cl6e1hc82009l0s0ebuei60ec` | `406e7187-2fae-45d5-b96f-1c893bbf0e30` | $136K | 2026-05-15 |
| Go Sonar (FreightWaves) | `0014x00000dz5NwAAI` | `cl8ub8vd001xe0uxz950r9c35` | `2d68588a-b985-43f8-a60f-75403ddcec18` | $78K | 2026-09-28 |
| Advanced Symbolics | `0014x000017PVw9AAG` | `clmz6bi9e00fm01hywjtgaj68` | `4441d863-d407-47dc-aa31-0171a3c78f40` | $53K | — |
| Premier Truck Rental LLC | `001PQ00000gl7fNYAQ` | `cmhbcy7ah01yj01nc3tmfooy5` | `6787d2e9-29cb-45ac-8452-15061763d15f` | $48K | 2026-10-31 |
| Pulumi | `0014x00000GNSZ6AAP` | `cmbz9v67x1tg201iyoi3kxpi2` | `cd3a1bf7-271b-499c-aaa2-7d7e9a4d4260` | $37K | 2026-08-18 |
| Together Computer | `001PQ00000AFyjAYAT` | `cmianzvn30dvy01kcmdamoe1q` | `e32e8a06-b47a-4453-b556-7e809ec7215c` | $36K | 2027-01-04 |
| Cordada | `0014x00000sdkWVAAY` | `clcuypvia0qe20t3d6c1if8ws` | `d83a4268-9deb-4369-b23f-2c56e728bab5` | $35K | 2027-01-04 |
| Differential | `0014x00000GMFd9AAH` | `cljsvo6na00y101lvx7i51kjm` | `8e2c81c8-d8e6-4ab4-ba8b-3c28aeb1d581` | $35K | 2026-11-03 |
| USAFacts | `001Du000004GXcWIAW` | `clk31o2l600fs01hkyyw98pwt` | `4070cbd8-5721-46f6-8212-24d09dff4d49` | $32K | 2027-04-08 |
| DLR | `001Du00000324PfIAI` | `cmc4xg1ih178v01ihhft678xg` | `2689990c-0ecc-486d-81cd-0ea4b12a3ba5` | $32K | 2026-07-24 |
| Crexi | `001Du000002gpwZIAQ` | `cmhtofqia161w01me3veevo66` | `a2dd259a-1309-42ad-bc2a-89594808c2c8` | $30K | 2027-01-04 |
| Rithm Capital | `001Du000003YrRKIA0` | `cmf5gimkj3ls501psapalaz63` | `25f75fcb-5dc8-42d1-bbf3-898bf043e0f3` | $28K | 2028-10-31 |
| GlossGenius | `001Du000004SswEIAS` | `cllmjc18y000801fgr9ehz27g` | `e3cfb8e8-d632-40ec-a9dd-8f1f12456298` | $28K | 2026-10-31 |
| Parafin | `0014x00000NQuMrAAL` | `cljpyvrn4020t01lt2igt3kdo` | `ff00fbd8-f00c-4801-b7ef-29a34315557a` | $28K | 2026-08-22 |
| NYCSBUS | `0014x0000123qn1AAA` | `cl1w5kbm301ya0rzo0pyb7v1k` | `54369b0a-754c-4fa8-9004-7e7d291b781e` | $26K | — |
| Behaviour Interactive | `0014x00000l0uEhAAI` | `cl6fd5hg9010c0tzphpmgftz3` | `b658958a-42a3-4f14-b758-0f405ec50091` | $26K | 2026-10-10 |
| Pretto | `0014x00000g3H2WAAU` | `cmk6y0dsn03dy01psb8earfkl` | `da14d290-2260-489c-9e3b-097636683397` | $25K | 2027-02-12 |
| Pivotal Life Sciences | `001Du000003elhgIAA` | `clgzuej0u006t01lmwj6gigt3` | `9f55545c-61b7-4f36-8ae4-1ac8405f6020` | $25K | 2026-04-30 |
| Ace 1 Media | `001PQ00000GaBfiYAF` | `cly3qqsky145801k2ulltysqu` | `4a594f96-3f2a-4c11-a032-26305a8ee03f` | $25K | 2026-07-17 |
| New Orleans Pelicans | `001PQ00000KPy79YAD` | `cm1du2l6y0zfs01j5dbi5wnxt` | `3a6ae7ce-859b-44c8-a9ce-e993d33727cb` | $24K | 2026-10-06 |
| Boothbay Fund Management | `001PQ00000Inu6qYAB` | `cmeohlt941c4f01pepwpyksne` | `1db2ab6c-8e65-408c-aaa0-cac2bcfce465` | $23K | — |
| Saatchi Art | `0014x00000GMFuUAAX` | `cljsnv8kz00ut01gi8a2xpfcy` | `d28b22cf-e45a-42e4-af1c-f17e39249108` | $23K | 2027-01-29 |
| Middle Seat | `001PQ00000ERfaNYAT` | `cmbqzrnkj1rge01lh73hyvhbl` | `9d7aa215-15a1-450b-b01d-5d0e4e2d6a68` | $22K | — |
| Updater Inc. | `0014x00000A9O24AAF` | `cloqcobtl003401kby4esrrmp` | `62b61b9d-ea01-41ea-a188-dc7c133fc839` | $22K | 2026-10-30 |
| JCA | `001PQ00000EJdNRYA1` | `cmgv7px2p09ko01jxdnra9glk` | `c4392afb-73f5-4c0a-a7d0-a4bd14d20647` | $19K | — |
| Spoiler Alert | `0014x00000u5N6xAAE` | `cm6fgnbcj1ep501l3ilxb1xgj` | `4420b6b3-e761-4425-973b-25a007ec3b80` | $18K | 2027-02-27 |
| NOW Insurance | `0014x00000GMELrAAP` | `cloolp7z201yw01jhymmhlwwb` | `bc45e0fa-45ef-435b-8dfe-f570716b8512` | $17K | — |
| Draftea Technologies | `0014x000017RT4bAAG` | `cl4eolzp300l20s0ec9gz9g2m` | `b2cd4ee8-a109-48b8-a93d-241dd73ef804` | $17K | 2026-05-31 |
| Surge AI | `0014x00000seOeeAAE` | `clthudyr0011301nzy9gvdtq1` | `33adbe27-fc52-4edb-bd06-d886927feed3` | $16K | — |
| Pyx Health | `0014x00000dxRcRAAU` | `cm976gqb51ila01madyh6c1mu` | `c6e007af-1a59-4df6-8928-4cada59cb45d` | $15K | — |
| Black Crow AI | `001Du0000032zPLIAY` | `clwqkqwwy0puu01nqtui7xyms` | `26c96d26-7530-4737-9c16-288025d248d7` | $15K | 2026-06-30 |
| Cozy Earth | `001PQ00000sSgIBYA0` | `cmn3jiuq64bla01pudh620bf4` | `d25a17b1-aa39-4153-aeaa-91be6b9a85dd` | $14K | — |
| Hover | `0014x00000GM7KzAAL` | `clmkxwux3003201m2pdvybgtj` | `c9216665-f052-448f-938b-a7345b6ff770` | $14K | — |
| BuildingMinds | `0014x00000bvRIyAAM` | `cmlr75fzo8f2v01om46irqnfe` | `fbaa6d0b-8455-4ab9-9315-ee8c940994f5` | $13K | 2027-04-02 |
| Prizma | `001PQ000007wQB5YAM` | `clv5ueo3g054z01or4o0ztkft` | `528793e9-9d24-4891-a638-1be211aa779a` | $14K | — |
| Panther Labs | `0014x000014diPMAAY` | `cl4rc9hvz004j0txb8jfw88f3` | `9b110534-a066-4740-aaff-a209fb2aaefc` | $13K | 2026-04-26 |
| Huli | `0014x00000DKqetAAD` | `clnmy428c008s01nx7hqs9w1t` | `423c2c9f-434c-4b9b-9f0d-479b9ed9f0a9` | $12K | — |
| Envoy | `0014x00000GNOaTAAX` | `cln0iktux00uq01hyw80jht5v` | `583a55ee-5f9d-4936-b487-993ac4049b1d` | $12K | 2027-01-30 |
| Tampa Bay Lightning | `0014x00000u5PgQAAU` | `clktxc1lr002401nzzajvletk` | `83b2beb0-d293-4af1-85b2-2789c4844a09` | $12K | 2026-10-30 |
| Orita | `001PQ00000X7UeHYAV` | `cma2t7w2j20uj01hvc0xjwrei` | `6ed17596-50e7-461f-b13e-14d1017404b2` | $12K | 2026-06-29 |
| Sutco | `0014x00000DKqdvAAD` | `cln0nqfcz003x01nhjjv9osld` | `9be3e209-bc2d-4cd1-be7c-3f6ecbec59f8` | $12K | 2027-12-31 |
| Rothy's | `001Du000005G40fIAC` | `clq0jrgbn00kl01m8ghcmw67f` | `8677403a-c9e3-4800-b2c8-3477df2d064e` | $11K | 2027-02-16 |
| Lemba | `0014x00000viwSPAAY` | `cm3pz2shq06w501np1yuy5iol` | `18c59364-2bc6-499b-a654-4dee8fa62216` | $11K | 2026-10-21 |
| MarginEdge | `001PQ00000LnvcCYAR` | `cm9n1pmd80ykw01m5bbkdmcv9` | `de1ed4b6-0c01-415c-86fe-5e56634292a9` | $10K | — |
| RaveHealth | `001PQ00000IeflGYAR` | `cm05e7u59013n01n352gir6cb` | `9c7513f6-e811-4833-942a-271d414da30e` | $10K | 2026-09-30 |
| MagicSchool AI | `001PQ00000fwt9OYAQ` | `cmfbox58l1icn01nt6bvlwg3n` | `36121aeb-26d0-4d21-8665-fb8595e63006` | $10K | 2026-11-02 |
| PlaneSense | `001PQ000007tSanYAE` | `clt68ead000js01k55vjqtek8` | `9f592c3a-09cc-47c2-829c-1ad2d99c6fc9` | $10K | 2026-04-30 |
| Tapcast | `0014x00000GNOS5AAP` | `clj65xg94021901klxq2lc2jc` | `fc89c56c-5af4-4601-80a7-7790361ebc31` | $9K | — |
| dolabradigital.com | `001PQ00000CPC8kYAH` | `clvt0722y06tf01p9guf8ow3o` | `c12c585d-bde6-490a-b22f-b8fbedb8737c` | $9K | — |
| Ayala Corporation | `0014x00000DKqcKAAT` | `clnbdv5mf00bm01mm4jkicddd` | `02864763-fddc-48b9-a744-70ef37a00be4` | $9K | 2027-02-02 |
| GovWell | `001PQ00000gjycXYAQ` | `cmfqt7yg31baz01pdd4biteex` | `a19bcf3d-db9d-4ddb-a74c-d4c32053ccfe` | $9K | — |
| Homebound | `0014x00000DKqb2AAD` | `clly67kuc00d101mv4al8rsd9` | `18e7f6c8-5412-4506-8456-3cea2d847d0e` | $8K | — |
| Kapten & Son GmbH | `001PQ00000e0R7gYAE` | `cme6v84lz1o4k01qhw9k57l0y` | `22d4b355-5c8e-47bf-8267-7f1c6088e11f` | $8K | — |
| Tennessee Football | `001PQ00000XSb6UYAT` | `cmb1irpf90jgg01ma1dlcyinm` | `aef3151e-4341-4a7a-afb1-6e397116f58c` | $8K | 2028-06-01 |
| Land Insights | `001PQ00000RYaCqYAL` | `cm68d8gob1yyk01nc9w3l1t82` | `3a954e06-526a-4110-b13b-edb8de01de9e` | $8K | — |
| Bay FC | `001PQ00000PBCaXYAX` | `cm4vxyn670lxu01lctl1hhgyt` | `3a9d9430-9fa9-4f19-8d48-7548bf6b6436` | $8K | 2027-02-02 |
| BioAge Labs | `001Du000002npk0IAA` | `cma6t7x7n078d01jmc0zgsefn` | `336c5f2b-14f9-4727-a648-9f96f0041dff` | $7K | — |
| The Picklr | `001PQ00000hwpvvYAA` | `cmgi1jxov288n01q6yuq3uzhq` | `ca30a482-04da-43f5-8272-23843b0254ed` | $7K | — |
| Dempsey Uniform & Linen | `001PQ00000OnZtFYAV` | `cm4x7wgam0syg01m7kyup3co7` | `b1dcda7d-58bd-4753-940f-10485c7357d6` | $5K | 2027-01-28 |
| Pay.com | `0014x00000NRfQPAA1` | `cmc8pap981zll01ln0su2ly9q` | `6df7890c-52e8-4c11-8727-ce40d7cf66de` | $5K | — |
| uDocz | `001Du000005FMyFIAW` | `clqpdxwwb02qs01k9ip69mcf5` | `5b1c21ef-457c-4869-a6c6-784dd2accab5` | $5K | — |
| TrovaTrip | `0014x000017pHUyAAM` | `clvcghivp013y01ou9su9xbvf` | `fe61fb7b-ca2c-46e3-935c-c942488eff88` | $4K | — |
| Coalesce | `001Du000004brUdIAI` | `cmj8pil8j3g2i01ibmxu1hb2g` | `2cd4e265-eb77-45c8-9298-df04c00b9374` | $4K | — |
| Ardent AI | `001PQ00000NhKpSYAV` | `cmcnpmu5j0l8x01ly0mjxxgdk` | `28b5bd18-494f-4600-b124-25baecafac0f` | $4K | — |
| Workweek | `001PQ00000At4WfYAJ` | `clve8u36c02o101n8b7ctqil9` | `fb62985b-d5b6-4844-8757-33e1b7eb333c` | $4K | — |
| Camperoni, Inc. | `001PQ00000CTnrJYAT` | `clvy14mjc05dr01n2q5s01tlv` | `ed31d880-ccd0-4384-9532-b38aec23baa5` | $3K | — |
| Next Pathway | `001Du000002XE1hIAG` | `clq2ngbm6026001m8jqkao477` | `4114517b-8f71-4212-9161-9ad5e4fdc581` | $3K | — |
| VISORY LLC | `001PQ00000bzeZVYAY` | `cmcywlc6211o401pv3gzrspt0` | `2e08976f-2286-4fb8-bcf3-3b68ae210699` | $3K | — |
| Asimetrix | `001PQ00000cJ6iCYAS` | `cmdt9j7461e5i01phl4yuqhua` | `2469b2c4-f6d2-400c-aadf-4351cdd28bb5` | $1K | — |
| DataBank | `0014x000011c7AQAAY` | `cmmdtu33z2gbm01nxci7cw9tt` | `064f2ccd-b68f-4efb-bbcd-05354e1f4258` | <$1K | — |
| J&R Data | `001PQ00000cPhaCYAS` | `cmdxv8tml2hsh01ms2et00db2` | `4ee90521-696a-4b21-a525-c9fc3e2e988f` | <$1K | — |
| Tracer | `001PQ000009R73SYAS` | `club6q3tx03e201o922b1d9kw` | `d2da0407-90f9-4199-94bf-a218f5c13643` | <$1K | — |
| SpringWorks Therapeutics | `001PQ00000ERgJRYA1` | `cm850f59l035g01ktwh5iwzpe` | `2c568dd9-ab11-4c29-a029-b8af1b7666a9` | $0 | 2027-04-13 |

> **Note**: Cache refreshed 2026-04-15. Full book of business from `CURRENT_ASTRO_CUSTS WHERE OWNER_NAME ILIKE '%kenney%'`. Excludes `amieles_personal` (personal test account). Refresh query: `SELECT ACCT_NAME, ACCT_ID, ORG_ID, METRONOME_ID, TOTAL_ARR_AMT, CONTRACT_END_DATE FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS WHERE OWNER_NAME ILIKE '%kenney%' ORDER BY TOTAL_ARR_AMT DESC NULLS LAST`.

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
| `METRICS_FINANCE.DEPLOYMENT_COST_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Per-deployment cost breakdown. Cost columns: `TOTAL_DEPLOYMENT_COST` (scheduler), `TOTAL_COST` (all-in), `A5_WORKER_COST`, `A20_WORKER_COST`. Runtime columns: `A5_WORKER_RUNTIME_SECONDS`, `A20_WORKER_RUNTIME_SECONDS`, `TOTAL_DEPLOYMENT_RUNTIME_SECONDS`. Add-on columns: `TOTAL_EPHEMERAL_STORAGE_COST`, `TOTAL_REMOTE_EXECUTION_COST`, `TOTAL_OBSERVE_COST`. Filter `DEPLOYMENT_ID != 'no_deployment_id'` to exclude unassigned rows. |
| `METRICS_FINANCE.DEPLOYMENT_REGION_COST_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Cost by cloud region |
| `METRICS_FINANCE.WORKER_QUEUE_COST_MULTI` | `WORKER_QUEUE_ID`, `ORG_ID`, `DEPLOYMENT_ID` | Worker queue cost. GPU runtime columns: `A5_WORKER_RUNTIME_SECONDS`, `A10_WORKER_RUNTIME_SECONDS`, `A20_WORKER_RUNTIME_SECONDS`, `TOTAL_COST`. Use instead of `DEPLOYMENT_COST_MULTI` when you need per-queue GPU hour breakdowns. |
| `METRICS_FINANCE.CLUSTER_COST_MULTI` | `CLUSTER_ID`, `ORG_ID` | Cluster cost |
| `METRICS_FINANCE.METRONOME_USAGE_MULTI` | `METRONOME_ID` | Credit usage vs contract |
| `METRICS_FINANCE.METRONOME_REVENUE_DAILY` | `METRONOME_ID` | Daily revenue |
| `METRICS_ASTRO.ORG_ACTIVITY_MULTI` | `ORG_ID` | Org-level task/DAG activity |
| `METRICS_ASTRO.DEPLOYMENT_ACTIVITY_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Deployment activity |
| `METRICS_ASTRO.DAG_ACTIVITY_DAILY` | `ORG_ID`, `DATE` | Daily DAG metrics |

### Layer 2 — MODEL (cleaned entities)

| Table | What it is |
|---|---|
| `MODEL_ASTRO.USERS` | All users. PK: `USER_ID`. Columns: `EMAIL_DOMAIN`, `STATUS`, `LOGINS_COUNT`, `LAST_LOGIN_TS`, `IS_DELETED`. **No full email stored. Join from SF_CONTACTS via `SF_CONTACTS.ASTRO_USER_ID = USERS.USER_ID`.** Filter `IS_DELETED = FALSE`. |
| `MODEL_ASTRO.USER_ROLES` | User-org role bindings with `EMAIL_DOMAIN`, `ROLE`, `IS_ACTIVE` |
| `MODEL_ASTRO.ORG_USERS` | User↔org membership with role |
| `MODEL_ASTRO.ORGANIZATIONS` | Org entities keyed on `ORG_ID` |
| `MODEL_ASTRO.DEPLOYMENTS` | All deployments |
| `MODEL_ASTRO.TASK_RUNS` | **7.4B rows / 1TB** — always filter by date |
| `MODEL_ASTRO.DAG_RUNS` | **1.5B rows** — always filter by date |
| `MODEL_CRM.SF_CONTACTS` | Salesforce contacts. PK: `CONTACT_ID`. No email column (privacy) — use `CONTACT_URL`. Key columns: `ACCT_ID`, `ACCT_NAME`, `TITLE`, `PRIMARY_DOMAIN`, `CONTACT_STATUS`, `LEAD_SCORE_GRADE`, `SOURCE`, `IS_OPTED_OUT_OF_EMAIL`, `IS_ACTIVE_BILLING_CONTACT`, `IS_BILLING_CONTACT`, `IS_TRIAL_CONTACT`, `OWNER_NAME`, `LAST_ACTIVITY_TS`, `LAST_SALES_ACTIVITY_TS`, `FIRST_MQL_DATE`, `LAST_MQL_DATE`, `LAST_VISITED_PRICING_PAGE_DATE`, `LAST_VISITED_DEBUGGING_AIRFLOW_PAGE_DATE`, `LAST_VISITED_DEBUGGING_DAGS_PAGE_DATE`, `ASTRO_USER_ID` (→ `MODEL_ASTRO.USERS.USER_ID`), `ASTRO_ORG_ID`, `ZD_USER_ID`. Filter `IS_DELETED = FALSE AND IS_EMPLOYEE = FALSE`. |
| `MODEL_CRM.SF_ACCOUNTS` | Salesforce accounts. Key columns: `ACCT_NAME`, `ACCT_ID`, `ACCT_DOMAIN`, `OWNER_NAME`, `INDUSTRY`, `SALES_TEAM` (Commercial/Enterprise/Strategic), `SALES_REGION`, `SEGMENT_PLANNED`, `TOTAL_ARR_AMT`, `SMOKE_SCORE`, `FIRE_SCORE`, `ACCT_SCORE`, `ACCT_SCORE_POSITIVE_DRIVERS`, `ACCT_SCORE_NEGATIVE_DRIVERS`, `ICP_DESIGNATION_V2`, `ACCT_HEALTH`, `IS_CURRENT_CUST`, `IS_CHURNED_CUST`, `CUSTOMER_SINCE_DATE`, `IS_CHURN_RISK`, `NEXT_RENEWAL_DATE`, `LAST_MQL_DATE`, `LAST_COSMOS_DOC_VIEW_DATE`, `LAST_DAG_FACTORY_DOWNLOAD_DATE`, `BILLING_COUNTRY`, `SHIPPING_COUNTRY`, `HG_AIRFLOW/DATABRICKS/MWAA` (boolean tech flags), `ZD_ORG_ID` (direct Zendesk org ID — shortcut for ZD lookups without MAPS join). **No IS_DELETED column** — filter `ACCT_TYPE NOT IN ('Internal','Competitor')`. |
| `MODEL_CRM.SF_OPPS` | Opportunities. `OPP_TYPE`: New Business/Expansion/Renewal/Guided Trial/Churn/Downsell. Stages: `1-Discovery` → `2-QSO & Demo` → `3-EB Meeting` → `4-Tech Workshop/POV` → `5-Negotiate` → `7-Closed Won`/`8-Closed Lost`. Filter active: `IS_OPEN = TRUE`. Key columns: `AMT`, `INCREMENTAL_ARR_AMT`, `TOTAL_ACV`, `NEW_BUSINESS_ACV`, `CLOSE_DATE`, `CREATED_DATE`, `WON_DATE`, `LOST_DATE`, `OWNER_FORECAST_CATEGORY`, `NEXT_STEPS`, `IS_WON`, `IS_LOST`, `LOSS_REASON`, `LOSS_DETAILS`, `COMPETITION`, `CLOUD_PROVIDER`, `LEAD_SOURCE`, `DISCOVERY_MEETING_DATE`, `AIRFLOW_COMMITMENT`, `AIRFLOW_EXPERIENCE`, `CURRENT_AIRFLOW_DEPLOYMENT_MODEL`, `CURRENT_AIRFLOW_VERSIONS`, `CURRENT_AIRFLOW_ENVIRONMENTS_COUNT`. |
| `MODEL_CRM.SF_MQLS` | MQL events. One row per MQL — contacts can have multiple. Key: `CONTACT_ID`, `ACCT_ID`, `MQL_TS`, `REPORTING_CHANNEL` (Webinar/Free Trial/Tradeshow/Paid Social/Paid Search/Field Event/etc), `ASSIGNED_AE_NAME`, `ASSIGNED_SDR_NAME`, `DISQUALIFICATION_REASON`. |
| `MODEL_CRM.SF_USERS` | SF users (reps, CSMs, FEs). `IS_ACTIVE`, `IS_ACCT_EXEC`. `ROLE` examples: `Commercial Sales (AE)`, `Enterprise Sales (AE) - East (Ritchie)`, `Field Engineer - Enterprise`, `CSM`. `SEGMENT`: Commercial/Enterprise/Enterprise+. |
| `MODEL_CRM.SF_RENEWALS` | Renewal opp summary. `ATR_AMT`, `RENEWAL_AMT`, `RENEWAL_OUTCOME`, `ATR_DATE`, `IS_PRODUCT_TRANSITION`. |
| `MODEL_CRM.SF_ASTRO_ORGS` | Maps `ORG_ID` → `ACCT_ID`. Also has `METRONOME_ID` — the bridge between product/billing and CRM. Rich trial/product context: `ASTRO_ORG_STATE`, `FREE_TRIAL_START_DATE`, `TRIAL_EXPIRED_DATE`, `IS_GUIDED_TRIAL_ORG`, `TRIAL_REASON`, `AIRFLOW_COMMITMENT`, `AIRFLOW_PAIN`, `PROPENSITY_TO_PURCHASE`, `DEPLOYMENT_CREATED_DATE`, `FIRST_CODE_PUSH_DATE`, `FIRST_TASK_SUCCESS_DATE`, `FIRST_NON_EXAMPLE_DAG_DATE`, `CLICKED_INSTALL_CLI_BUTTON_DATE`, `ADDED_PAYMENT_METHOD_DATE`, `ASTRO_FREE_TRIAL_CREDIT_USAGE`, `ASTRO_FREE_TRIAL_CREDITS_ISSUED`, `FIRST_VIEWED_PRICING_PAGE_DATE`, `ASTRO_PLAN_UPGRADE_REQUEST`, `SF_RECORD_URL`. Useful for prospect product engagement context. |
| `MODEL_CRM.LF_WEBSITE_VISITS` | Leadfeeder web visits. **FK is `SF_ACCT_ID` (not `ACCT_ID`)** — join to SF_ACCOUNTS on `SF_ACCT_ID = ACCT_ID`. Columns: `LF_VISIT_ID`, `VISIT_TS`, `VISIT_DURATION`, `LANDING_PAGE`, `PAGE_VIEW_COUNT`, `SOURCE`, `MEDIUM`, `CAMPAIGN_NAME`, `REFERRER`. Join to `LF_PAGE_VIEWS` on `LF_VISIT_ID` for page-level detail. |
| `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS` | Gong transcript text. Key columns: `CALL_ID`, `ACCT_ID` (SF account ID — useful for rep-scoped joins), `ACCT_NAME`, `CALL_TITLE`, `CALL_URL`, `SCHEDULED_TS`, `OPP_NAME`, `CALL_BRIEF`, `CALL_NEXT_STEPS`, `ATTENDEES`, `FULL_TRANSCRIPT`. Join to `GONG_CALLS` on `CALL_ID`. **Prefer `ACCT_NAME ILIKE` for single-account lookups; use `ACCT_ID IN (...)` or join to `SF_ACCOUNTS` for rep book-of-business scoping.** ⚠️ **Always scans ~750MB regardless of which columns are selected** — even metadata-only queries (no `FULL_TRANSCRIPT`) scan the full table partition. For metadata-only Gong lookups (title, brief, sentiment), use Pattern 12 (`GONG_CALL_ENRICHMENTS_V` + `GONG_CALLS` join) instead — ~25MB vs 750MB. |
| `MODEL_CRM_SENSITIVE.GONG_CALLS` | Gong call metadata. Key columns: `CALL_ID`, `ACCT_ID`, `IS_DELETED`, `OPP_STAGE_AT_CALL`, `CALL_DURATION`, `CALL_START_TS`, `PRIMARY_EMPLOYEE`, `EMPLOYEE_ARRAY`. Always filter `IS_DELETED = FALSE`. Can filter by `ACCT_ID` for account-scoped lookups (alternative to ACCT_NAME on transcripts). |
| `MODEL_SUPPORT.ZD_TICKETS` | Zendesk tickets. **`ORG_ID` is Zendesk's ORG_ID (NUMBER type), NOT Astro ORG_ID.** Join chain: `ZD_TICKETS.ORG_ID → MAPS.ZD_ORGS.ZD_ORG_ID → ACCT_ID`. Key: `STATUS` (open/pending/hold/solved/closed), `PRIORITY` (p1-p4), `TYPE` (question/incident/problem/task), `PRODUCT`, `IS_ESCALATED`, `BUSINESS_IMPACT`, `CUSTOMER_SENTIMENT`. |
| `MODEL_SUPPORT.ZD_TICKET_COMMENTS` | Ticket thread. `BODY`, `IS_EMPLOYEE`. Join on `TICKET_ID`. Use `IS_EMPLOYEE = FALSE` for customer-only comments. |
| `MODEL_SUPPORT.ZD_ORGS` | Raw Zendesk org data. `ORG_ID`, `ORG_NAME`, `DOMAIN_NAMES` (array — use `LATERAL FLATTEN` for domain matching), `IS_DELETED`. Different schema from `MAPS.ZD_ORGS` — use this for domain-based ZD org resolution. |
| `MODEL_CRM.SF_ACCOUNT_DOMAINS` | Domain→account mapping. `ACCT_ID`, `EMAIL_DOMAIN`, `IS_UNIQUE_DOMAIN`. Use `IS_UNIQUE_DOMAIN = TRUE` to avoid false matches on shared domains (e.g. gmail.com). |
| `MODEL_ASTRO.ORGANIZATIONS` | Org metadata. **FK to SF is `SF_ACCT_ID` (not `ACCT_ID`)** — naming inconsistency vs all other tables. Has `PRODUCT_TIER` (trial/paygo/team/enterprise/etc), `IS_TRIAL`, `IS_POV`, `IS_OBSERVE_ENABLED`, `METRONOME_ID`. Filter `IS_DELETED = FALSE AND IS_INTERNAL = FALSE`. |
| `MODEL_ASTRO.DEPLOYMENTS` | Deployment config. `EXECUTOR` (Celery/Astro/Kubernetes/Stellar), `SCHEDULER_SIZE` (small/medium/large), `CLUSTER_TYPE` (HOSTED/SHARED/BRING_YOUR_OWN_CLOUD), `AIRFLOW_VERSION`, `CLOUD_PROVIDER` (aws/gcp/azure), `REGION` (e.g. `us-east-1`, `eu-west-1`), `IS_REMOTE_EXECUTION_ENABLED`, `HAS_CICD_ENFORCEMENT`, `RESILIENCY`. Filter `IS_DELETED = FALSE`. |
| `MODEL_ASTRO.CLUSTERS` | Cluster metadata. `CLUSTER_ID`, `CLOUD_PROVIDER`, `REGION`, `CLUSTER_TYPE`, `IS_DELETED`. Join to `MODEL_ASTRO.ORGANIZATIONS` via `CLUSTER_ID` to resolve org → cluster. |
| `MODEL_CONTRACTS.SF_CUST_CONTRACTS` | Contract terms per opp. `BASE_RATE`, `ON_DEMAND_RATE`, `RESERVED_CAPACITY`, `IS_ANNUAL`, `IS_M2M`, `ASTRO_ORG_ID`. Filter `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE` for current terms. More granular than `ACCT_PRODUCT_ARR`. |
| `MODEL_ECOSYSTEM.SCARF_COMPANY_ARTIFACT_EVENTS` | OSS download signals by company domain. `COMPANY_NAME`, `COMPANY_DOMAIN`, `ARTIFACT_NAME`, `EVENT_COUNT`, `IS_COSMOS_DOCS_PAGE_VIEW`, `IS_DAG_FACTORY_DOWNLOAD`. No direct SF join — match via domain → `SF_ACCOUNT_DOMAINS`. Good for prospecting. |
| `MODEL_EDU.SKILLJAR_COURSE_PROGRESS` | Training completion. `STUDENT_ID`, `COURSE_NAME`, `IS_COMPLETED`, `IS_CERTIFICATION`, `DAYS_TO_COMPLETE`, `COMPLETED_AT_TS`. Good for onboarding health. Join to `SKILLJAR_STUDENTS` on `STUDENT_ID`. |
| `MODEL_EDU.SKILLJAR_STUDENTS` | Skilljar user registry. `STUDENT_ID`, `EMAIL_DOMAIN`, `IS_EMPLOYEE`. **No individual contact ID — only domain-level linkage to SF contacts.** Filter `IS_EMPLOYEE = FALSE`. |
| `MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES` | **Schema discovery tool.** `TABLE_FQID`, `TABLE_SIZE_GB`, `IS_STALE`, `PRIMARY_KEY`, `FOREIGN_KEY`. Query before running against unknown large tables. |
| `GTM.PUBLIC.CONTACT_360_V` | **Unified contact view** — SF contacts + product user status + MQL history + domain-level Skilljar training. Columns: `CONTACT_ID`, `ACCT_ID`, `ACCT_NAME`, `TITLE`, `CONTACT_URL`, `PRIMARY_DOMAIN`, `CONTACT_STATUS`, `LEAD_SCORE_GRADE`, `IS_OPTED_OUT_OF_EMAIL`, `IS_ACTIVE_BILLING_CONTACT`, `IS_PRODUCT_USER`, `PRODUCT_STATUS`, `LOGINS_COUNT`, `LAST_LOGIN_TS`, `MQL_COUNT`, `LAST_MQL_TS`, `LAST_MQL_CHANNEL`, `LAST_ASSIGNED_AE`, `DOMAIN_COURSES_COMPLETED`, `DOMAIN_HAS_CERTIFICATION`. Filter by `ACCT_ID` or `ACCT_NAME ILIKE`. No joins needed. Created 2026-04-08. **Note:** Gong sentiment not joinable here (no name column in SF_CONTACTS) — use `CONTACT_SENTIMENT_V` separately. |
| `GTM.PUBLIC.CONTACT_SENTIMENT_V` | Pre-built Gong sentiment view. Columns: `contact_name`, `ACCT_NAME`, `avg_sentiment`, `call_count`, `contact_role` (Champion/Skeptic/At Risk), `sentiment_direction`. Use for rep-level contact health — no joins needed. Note: `GTM.GONG.*` tables do NOT exist; only `GTM.PUBLIC.*` views are accessible. |
| `GTM.PUBLIC.CONTACT_NOTES` | Per-contact notes log (analogous to `ACCOUNT_NOTES` for individuals). Columns: `NOTE_ID`, `CONTACT_NAME`, `NOTE_DATE`, `NOTE_TYPE`, `CONTENT`, `SOURCE`, `CREATED_AT`. Filter by `ACCT_ID` to get all contact notes for an account. |
| `GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V` | Cortex-enriched Gong call view. Columns: `CALL_ID`, `ACCT_ID`, `ACCT_NAME`, `CALL_DATE`, `SENTIMENT_SCORE`, `DEAL_RISK`, `TECH_STACK`, `PAIN_POINTS`, `COMPETITORS`, `AIRFLOW_TOPICS`. Join to `HQ.MODEL_CRM_SENSITIVE.GONG_CALLS` on `CALL_ID` to get `CALL_TITLE`, `CALL_URL`, `CALL_BRIEF`, `CALL_NEXT_STEPS`, `PRIMARY_EMPLOYEE`, `CALL_DURATION`. Filter by `ACCT_ID` for account-scoped lookups. |
| `GTM.PUBLIC.ZD_TICKET_ENRICHMENTS_V` | Cortex-enriched Zendesk ticket view. Columns: `TICKET_ID`, `ACCT_ID`, `TICKET_DATE`, `PRIORITY`, `STATUS`, `SENTIMENT_SCORE`, `ISSUE_CATEGORY`, `URGENCY_SIGNAL`, `KEY_PHRASES`, `PRODUCT_AREA`. Filter by `ACCT_ID` (SF account ID). No joins needed for account-level ticket summaries. |
| `HQ.MODEL_CRM.SF_CAMPAIGN_MEMBERS` | Campaign membership and engagement. Columns: `ACCT_ID`, `CONTACT_ID`, `CAMPAIGN_ID`, `STATUS`, `HAS_RESPONDED`, `CREATED_TS`, `FIRST_RESPONDED_TS`, `JOB_TITLE`, `COMPANY_OR_ACCOUNT`, `WEBINAR_NAME`, `FUNNEL_NAME`, `EBOOK_NAME`, `UTM_SOURCE`, `UTM_CAMPAIGN`, `MQL_QUALIFICATION_DATE`, `ASSIGNED_AE_NAME`, `ASSIGNED_SDR_NAME`, `REPORTING_CHANNEL`, `OPP_ID`, `CAMPAIGN_MEMBER_EMAIL_DOMAIN`. Join to `SF_CAMPAIGNS` on `CAMPAIGN_ID` for campaign metadata. Filter by `ACCT_ID` for account-level campaign history, `CONTACT_ID` for contact-level, or `CAMPAIGN_MEMBER_EMAIL_DOMAIN` for domain-based lookups (useful for prospects without an ACCT_ID yet). |
| `HQ.MODEL_CRM.SF_CAMPAIGNS` | Campaign definitions. Columns: `CAMPAIGN_ID`, `CAMPAIGN_NAME`, `TYPE`. Join key for `SF_CAMPAIGN_MEMBERS`. |
| `HQ.MODEL_CRM.LF_PAGE_VIEWS` | Individual page view events within a Leadfeeder visit. Columns: `LF_VISIT_ID`, `PAGE_URL`, `PAGE_NAME`, `PAGEVIEW_TS`. Join to `LF_WEBSITE_VISITS` on `LF_VISIT_ID` for page-level detail. |
| `GTM.PUBLIC.ACCOUNT_RESEARCH_LATEST_V` | Latest account research report per account (one row per ACCT_ID). Columns: `RESEARCH_ID`, `ACCT_ID`, `ACCT_NAME`, `RESEARCH_DATE`, `SCORE`, `GRADE`, `CONFIDENCE`, `MC_GRADE`, `SOURCES_USED` (JSON), `REPORT_MD` (full markdown report), `CREATED_AT`, `DAYS_SINCE_RESEARCH`, `IS_STALE`. Filter by `ACCT_ID` or `ACCT_NAME ILIKE`. Check `IS_STALE` and `DAYS_SINCE_RESEARCH` to decide whether to re-run research. |
| `MAPS.ZD_ORGS` | Zendesk org → SF account. `ZD_ORG_ID`, `ZD_ORG_NAME`, `ACCT_ID`, `ACCT_NAME`. Filter `IS_DELETED = FALSE`. |
| `MAPS.ZD_ACCTS` | SF account → Zendesk orgs (reverse). `ACCT_ID`, `ZD_ORG_MAP` (array). |
| `MODEL_FINANCE.METRONOME_CONTRACTS` | Billing contracts. `PLAN_TYPE`: contract/paygo/trial/pov/internal. `IS_ACTIVE`, `START_TS`, `END_TS`, `RATE_CARD_ID`. Join via `METRONOME_ID`. |
| `MODEL_FINANCE.METRONOME_INVOICES` | Invoices. Filter `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE` for real revenue. `INV_TYPE`: usage/plan_arrears/scheduled/credit_purchase. `TOTAL_AMT`, `PERIOD_START_DATE`, `PERIOD_END_DATE`. |
| `MODEL_FINANCE.METRONOME_CREDIT_GRANTS` | Prepaid credits. `GRANTED_AMT`, `CURRENT_BALANCE_AMT`, `EXPIRED_AMT`. `IS_CONTRACT_CREDIT`, `IS_ACTIVE`, `EFFECTIVE_DATE`, `EXPIRATION_DATE`. Links to SF via `SF_OPP_ID`. |
| `MODEL_FINANCE.METRONOME_CREDITS_DAILY` | Daily credit burn. `CREDIT_DATE`, `DEDUCTED_AMT`, `PERIOD_CREDIT_AMT_CUMULATIVE`. Best for burn rate trends. |
| `MODEL_FINANCE.METRONOME_USAGE_DAILY` | Daily usage billing. **Always filter `IS_LATEST = TRUE`** to avoid snapshot double-counting. `USAGE_AMT`, `BILL_AMT`, `PERIOD_USAGE_AMT_CUMULATIVE`. |
| `MODEL_FINANCE.METRONOME_RATE_CARDS` | Rate card definitions. Columns: `RATE_CARD_NAME`, `PLAN_TYPE`, `SUPPORT_LEVEL`, `IS_UPLIFTED`, `AVG_UPLIFT_PCT`. Use to discover valid rate card names before querying `METRONOME_RATE_CARD_ITEMS`. |
| `MODEL_FINANCE.METRONOME_RATE_CARD_ITEMS` | Per-item rates within each rate card. Key columns: `RATE_CARD_NAME`, `PRODUCT_ITEM_NAME`, `PRICING_GROUP_TYPE`, `PRICING_GROUP_OBJECT_HASH`, `SUPPORT_LEVEL`, `UNIT_PRICE`, `UPLIFT_PCT`, `RATE_TYPE`, `IS_TIERED`, `IS_COMPOSITE`, `IS_ACTIVE`. Filter `IS_ACTIVE = TRUE AND IS_COMPOSITE = FALSE` for atomic per-unit rates; composite rows are bundles and inflate results. |
| `MODEL_FINANCE.METRONOME_PRODUCTS` | Product definitions. Undocumented schema — use `SELECT * LIMIT 50` to discover columns on demand. |
| `MODEL_FINANCE.METRONOME_RATE_CARD_ITEM_UPLIFT_LOG` | Uplift change log for rate card items. **`RATE_CARD_NAME` is NOT a valid column** (query error confirmed). Valid columns: `SUPPORT_LEVEL`, `PRODUCT_ITEM_NAME`, `UPLIFT_PCT`, `UNIT_PRICE`, `START_TS`, `END_TS`. |

### Layer 1 — IN (raw ingested)

| Table | What it is |
|---|---|
| `IN_ASTRO_DB_PROD.ORG_USER_RELATION` | Raw user↔org with `DELETED_AT` |
| `IN_ASTRO_DB_PROD.ORGANIZATION` | Raw org with `BILLING_EMAIL` |
| `IN_ASTRO_DB_PROD.USER_INVITE` | User invite records |

---

## Table Selection Decision Tree

Use this before writing any query. Pick the first table that satisfies the question.

**"Give me a full account snapshot / everything about this account"**
→ `GTM.PUBLIC.ACCOUNT_360_V` — single query, one row per account, all signals pre-joined  
→ Returns: ARR, usage, contract, Gong sentiment, deal risk, ZD tickets, contact count, LF visits, research tier  
→ Also has `RESEARCH_DATE`, `RESEARCH_IS_STALE`, `OWNER_NAME` — usable directly for research-cron eligibility checks (e.g. `WHERE OWNER_NAME ILIKE '%kenney%' AND (RESEARCH_DATE IS NULL OR RESEARCH_IS_STALE = TRUE)`)  
→ ⚠️ Column names use `ACCT_*` pattern — NOT `ACCOUNT_*`: use `ACCT_NAME`, `ACCT_ID`, `TOTAL_ARR_AMT`. `ACCOUNT_NAME`/`SF_ACCT_ID`/`ARR`/`STAGE`/`OWNER` are NOT valid columns (silent error, 0 rows)

**"What's the history / what have we discussed with this account? / What notes exist?"**
→ `GTM.PUBLIC.ACCOUNT_NOTES` — filter by `ACCT_ID`, `ORDER BY NOTE_DATE DESC LIMIT 20`  
→ Types: `interaction` (ad-hoc conversations), `prep_brief` (pre-call briefs), `email_draft`, `call_brief`, `ad_hoc`  
→ ⚠️ Filter column is `ACCT_ID` only — `ACCOUNT_NAME` and `ACCT_NAME` are NOT valid columns in this table (silent failure, 0 rows, 0 bytes scanned)

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

**"Who are the contacts for an account? (titles, MQL history, product status, training)"**
→ `GTM.PUBLIC.CONTACT_360_V` — filter by `ACCT_ID` or `ACCT_NAME ILIKE`, no joins needed  
→ Fallback for raw product users: `IN_ASTRO_DB_PROD.ORG_USER_RELATION` + `MODEL_ASTRO.USERS`

**"Who are the users on this account?"**
→ `GTM.PUBLIC.CONTACT_360_V` (preferred — includes product status, MQL, training in one query)  
→ Or: `IN_ASTRO_DB_PROD.ORG_USER_RELATION` + `MODEL_ASTRO.USERS` + `SF_CONTACTS` (3-table join, use only if you need raw product user data not in CONTACT_360_V)

**"What's happening in Gong / what was discussed?"**
→ For enriched summary (sentiment, deal risk, tech stack): `GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V` filter by `ACCT_ID`, JOIN `GONG_CALLS` on `CALL_ID` for title/URL/brief  
→ For full transcripts: `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS` JOIN `GONG_CALLS` on `CALL_ID`, filter `IS_DELETED = FALSE`

**"What support tickets does this account have?"**
→ For enriched summary (sentiment, urgency, category): `GTM.PUBLIC.ZD_TICKET_ENRICHMENTS_V` filter by `ACCT_ID` — no joins needed  
→ For raw tickets: `MODEL_SUPPORT.ZD_TICKETS` — bridge via `ZD_TICKETS.ORG_ID → MAPS.ZD_ORGS.ZD_ORG_ID → ACCT_ID` (or use `SF_ACCOUNTS.ZD_ORG_ID` shortcut)

**"Has this account been researched before? What was the fit score / grade?"**
→ `GTM.PUBLIC.ACCOUNT_RESEARCH_LATEST_V` — filter by `ACCT_ID` or `ACCT_NAME ILIKE`  
→ Returns: `SCORE`, `GRADE`, `MC_GRADE`, `CONFIDENCE`, `DAYS_SINCE_RESEARCH`, `IS_STALE`, full `REPORT_MD`  
→ Check `IS_STALE = FALSE AND DAYS_SINCE_RESEARCH <= 14` before deciding whether to re-research

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

**For accounts in the ID cache above: skip the CTE — use `ORG_ID` directly.**

For unknown accounts, resolve via CTE first:

```sql
-- Known account (use ID cache): skip CTE entirely
SELECT DATE, TOTAL_COST
FROM HQ.METRICS_FINANCE.ORG_COST_MULTI
WHERE ORG_ID = 'cl6e1hc82009l0s0ebuei60ec'  -- Third Point
  AND TIME_GRAIN = 'day'
  AND DATE = CURRENT_DATE - 1

-- Unknown account: resolve via CTE
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

### Pattern 2: Contacts/users for an account — ALWAYS include names

**Always join `HQ.MODEL_ASTRO_PII.USERS` for `FULL_NAME` and `EMAIL`** — names are stripped from all other tables. This is required on every user/contact list output.

```sql
-- Preferred: CONTACT_360_V + PII join for names
SELECT
    p.FULL_NAME,
    p.EMAIL,
    c.TITLE,
    c.CONTACT_STATUS,
    c.LEAD_SCORE_GRADE,
    c.IS_PRODUCT_USER,
    c.PRODUCT_STATUS,
    c.LOGINS_COUNT,
    c.LAST_LOGIN_TS,
    c.IS_OPTED_OUT_OF_EMAIL,
    c.MQL_COUNT,
    c.LAST_MQL_TS,
    c.LAST_MQL_CHANNEL,
    c.CONTACT_URL
FROM GTM.PUBLIC.CONTACT_360_V c
LEFT JOIN HQ.MODEL_ASTRO_PII.USERS p ON p.USER_ID = c.ASTRO_USER_ID
WHERE c.ACCT_NAME ILIKE '%CUSTOMER_NAME%'
ORDER BY c.IS_PRODUCT_USER DESC, c.LOGINS_COUNT DESC NULLS LAST
```

For raw product users only (when CONTACT_360_V is overkill):
```sql
-- Join key: SF_CONTACTS.ASTRO_USER_ID = MODEL_ASTRO.USERS.USER_ID
WITH acct AS (
    SELECT ORG_ID FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
    WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
)
SELECT DISTINCT
    p.FULL_NAME, p.EMAIL,
    ou.USER_ID, ou.ROLE, u.EMAIL_DOMAIN, u.STATUS,
    c.CONTACT_URL, c.TITLE
FROM HQ.IN_ASTRO_DB_PROD.ORG_USER_RELATION ou
JOIN HQ.MODEL_ASTRO.USERS u ON ou.USER_ID = u.USER_ID
LEFT JOIN HQ.MODEL_ASTRO_PII.USERS p ON p.USER_ID = u.USER_ID
LEFT JOIN HQ.MODEL_CRM.SF_CONTACTS c
    ON c.ASTRO_USER_ID = u.USER_ID
    AND c.IS_DELETED = FALSE
JOIN acct a ON ou.ORGANIZATION_ID = a.ORG_ID
WHERE ou.DELETED_AT IS NULL
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

### Pattern 11: Domain-based contact/account fallback

Use when you have an email domain but no direct SF link (e.g., product users not yet in Salesforce):

```sql
-- Domain → account
SELECT ACCT_ID, EMAIL_DOMAIN
FROM HQ.MODEL_CRM.SF_ACCOUNT_DOMAINS
WHERE EMAIL_DOMAIN = 'example.com'
  AND IS_UNIQUE_DOMAIN = TRUE  -- exclude shared domains (gmail.com etc.)

-- Domain → all SF contacts at that account
SELECT c.CONTACT_ID, c.TITLE, c.CONTACT_URL, c.PRIMARY_DOMAIN
FROM HQ.MODEL_CRM.SF_CONTACTS c
JOIN HQ.MODEL_CRM.SF_ACCOUNT_DOMAINS d
    ON c.PRIMARY_DOMAIN = d.EMAIL_DOMAIN
WHERE d.EMAIL_DOMAIN = 'example.com'
  AND d.IS_UNIQUE_DOMAIN = TRUE
  AND c.IS_DELETED = FALSE
  AND c.IS_EMPLOYEE = FALSE
```

### Pattern 12: Gong enrichment with call detail

Preferred pattern for account call research — enrichment view first, then join for full metadata:

```sql
SELECT
    e.CALL_DATE, e.SENTIMENT_SCORE, e.DEAL_RISK,
    e.TECH_STACK, e.PAIN_POINTS, e.COMPETITORS, e.AIRFLOW_TOPICS,
    c.CALL_TITLE, c.CALL_URL, c.CALL_BRIEF, c.CALL_NEXT_STEPS,
    c.PRIMARY_EMPLOYEE, c.CALL_DURATION
FROM GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V e
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON e.CALL_ID = c.CALL_ID
WHERE e.ACCT_ID = '<acct_id>'
  AND c.IS_DELETED = FALSE
ORDER BY e.CALL_DATE DESC
```

---

### Pattern 13: Full account 360 snapshot (single query)

Single-row account context — joins CURRENT_ASTRO_CUSTS with Gong, ZD, contacts, LF visits, and research:

```sql
SELECT ACCT_NAME, TOTAL_ARR_AMT, USAGE_AMT_30D, CREDIT_BALANCE,
       CONTRACT_END_DATE, DAYS_TO_RENEWAL, USAGE_VS_CONTRACT_TARGET_PCT_30D,
       LAST_CALL_DATE, LAST_GONG_SENTIMENT, LAST_DEAL_RISK, LAST_PAIN_POINTS, CALL_COUNT_90D,
       OPEN_TICKET_COUNT, P1_OPEN_COUNT, LAST_TICKET_DATE,
       CONTACT_COUNT, PRODUCT_USER_COUNT, DOMAIN_HAS_CERTIFICATION,
       VISITS_30D, LAST_VISIT_DATE,
       RESEARCH_SCORE, RESEARCH_TIER, KEY_SIGNALS
FROM GTM.PUBLIC.ACCOUNT_360_V
WHERE ACCT_NAME ILIKE '%account_name%'
```

For ID-cache accounts, use `WHERE ACCT_ID = '<acct_id>'` (faster).

---

### Pattern 14: Account history / interaction notes

All Claude-generated and cron-generated notes for an account, newest first:

```sql
SELECT NOTE_DATE, NOTE_TYPE, SOURCE, CONTENT
FROM GTM.PUBLIC.ACCOUNT_NOTES
WHERE ACCT_ID = '<acct_id>'   -- ACCT_ID only; ACCOUNT_NAME / ACCT_NAME are not valid columns here
ORDER BY NOTE_DATE DESC, CREATED_AT DESC
LIMIT 20
```

Filter by note type: `AND NOTE_TYPE IN ('interaction', 'prep_brief', 'call_brief', 'email_draft', 'ad_hoc')`

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

15. **`METRONOME_COMPUTE_EVENTS` has no cost column**: Must join to `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH` and compute `COMPUTE_RUNTIME_SECONDS / 3600 * UNIT_PRICE`. Always scope `RATE_CARD_ITEMS` to the customer's specific `RATE_CARD_ID` first — otherwise you pull prices from other rate cards. Use `ASTRO_ORG_ID` (not `ORGANIZATION_ID`) to filter. `METRONOME_RATE_CARD_ITEMS` has a `PRICING_GROUP_OBJECT_DEFINITION` column — use `LIKE '%small%'` (or the desired scheduler size) to filter to specific rates without JSON parsing. `METRONOME_DEPLOYMENT_EVENTS` has both `EVENT_TS` and `START_TIMESTAMP` date columns — both work for date range filtering. `DEPLOYMENT_COST_MULTI` can be filtered by `METRONOME_ID` in addition to `ORG_ID`. **Always add `IS_COMPOSITE = FALSE`** when querying `METRONOME_RATE_CARD_ITEMS` for per-unit prices — composite rows are bundled rollups and will inflate results.

19. **`METRONOME_DEPLOYMENT_EVENTS` key columns for pricing lookup**: `SCHEDULER_SIZE`, `IS_HA`, `REGION`, `CLOUD_PROVIDER`, `RATE_CARD_ID`, `PRICING_GROUP_OBJECT_HASH`. Join to `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH AND RATE_CARD_ID` to get per-hour `UNIT_PRICE` — multiply by 730 for monthly estimate.

20. **`METRONOME_COMPUTE_EVENTS` key columns for worker pricing**: `WORKER_SIZE` (values: `a5`, `a10`, `a20`, `a40` — lowercase), `REGION`, `CLOUD_PROVIDER`, `IS_REMOTE_EXECUTION`, `PRICING_GROUP_OBJECT_HASH`. Note: case matters — worker sizes are lowercase in this table (`a5` not `A5`).

21. **`METRONOME_CLUSTER_EVENTS` key columns**: `CLUSTER_ZONE_TYPE`, `CLUSTER_TYPE`, `REGION`, `CLOUD_PROVIDER`, `PRICING_GROUP_OBJECT_HASH`. Use for dedicated cluster pricing lookup; `CLUSTER_TYPE = 'dedicated'` filters to BYOC/dedicated zones.

22. **`MODEL_FINANCE.METRONOME_ID_PRICE_LOG` exists** — confirmed via `SELECT * LIMIT 3`; appears to be a price history log. Schema needs discovery via `SELECT * LIMIT 50` before use.

16. **`DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` requires `TIME_GRAIN = 'day'`**: The table stores day, roll_7d, roll_30d, and week rows for every period. Omitting this filter inflates counts by 40–50x. **Always include `TIME_GRAIN = 'day'` (or the intended grain explicitly).**

17. **Prefer GTM enrichment views over raw joins for Gong/ZD/contacts**: `GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V`, `ZD_TICKET_ENRICHMENTS_V`, `CONTACT_360_V`, and `CONTACT_SENTIMENT_V` replace 3–5 manual join steps each. Always check the Decision Tree — if a GTM view covers the question, use it first. Fall back to raw `GONG_CALL_TRANSCRIPTS` / `ZD_TICKETS` / `SF_CONTACTS` only when you need data not in the views (e.g. full transcript text, raw ticket comments).

18. **Push account filter into every CTE in multi-CTE scorecards**: When building a scorecard or report across multiple enrichment views, always pre-filter inside each CTE — add `WHERE ACCT_ID IN (SELECT ACCT_ID FROM my_accounts)` before any `GROUP BY`. Never let a GTM view (`GONG_CALL_ENRICHMENTS_V`, `ZD_TICKET_ENRICHMENTS_V`, etc.) scan all accounts to then join down to a 47-account book-of-business. Omitting this filter caused a 2.87GB scan (vs ~5–10MB expected). `ZD_TICKET_ENRICHMENTS_V` already has `ACCT_ID` — filter it directly, no `MAPS.ZD_ORGS` bridge needed.

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
- `PROJECTED_OVERAGE_TAG`, `CREDIT_EXHAUSTION_TAG` — string tags set when overage/exhaustion is projected; filter `IS NOT NULL` to find at-risk accounts
- `CREDIT_CONSUMED_AMT` — credits consumed to date in current contract period
- `CONTRACT_GRANTED_AMT` — total contract credit amount
- `LICENSE_CONSUMED_PCT` — fraction of contract consumed (0–1); multiply by 100 for percentage
- `PROJECTED_CREDITS_CONSUMED_30D` — projected total credits consumed by period end (30d run rate)
- `PROJECTED_OVERAGE_AMT_30D` — projected overage dollar amount at 30d run rate
- `PROJECTED_OVERAGE_PCT_30D` — projected overage as % of contract

**Pay-Go Specific** (filter `PLAN_TYPE = 'paygo'`)
- `PLAN_TYPE` — `'paygo'` or `'contract'` — top-level billing type on CURRENT_ASTRO_CUSTS
- `BILLING_PROVIDER_TYPE` — billing system identifier for the account
- `PAYGO_BILLED_AMT_TO_DATE` — cumulative pay-go billing amount in current period
- `PROJECTED_PAYGO_CONTRACT_AMT_30D` — projected total pay-go charge at 30d run rate
- `USAGE_AMT_30D_LAG` — usage amount from the prior 30d window (for trend comparison)
- `USAGE_GROWTH_PCT_30D` — MoM usage growth rate (current 30d vs prior 30d); multiply by 100 for %
- `PROJECTED_PAYGO_CONTRACT_TAG` — string tag (non-null) when account is projected to exceed pay-go threshold

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
Values: Active, Inactive, Former Customer, No Engagement

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
**2026-04-06** — 3 substantive queries observed (Gong ATTENDEES sample + GTM sentiment view exploration):
- `GTM.PUBLIC.CONTACT_SENTIMENT_V` confirmed working: columns `contact_name`, `ACCT_NAME`, `avg_sentiment`, `call_count`, `contact_role` (Champion/Skeptic/At Risk), `sentiment_direction`; pre-built view, no joins needed; `GTM.GONG.*` tables do NOT exist (only `GTM.PUBLIC.*` views are accessible in GTM database)
- `GONG_CALL_TRANSCRIPTS.ACCT_ID` confirmed: can join directly to `SF_ACCOUNTS.ACCT_ID` for rep book-of-business scoping; however the join scanned 785MB for LIMIT 3 — prefer `ACCT_NAME ILIKE` for single-account lookups; use `ACCT_ID` join only when filtering across a rep's full book
**2026-04-07** — 40 queries observed (account-research skill sessions for ZebraFox/Elutions prospects + credit alert cron):
- Four new tables confirmed: `MODEL_CRM.SF_CAMPAIGN_MEMBERS` (campaign engagement — filter by `ACCT_ID`; join `SF_CAMPAIGNS` on `CAMPAIGN_ID`), `MODEL_CRM.SF_CAMPAIGNS` (`CAMPAIGN_ID`, `CAMPAIGN_NAME`, `TYPE`), `MODEL_CRM.LF_PAGE_VIEWS` (page-level detail; join `LF_WEBSITE_VISITS` on `LF_VISIT_ID`), `GTM.PUBLIC.ZD_TICKET_ENRICHMENTS_V` (Cortex-enriched ZD view; filter by `ACCT_ID`; columns: `SENTIMENT_SCORE`, `ISSUE_CATEGORY`, `URGENCY_SIGNAL`, `KEY_PHRASES`, `PRODUCT_AREA`)
- `GTM.PUBLIC.GONG_CALL_ENRICHMENTS_V` full schema confirmed: `ACCT_ID`, `CALL_DATE`, `SENTIMENT_SCORE`, `DEAL_RISK`, `TECH_STACK`, `PAIN_POINTS`, `COMPETITORS`, `AIRFLOW_TOPICS`; `ACCT_ID` filter works and is faster than `ACCT_NAME` when ACCT_ID is known; join `GONG_CALLS` on `CALL_ID` for title/URL/brief/next_steps
- New undocumented columns added to existing tables: `SF_CONTACTS` engagement fields (`LEAD_SCORE_GRADE`, `IS_OPTED_OUT_OF_EMAIL`, `LAST_ACTIVITY_TS`, `LAST_VISITED_PRICING_PAGE_DATE`); `SF_OPPS` deal-context fields (`IS_WON/IS_LOST`, `LOSS_REASON`, `COMPETITION`, `AIRFLOW_COMMITMENT/EXPERIENCE`, `TOTAL_ACV`); `SF_ASTRO_ORGS` trial/product fields (`AIRFLOW_COMMITMENT`, `PROPENSITY_TO_PURCHASE`, `FIRST_TASK_SUCCESS_DATE`, `ASTRO_FREE_TRIAL_CREDIT_USAGE`); `SF_ACCOUNTS` ICP/scoring fields (`ACCT_DOMAIN`, `ICP_DESIGNATION_V2`, `ACCT_SCORE`, `IS_CHURNED_CUST`); `GONG_CALLS` new fields (`CALL_START_TS`, `EMPLOYEE_ARRAY`); `CURRENT_ASTRO_CUSTS` overage fields (`PROJECTED_OVERAGE_TAG`, `CREDIT_EXHAUSTION_TAG`)
**2026-04-08** — Rate card analysis session + prospect research cron (28 queries, 1 error):
- Three new `MODEL_FINANCE` tables added to schema: `METRONOME_RATE_CARDS` (columns: `RATE_CARD_NAME`, `PLAN_TYPE`, `SUPPORT_LEVEL`, `IS_UPLIFTED`, `AVG_UPLIFT_PCT`), `METRONOME_RATE_CARD_ITEMS` (full column set confirmed — add `IS_COMPOSITE = FALSE` filter when querying per-unit prices; composite rows are bundles), `METRONOME_PRODUCTS` (schema undiscovered — use `SELECT * LIMIT 50`)
- `METRONOME_RATE_CARD_ITEM_UPLIFT_LOG`: `RATE_CARD_NAME` is NOT a valid column (confirmed query error); valid columns are `SUPPORT_LEVEL`, `PRODUCT_ITEM_NAME`, `UPLIFT_PCT`, `UNIT_PRICE`, `START_TS`, `END_TS`
- Prospect research cron confirmed running clean across 9 accounts: `SF_ACCOUNTS ILIKE` → `ACCT_ID` → `GONG_CALLS WHERE ACCT_ID = '...' AND IS_DELETED = FALSE ORDER BY CALL_START_TS DESC`; all sub-0.7s; this metadata-only pattern (no transcript join) is the right first step before deciding whether to fetch full transcripts
**2026-04-08 (optimization session)** — Schema/linkage optimization pass. Key changes:
- `GTM.PUBLIC.CONTACT_360_V` created: unified contact view joining `SF_CONTACTS` + `MODEL_ASTRO.USERS` (via `SF_CONTACTS.ASTRO_USER_ID = USERS.USER_ID`) + `SF_MQLS` (via `CONTACT_ID`) + `SKILLJAR_STUDENTS/COURSE_PROGRESS` (domain-level only — no individual ID link exists). Created with `GTMUSER` role via Python connector (MCP tool doesn't persist `USE ROLE` across calls; personal databases don't support views).
- `MODEL_ASTRO.USERS` full schema confirmed: `USER_ID` (PK), `EMAIL_DOMAIN`, `STATUS`, `LOGINS_COUNT`, `LAST_LOGIN_TS`, `IS_DELETED`. No `ASTRO_USER_ID` column — join from SF_CONTACTS using `SF_CONTACTS.ASTRO_USER_ID = USERS.USER_ID`.
- `MODEL_CRM.SF_CONTACTS` full schema confirmed: `CONTACT_ID` (PK/TEXT), `ACCT_ID`, `ACCT_NAME`, `ASTRO_ORG_ID`, `ZD_USER_ID` (new columns vs prior doc). `IS_EMPLOYEE` filter needed — view excludes internal contacts.
- `MODEL_EDU.SKILLJAR_STUDENTS` confirmed: `STUDENT_ID`, `EMAIL_DOMAIN`, `IS_EMPLOYEE` only — no contact-level ID link to SF. Domain-level aggregation is the only join path.
- Decision tree updated: `CONTACT_360_V` is now the first-choice for contact queries; GTM enrichment views (`GONG_CALL_ENRICHMENTS_V`, `ZD_TICKET_ENRICHMENTS_V`) are first-choice for Gong/ZD context.
- Pattern 1 updated to show direct `ORG_ID` usage for ID-cache accounts vs CTE for unknown accounts.
- Pattern 2 rewritten: `CONTACT_360_V` as preferred, raw 3-table join as fallback. Correct join key documented: `SF_CONTACTS.ASTRO_USER_ID = MODEL_ASTRO.USERS.USER_ID`.
- Patterns 11 (domain fallback) and 12 (Gong enrichment + call detail) added.
- Optimization Rule 17 added: GTM views first, raw tables only when views don't cover the need.
**2026-04-09** — 49 queries observed (cache warming cron + ad-hoc risk scorecard):
- Cache warming ran at 8:25pm UTC: 47 `ACCOUNT_360_V` queries at ~500-760ms (~120MB each); all 22 subsequent `ACCOUNT_NOTES` prefetch queries hit result cache (BYTES_SCANNED=0, 47-105ms) — cron is healthy
- Risk scorecard query scanned 2.87GB in 2.5s because `GONG_CALL_ENRICHMENTS_V` and `ZD_TICKET_ENRICHMENTS_V` were grouped across ALL accounts before joining to `my_accounts` (~47 accounts). Fix: add `WHERE ACCT_ID IN (SELECT ACCT_ID FROM my_accounts)` inside each enrichment CTE to pre-filter before grouping — pushes pruning before the full-view scan
- Buggy join pattern found in ZD enrichment CTE: `JOIN MAPS.ZD_ORGS zo ON zo.ZD_ORG_ID = t.TICKET_ID` — `TICKET_ID` is a ticket primary key, not a ZD org ID, so this join returns nothing. `ZD_TICKET_ENRICHMENTS_V` already has `ACCT_ID` — filter directly with `WHERE t.ACCT_ID = a.ACCT_ID`, no MAPS bridge needed
**2026-04-10** — 42 queries observed (account research session + cost analysis for unknown account `clvy14mjc05dr01n2q5s01tlv`):
- `DEPLOYMENT_COST_MULTI` confirmed new columns: `A5_WORKER_COST`, `A20_WORKER_COST`, `A5_WORKER_RUNTIME_SECONDS`, `A20_WORKER_RUNTIME_SECONDS`, `TOTAL_DEPLOYMENT_RUNTIME_SECONDS`, `TOTAL_EPHEMERAL_STORAGE_COST`, `TOTAL_REMOTE_EXECUTION_COST`, `TOTAL_OBSERVE_COST` — all usable for GPU/RE cost breakdown. Add `DEPLOYMENT_ID != 'no_deployment_id'` filter to exclude unassigned rows.
- `WORKER_QUEUE_COST_MULTI` confirmed columns: `A5/A10/A20_WORKER_RUNTIME_SECONDS`, `TOTAL_COST`, `DEPLOYMENT_ID` — use for per-queue GPU hour breakdowns when `DEPLOYMENT_COST_MULTI` isn't granular enough.
- `GTM.PUBLIC.ACCOUNT_NOTES` and `ACCOUNT_360_V` have no `ACCOUNT_NAME` column — two queries silently failed (0 bytes, 0 rows) trying `WHERE LOWER(n.ACCOUNT_NAME) LIKE ...`; a third tried `ACCOUNT_NAME, SF_ACCT_ID, ARR, STAGE, OWNER` on `ACCOUNT_360_V` (also wrong). Correct: `ACCOUNT_NOTES` uses `ACCT_ID` filter only; `ACCOUNT_360_V` columns follow `ACCT_*` naming (`ACCT_NAME`, `ACCT_ID`, `TOTAL_ARR_AMT`). Wrong column names trigger silent errors — no exception, just 0 rows returned, forcing a 129MB `SELECT * LIMIT 1` probe.

**2026-04-13** — No queries in past 24h; 88 late-April-10 queries (post-cron) analyzed. Key new findings:
- New `CURRENT_ASTRO_CUSTS` pay-go columns confirmed working: `PAYGO_BILLED_AMT_TO_DATE`, `PROJECTED_PAYGO_CONTRACT_AMT_30D`, `BILLING_PROVIDER_TYPE`, `PLAN_TYPE`, `USAGE_AMT_30D_LAG`, `USAGE_GROWTH_PCT_30D`, `LICENSE_CONSUMED_PCT`, `CREDIT_CONSUMED_AMT`, `CONTRACT_GRANTED_AMT`, `PROJECTED_CREDITS_CONSUMED_30D`, `PROJECTED_OVERAGE_AMT_30D`, `PROJECTED_OVERAGE_PCT_30D` — added to column reference
- `GTM.PUBLIC.CONTACT_NOTES` confirmed: columns `NOTE_ID`, `CONTACT_NAME`, `NOTE_DATE`, `NOTE_TYPE`, `CONTENT`, `SOURCE`, `CREATED_AT`; filter by `ACCT_ID`; parallel structure to `ACCOUNT_NOTES` for per-person notes
- `SF_CAMPAIGN_MEMBERS.CAMPAIGN_MEMBER_EMAIL_DOMAIN` confirmed: enables prospect campaign lookup by domain without needing `ACCT_ID` (useful pre-qualification); `CONTACT_ID` filter also confirmed
- `LF_WEBSITE_VISITS` new columns confirmed: `VISIT_DURATION`, `CAMPAIGN_NAME`, `LF_VISIT_ID` (join key to `LF_PAGE_VIEWS`)

**2026-04-15** — 45 queries observed (account-research sessions for Pay.com + Rithm Capital prospects). Key findings:
- `GTM.PUBLIC.ACCOUNT_RESEARCH_LATEST_V` confirmed as new table (was undocumented): queried in every account-research session; columns: `RESEARCH_ID`, `ACCT_ID`, `ACCT_NAME`, `RESEARCH_DATE`, `SCORE`, `GRADE`, `CONFIDENCE`, `MC_GRADE`, `SOURCES_USED` (JSON), `REPORT_MD` (full markdown), `DAYS_SINCE_RESEARCH`, `IS_STALE`; added to schema map and decision tree
- `GONG_CALL_TRANSCRIPTS` full-fetch pattern (all transcript fields + join to `GONG_CALLS`) scanned 735MB for a single `ACCT_NAME ILIKE '%Pay.com%'` — expected for transcript fetches; no optimization needed at 1.4s; all other queries hit result cache (0MB, 0.1s)
- Account-research multi-table query pattern confirmed healthy: 10 parallel queries per account (`SF_ACCOUNTS`, `SF_CONTACTS`, `GONG_CALL_ENRICHMENTS_V`, `LF_WEBSITE_VISITS + LF_PAGE_VIEWS`, `SF_CAMPAIGN_MEMBERS`, `SF_OPPS`, `SF_ASTRO_ORGS`, `ZD_TICKET_ENRICHMENTS_V`, `ACCOUNT_NOTES`, `ACCOUNT_RESEARCH_LATEST_V`) — repeated runs hit result cache on all queries
**2026-04-20** — 48 queries observed (account-research cron + Dempsey account-research session):
- `GTM.PUBLIC.ACCOUNT_360_V` has `RESEARCH_DATE`, `RESEARCH_IS_STALE`, and `OWNER_NAME` columns — confirmed used in research-cron eligibility query (`WHERE OWNER_NAME ILIKE '%kenney%' AND (RESEARCH_DATE IS NULL OR RESEARCH_IS_STALE = TRUE)`); updated decision tree note
- `SF_ACCOUNTS.INDUSTRY` column confirmed in live query (was missing from schema table) — added to column list
- All account-research session queries (SF_ACCOUNTS, GONG_CALL_TRANSCRIPTS, GONG_CALL_ENRICHMENTS_V, LF_WEBSITE_VISITS, SF_CAMPAIGN_MEMBERS, SF_OPPS, SF_ASTRO_ORGS, ZD_TICKET_ENRICHMENTS_V, ACCOUNT_NOTES, ACCOUNT_RESEARCH_LATEST_V) hit result cache on repeated runs — 10-query parallel pattern fully cache-warm

**2026-04-21** — 35 queries observed (Metronome rate card / deployment pricing analysis session for dolabradigital and MarginEdge):
- Three `MODEL_FINANCE` Metronome event tables newly confirmed — `METRONOME_DEPLOYMENT_EVENTS` (scheduler pricing lookup: `SCHEDULER_SIZE`, `IS_HA`, `REGION`, `CLOUD_PROVIDER`, `RATE_CARD_ID`, `PRICING_GROUP_OBJECT_HASH`), `METRONOME_COMPUTE_EVENTS` (worker pricing: `WORKER_SIZE` lowercase `a5/a10/a20/a40`, `IS_REMOTE_EXECUTION`, `PRICING_GROUP_OBJECT_HASH`), `METRONOME_CLUSTER_EVENTS` (dedicated cluster pricing: `CLUSTER_ZONE_TYPE`, `CLUSTER_TYPE`, `PRICING_GROUP_OBJECT_HASH`); all three join to `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH` for per-unit prices
- `MODEL_ASTRO.DEPLOYMENTS` has `REGION` and `RESILIENCY` columns (previously undocumented); `MODEL_ASTRO.CLUSTERS` confirmed as a table joinable from `MODEL_ASTRO.ORGANIZATIONS` via `CLUSTER_ID`
- `MODEL_FINANCE.METRONOME_ID_PRICE_LOG` exists (undocumented table) — needs `SELECT * LIMIT 50` to discover schema before use
- `DEPLOYMENT_COST_MULTI` scans ~1.8GB per account even with tight ORG_ID + TIME_GRAIN + date filters — expected, no fix needed; use `ORG_COST_MULTI` if deployment-level breakdown isn't required

**2026-04-22** — 44 queries observed (account-research sessions for Diagram, and two unnamed prospect accounts):
- `SF_ACCOUNTS.ACCT_STATUS` has an undocumented value: `'No Engagement'` — enum in skill previously listed only `Active, Inactive, Former Customer`; updated below
- Multi-OR Gong transcript lookup confirmed for accounts with name variations: `WHERE (UPPER(t.ACCT_NAME) LIKE '%NYCDOT%' OR UPPER(t.ACCT_NAME) LIKE '%NYC DOT%' OR ...)` — use this pattern when an account name has common abbreviations or spacing variants; Pattern 5 in skill shows single-LIKE but multi-OR is safe and correct
- One `ERROR(606)` "No active warehouse selected" — connection started without specifying warehouse; always connect with `warehouse='HUMANS'` (confirmed: the query immediately after retried successfully with warehouse set)
- 10-query account-research parallel pattern clean across 3 prospects (SF_ACCOUNTS, SF_CONTACTS, GONG_CALL_ENRICHMENTS_V, LF_WEBSITE_VISITS+LF_PAGE_VIEWS, SF_CAMPAIGN_MEMBERS, SF_OPPS, SF_ASTRO_ORGS, ZD_TICKET_ENRICHMENTS_V, ACCOUNT_NOTES, ACCOUNT_RESEARCH_LATEST_V) — all sub-650ms; `IS_STALE IS NULL OR IS_STALE = FALSE` is the correct NULL-safe check for "research is current" on `ACCOUNT_RESEARCH_LATEST_V`

**2026-04-23** — 84 queries observed (account-research sessions for Pathlock, Nayya, Roofstock, Starship, Involves, SPX Capital, Saika, CREC, plus schema discovery run). Key finding:
- `GONG_CALL_TRANSCRIPTS` **always scans ~750MB regardless of columns selected** — 3 separate queries that excluded `FULL_TRANSCRIPT` (metadata-only: title, brief, attendees, next steps) still scanned 750,818,304 bytes each, identical to full transcript fetches. The full table partition is always read. Use Pattern 12 (`GONG_CALL_ENRICHMENTS_V` + `GONG_CALLS` join) for metadata-only Gong lookups — that pattern scans ~25MB; only use GONG_CALL_TRANSCRIPTS when you specifically need `FULL_TRANSCRIPT`
- `SF_ACCOUNTS` domain lookup via `WHERE LOWER(ACCT_DOMAIN) LIKE LOWER('%domain%')` confirmed as the standard prospect resolution pattern — scans ~47-49MB consistently, sub-600ms; result cache kicks in on repeat lookups within same session
- `GTM.SHARED` schema exists but is empty/inaccessible — no tables returned; ignore it

**2026-04-24** — 79 queries observed (account-research cron processing 7 prospects: Neustreet, Aegro, MRS, Restaurant365, jebsweb.com.br, Northbeam, Mulliganfunding, Prenuvo):
- ERROR 606 "No active warehouse" appeared 5 times across 4 separate MCP sessions within the same cron run — frequency higher than previous days (prior log shows 1x/day). The MCP server is restarting connections mid-cron, losing warehouse state each time. Each session retries and succeeds after warehouse is set. No data loss but adds ~100ms latency and noise to history.
- Account-research cron confirmed running a dual Gong fetch per account: Pattern 12 (`GONG_CALL_ENRICHMENTS_V + GONG_CALLS`, ~230KB) runs first, then a separate `GONG_CALL_TRANSCRIPTS` fetch (~750–790MB) for `ATTENDEES` and `OPP_NAME` — two columns not available via the enrichment view. Total Gong scan cost: ~5.3GB for 7 accounts vs ~1.6MB if Pattern 12 alone sufficed. If `ATTENDEES`/`OPP_NAME` are not critical outputs, dropping the GONG_CALL_TRANSCRIPTS step would eliminate this cost. This is expected behavior given current skill design; documenting as known overhead.
- All 10-query parallel account-research pattern healthy — non-Gong queries all sub-500ms; `GONG_CALL_ENRICHMENTS_V` with `ACCT_ID` filter consistently scans only ~230KB (result cache on repeated accounts).
**2026-04-24** — Renewal analysis session (Python connector via Bash, not MCP — hooks did not fire). Column errors caught and corrected:
- `SF_OPPS` has NO `DISCOUNT`, `DISCOUNT_PCT`, `LIST_PRICE`, or `LIST_PRICE_AMT` columns — discount is not stored in SF opps at all; infer from `METRONOME_CREDIT_GRANTS.COST_BASIS` (e.g. 0.8333 = 16.67% discount)
- `METRONOME_USAGE_DAILY` has NO `PRODUCT_NAME` column — it is an invoice-level row (one row per day per invoice period), not a line-item table; key columns: `USAGE_DATE`, `USAGE_AMT`, `BILL_AMT`, `PLAN_NAME`, `SUPPORT_LEVEL`, `INV_UPLIFT_PCT`, `PERIOD_START_DATE`, `PERIOD_END_DATE`, `IS_LATEST`, `IS_CONTRACT`, `IS_FINALIZED`, `IS_DRAFT`
- `MODEL_ASTRO.DEPLOYMENTS` has NO `RESILIENCY` column — confirmed via query error; use `IS_HIGH_AVAILABILITY` (boolean) instead; also confirmed new columns: `RUNTIME_TYPE`, `ASTRO_RUNTIME_VERSION`, `WORKSPACE_NAME`, `CLUSTER_NAME`, `PROVIDER_REGION`, `IS_DEVELOPMENT_ONLY`, `SCHEDULER_AU`, `WORKER_AU`, `SCALING_SPEC` (JSON with hibernation schedules)
- `METRONOME_CREDIT_GRANTS` has NO `CREDIT_CONSUMED_AMT` column — use `GRANTED_AMT - CURRENT_BALANCE_AMT` to compute consumed; confirmed columns: `GRANTED_AMT`, `CURRENT_BALANCE_AMT`, `ROLLED_OVER_AMT`, `EXPIRED_AMT`, `COST_BASIS` (discount multiplier), `PAID_AMT`, `IS_ROLLOVER_CREDIT`, `IS_ROLLED_OVER_CREDIT`, `ROLLOVER_RATIO`
- `SF_CUST_CONTRACTS` filter `ASTRO_ORG_ID` returns empty when used with `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE` — use `ACCT_ID` filter instead; confirmed columns include `OPP_TYPE`, `CONTRACT_ARR_AMT`, `TOTAL_CONTRACT_VALUE`, `SUPPORT_LEVEL`, `SUPPORT_TIER_PCT`, `PRODUCT`, `SUB_PRODUCT`, `IS_OBSERVE`, `DAYS_IN_CONTRACT`
- `METRONOME_CONTRACTS` confirmed columns: `CONTRACT_ID`, `PLAN_TYPE`, `RATE_CARD_ID`, `IS_ACTIVE`, `START_TS`, `END_TS` — use `RATE_CARD_ID` to join to `METRONOME_RATE_CARDS` for tier/uplift info
- Rate card discovery pattern confirmed: `METRONOME_RATE_CARDS` has `RATE_CARD_ID`, `RATE_CARD_NAME`, `AVG_UPLIFT_PCT` — join via `METRONOME_CONTRACTS.RATE_CARD_ID` to get a customer's current rate card; `AVG_UPLIFT_PCT` values: Enterprise=1.0, Enterprise w/ BC Support=1.25, Business Critical=0.75, Business=0.5
- MCP Snowflake tool availability: only loads in sessions started from Claude desktop app at `$HOME`; not available in CLI sessions started from other directories — use Python connector (`~/.venvs/snowflake/bin/python3`) as fallback; hooks won't fire in fallback sessions
**2026-05-05** — Zendesk ticket monitor DAG build session (Python connector via Bash):
- Correct warehouse is `HUMANS` (not `COMPUTE_WH`) — `COMPUTE_WH` does not exist; `GTM_ROBOTS` and `HUMANS` are the two user-accessible warehouses; `HUMANS` is correct for interactive/cron use
- ZD ticket join path: `HQ.MODEL_SUPPORT.ZD_TICKETS` → `HQ.MODEL_SUPPORT.ZD_ORGS` (on `ZD_ORGS.ORG_ID = ZD_TICKETS.ORG_ID`) → `GTM.PUBLIC.ACCOUNT_360_V` (on `ACCOUNT_360_V.ACCT_ID = ZD_ORGS.SF_ACCT_ID`). `ZD_ORGS.SF_ACCT_ID` is the direct FK to Salesforce account ID. Do NOT use `HQ.MAPS.ZD_ACCTS` (has `ZD_ORG_MAP` as JSON array, requires FLATTEN — more complex and error-prone).
- `HQ.MODEL_SUPPORT.ZD_TICKETS` key columns: `TICKET_ID`, `ORG_ID`, `ORG_NAME`, `STATUS`, `PRIORITY`, `SUBJECT`, `DESCRIPTION`, `CREATED_TS` (TIMESTAMP_TZ), `UPDATED_TS` (TIMESTAMP_TZ). Note: column is `CREATED_TS` not `CREATED_AT` or `UPDATED_AT`.
- `SELECT DISTINCT` with `ORDER BY`: can only ORDER BY columns in the SELECT list — aliased expressions (e.g. `t.CREATED_TS::DATE AS TICKET_DATE`) must be referenced by alias, not original expression.
- `INFORMATION_SCHEMA.TABLES` queries fail with error 002043 when no warehouse is set — always set warehouse before using INFORMATION_SCHEMA; `SHOW TABLES` works without warehouse.
<!-- PATTERNS_LOG_END -->
