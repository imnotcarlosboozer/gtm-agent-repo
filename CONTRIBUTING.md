# Contributing

Guidelines for adding skills, updating existing ones, and submitting PRs to this repo.

> **Context**: This repo is used by the Astronomer sales team. It is currently public. All internal identifiers, credentials, and account data must stay out of the repo. The `/setup` skill patches installed copies with real values at setup time — the repo itself always keeps placeholders.

---

## Before every PR: sanitization checklist

Run this before opening or updating a PR:

```bash
cd /path/to/gtm-agent-repo

# 1. No hardcoded paths
grep -rn "/Users/" --include="*.md" --include="*.py" --include="*.js" . \
  && echo "FAIL: hardcoded paths found" || echo "OK: no hardcoded paths"

# 2. No real API keys or tokens (patterns: long hex strings, sk-, Bearer values)
grep -rEn "[a-f0-9]{32,}|sk-[a-zA-Z0-9]{20,}|Bearer [a-zA-Z0-9]" \
  --include="*.md" --include="*.py" --include="*.js" . \
  | grep -v "YOUR_\|your_\|placeholder\|example\|{" \
  && echo "FAIL: possible secrets found" || echo "OK: no secrets"

# 3. No specific individuals' emails (only user@astronomer.io is allowed)
grep -rEn "[a-z]+\.[a-z]+@astronomer\.io" --include="*.md" . \
  && echo "FAIL: individual emails found" || echo "OK: no individual emails"

# 4. No Gong workspace subdomain
grep -rn "us-[0-9]\+\.app\.gong\.io" --include="*.md" . \
  && echo "FAIL: Gong workspace subdomain found" || echo "OK: no workspace subdomain"

# 5. No real account names as examples
# Manual check — scan for customer or prospect company names used as examples.
# Use: Acme Corp, Beta Inc, Gamma LLC

# 6. No org-specific numeric IDs
grep -rEn "\"[0-9]{6,}\"" --include="*.md" . \
  | grep -v "123456\|000000\|example\|call\?id" \
  && echo "WARN: check numeric IDs" || echo "OK: no suspicious numeric IDs"
```

All checks must pass before merging.

---

## Placeholder reference

When adding or updating skills, use these exact placeholder strings for values that vary per user or organization. The `/setup` skill knows how to replace them at install time.

| Placeholder | What it represents | Where to get it |
|-------------|-------------------|-----------------|
| `{YOUR_LEADFEEDER_ACCOUNT_ID}` | Leadfeeder account ID | Auto-derived by `/setup` via Leadfeeder API |
| `{YOUR_APOLLO_FIELD_ID}` | Apollo `Account_Research` custom field ID | Auto-derived by `/setup` via Apollo API |
| `your_access_key` | Gong API access key | Gong → Settings → API → Access Keys |
| `your_secret_key` | Gong API secret key | Gong → Settings → API → Access Keys |
| `your_apollo_api_key` | Apollo API key | Apollo → Settings → Integrations → API Keys |
| `your_token` | Leadfeeder API token | Leadfeeder → Settings → API Tokens |
| `your_exa_api_key` | Exa AI API key | exa.ai → Dashboard → API Keys |
| `your-workspace.app.gong.io` | Gong workspace URL (for deep links) | Derived at runtime from user's Gong session |
| `user@astronomer.io` | Generic Astronomer user email | Not a real address — used as a doc example only |

---

## What belongs in the repo vs. what does not

| Belongs in repo | Does NOT belong in repo |
|-----------------|------------------------|
| Skill instructions (SKILL.md files) with placeholder values | Real Leadfeeder account IDs |
| Python and JS scripts with `os.path.expanduser('~/')` paths | Real Apollo field IDs |
| README setup instructions using placeholder credentials | Any `GONG_ACCESS_KEY` / `APOLLO_API_KEY` values |
| `config.example.sh` with placeholder values | `config.sh` with real values |
| Generic examples using Acme Corp, Beta Inc, Gamma LLC | Real customer or prospect company names |
| `user@astronomer.io` as a generic email example | `firstname.lastname@astronomer.io` |
| `your-workspace.app.gong.io` | `us-XXXXX.app.gong.io` (real subdomain) |
| Changelog and PR descriptions (no account data) | Gong transcripts, Leadfeeder visit data, Common Room contacts |

---

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md`
2. Write instructions for Claude — not a shell script. The SKILL.md tells Claude what to do step by step.
3. Use placeholders from the table above for any org-specific values.
4. Use `~/` (not `/Users/yourname/`) for all home directory references in bash, and `os.path.expanduser('~/')` in Python.
5. If the skill needs a new credential or ID, add it to the placeholder table in this file and add auto-derivation logic to `skills/setup/SKILL.md`.
6. Add the skill to the `README.md` Contents table and write a Setup section for it.
7. Update `skills/setup/SKILL.md` to install the new skill (Step 6) and patch any new placeholders (Step 7).

---

## Updating an existing skill

1. Pull the latest: `git pull origin main`
2. Edit the file in `skills/<skill-name>/SKILL.md`
3. Run the sanitization checklist above
4. Update the PR description to describe exactly what changed and why
5. If any placeholder values changed (new IDs, renamed env vars), update `CONTRIBUTING.md` placeholder table and `skills/setup/SKILL.md` accordingly

---

## PR description standard

Every PR must include:

- **What changed**: bullet list of each skill or file modified
- **Why**: one sentence per change explaining the motivation
- **Test plan**: checkboxes for each change tested — at minimum, run the affected skill on one real account and confirm the report generates without errors
- **Sanitization**: confirm the checklist above was run and passed

---

## Repo structure

```
gtm-agent-repo/
├── skills/
│   ├── setup/               # /setup skill — installs and configures everything
│   ├── account-research/    # Research a company for Astronomer fit
│   ├── account-question/    # Answer questions about an account using Gong + saved research
│   ├── demo-prep/           # Generate SE demo prep brief from Gong transcripts
│   ├── weekly-gong-review/  # Weekly call coaching report
│   └── quarterly-pipeline-report/
├── prompts/                 # Prompt templates used by account-research
├── mcp-servers/             # MCP server source (Leadfeeder, etc.)
├── scripts/                 # Python helper scripts
├── docs/                    # Architecture docs and design notes
├── README.md                # User-facing setup and usage guide
└── CONTRIBUTING.md          # This file
```

Each `SKILL.md` file is read directly by Claude Code when the skill is invoked. Keep them focused and procedural — Claude follows them step by step.
