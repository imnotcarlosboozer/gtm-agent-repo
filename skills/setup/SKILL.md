# Setup Skill

Install and configure all Astronomer Claude Code skills for a new user. Claude detects what is already configured, auto-derives values it can fetch from APIs, and only asks the user for credentials it cannot obtain itself.

## Trigger

User runs `/setup` or says something like "set up the skills", "help me get started", or "install everything".

---

## Instructions

### Step 1: Detect current state

Run all checks in parallel:

```bash
# Check env vars
python3 -c "
import os
vars = ['GONG_ACCESS_KEY', 'GONG_SECRET_KEY', 'APOLLO_API_KEY', 'EXA_API_KEY']
for v in vars:
    print(f'{v}: {\"SET\" if os.environ.get(v) else \"MISSING\"}')"

# Check MCP servers
claude mcp list 2>/dev/null || echo "MCP: unable to list"

# Check scripts
for f in ~/claude-work/gong_account_transcripts.py ~/claude-work/gong_json_to_markdown.py; do
  [ -f "$(eval echo $f)" ] && echo "SCRIPT OK: $f" || echo "SCRIPT MISSING: $f"
done

# Check installed skills
for s in account-research account-question demo-prep weekly-gong-review quarterly-pipeline-report; do
  [ -f "$HOME/.claude/skills/$s/SKILL.md" ] && echo "SKILL OK: $s" || echo "SKILL MISSING: $s"
done

# Check prompt templates
for f in ~/claude-work/research-assistant/prompts/01_fit_scoring.md \
          ~/claude-work/research-assistant/prompts/02_account_research.md; do
  [ -f "$(eval echo $f)" ] && echo "TEMPLATE OK: $f" || echo "TEMPLATE MISSING: $f"
done

# Check Leadfeeder account ID config
python3 -c "
import os, json
cfg = os.path.expanduser('~/claude-work/astronomer-skills-config.json')
if os.path.exists(cfg):
    data = json.load(open(cfg))
    lid = data.get('leadfeeder_account_id', '')
    aid = data.get('apollo_field_id', '')
    print(f'CONFIG: leadfeeder_account_id={lid or \"MISSING\"} apollo_field_id={aid or \"MISSING\"}')
else:
    print('CONFIG: file not found')"
```

Summarize what is already working and what needs to be set up. Tell the user what you found before asking for anything.

---

### Step 2: Collect credentials

For each credential that is MISSING, ask the user. Ask all missing credentials in a single message — do not ask one at a time.

**What to ask for (only if missing):**

| Credential | Where to get it |
|------------|----------------|
| `GONG_ACCESS_KEY` + `GONG_SECRET_KEY` | Gong → Settings → API → Access Keys → Create |
| `APOLLO_API_KEY` | Apollo → Settings → Integrations → API Keys |
| `LEADFEEDER_API_TOKEN` | Leadfeeder → Settings → API Tokens → Create new token |
| `EXA_API_KEY` | [exa.ai](https://exa.ai) → Dashboard → API Keys (optional — skip if not needed) |

Tell the user: "You only need Gong and Apollo to get started. Leadfeeder adds website visit data (recommended). Exa is optional."

If the user does not have a credential for an optional source, skip it and note the graceful degradation in the summary.

---

### Step 3: Write env vars to shell config

```bash
SHELL_RC="$HOME/.zshrc"
[ -f "$HOME/.bash_profile" ] && [ ! -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.bash_profile"

# Only append vars that are not already present
python3 -c "
import os, sys
rc = os.path.expanduser(os.environ.get('SHELL_RC', '~/.zshrc'))
content = open(rc).read() if os.path.exists(rc) else ''
to_add = []
pairs = sys.argv[1:]
for pair in pairs:
    key, val = pair.split('=', 1)
    if key not in content:
        to_add.append(f'export {key}={val}')
if to_add:
    with open(rc, 'a') as f:
        f.write('\n# Astronomer Claude Code Skills\n')
        f.write('\n'.join(to_add) + '\n')
    print(f'Added {len(to_add)} vars to {rc}')
else:
    print('All vars already present')
" \
  "GONG_ACCESS_KEY={USER_PROVIDED_VALUE}" \
  "GONG_SECRET_KEY={USER_PROVIDED_VALUE}" \
  "APOLLO_API_KEY={USER_PROVIDED_VALUE}" \
  "EXA_API_KEY={USER_PROVIDED_VALUE}"

source "$SHELL_RC"
```

Only write the vars the user actually provided. Skip missing optional ones.

---

### Step 4: Auto-derive account IDs and field IDs

Once credentials are available (set in env or provided by user), auto-fetch all IDs so the user never has to look them up manually.

Run all three derivations in parallel:

**4a. Gong — verify credentials work:**
```bash
AUTH=$(echo -n "$GONG_ACCESS_KEY:$GONG_SECRET_KEY" | base64)
RESULT=$(curl -s -o /dev/null -w "%{http_code}" "https://api.gong.io/v2/users?limit=1" \
  -H "Authorization: Basic $AUTH")
echo "GONG_AUTH: $RESULT"
```
If `200`, credentials are valid. If not, tell the user and ask them to re-check the key pair.

**4b. Apollo — find the Account_Research custom field ID:**
```bash
FIELDS=$(curl -s -X GET "https://api.apollo.io/v1/typed_custom_fields" \
  -H "Content-Type: application/json" \
  -H "Cache-Control: no-cache, no-store, must-revalidate" \
  -d "{\"api_key\": \"$APOLLO_API_KEY\"}")
echo "$FIELDS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
fields = data.get('typed_custom_fields', [])
for f in fields:
    if 'research' in f.get('name', '').lower() or 'account_research' in f.get('name', '').lower():
        print(f'APOLLO_FIELD_ID: {f[\"id\"]} (name: {f[\"name\"]})')
if not fields:
    print('APOLLO_FIELD_ID: none found — check API key')
"
```

**4c. Leadfeeder — find Astronomer account ID:**
Use `mcp__leadfeeder__list_accounts` if the MCP is connected. Otherwise use the REST API:
```bash
curl -s "https://api.dealfront.com/v1/accounts" \
  -H "Authorization: Token token={LEADFEEDER_API_TOKEN}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
accounts = data.get('data', [])
for a in accounts:
    print(f'ACCOUNT: {a.get(\"id\")} — {a.get(\"attributes\", {}).get(\"name\", \"\")}')
"
```
Show the user the list and ask them to confirm which account is theirs (usually the first and only one).

Save all derived values to a local config file:
```bash
python3 -c "
import json, os
cfg_path = os.path.expanduser('~/claude-work/astronomer-skills-config.json')
os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
existing = {}
if os.path.exists(cfg_path):
    existing = json.load(open(cfg_path))
existing.update({
    'leadfeeder_account_id': '{DERIVED_LEADFEEDER_ID}',
    'apollo_field_id': '{DERIVED_APOLLO_FIELD_ID}',
})
json.dump(existing, open(cfg_path, 'w'), indent=2)
print(f'Config saved to {cfg_path}')
"
```

---

### Step 5: Install MCP servers

For each MCP server not already connected, run the install command. Do not re-run for already-connected servers.

```bash
# Gong MCP (needed by account-research, account-question, demo-prep, weekly-gong-review)
claude mcp add --transport http gong https://mcp.gong.io/mcp

# Apollo MCP (needed by account-research for contact enrichment)
claude mcp add --transport http apollo https://mcp.apollo.io/mcp

# Common Room MCP (optional — needed by account-research for contact intelligence)
claude mcp add --transport http commonroom https://mcp.commonroom.io/mcp

# Exa MCP (optional — supplements account-research web search)
npm install -g exa-mcp-server 2>/dev/null
claude mcp add --transport stdio exa -- npx exa-mcp-server
```

**Leadfeeder MCP** (if API token was provided):
```bash
# Clone the MCP server from the repo
REPO_DIR=$(pwd)
mkdir -p ~/.claude/mcp-servers/leadfeeder
cp "$REPO_DIR/mcp-servers/leadfeeder/index.js" ~/.claude/mcp-servers/leadfeeder/
cd ~/.claude/mcp-servers/leadfeeder && npm install

claude mcp add leadfeeder --scope user \
  -e LEADFEEDER_API_TOKEN={USER_PROVIDED_TOKEN} \
  -- node ~/.claude/mcp-servers/leadfeeder/index.js
```

---

### Step 6: Install skills and scripts

Run all in parallel:

```bash
# Create directories
mkdir -p ~/.claude/skills/account-research
mkdir -p ~/.claude/skills/account-question
mkdir -p ~/.claude/skills/demo-prep
mkdir -p ~/.claude/skills/weekly-gong-review
mkdir -p ~/.claude/skills/quarterly-pipeline-report
mkdir -p ~/claude-work/research-assistant/prompts
mkdir -p ~/Scripts

# Copy skill files (from the repo root — adjust path if running from elsewhere)
REPO_DIR=$(pwd)
cp "$REPO_DIR/skills/account-research/SKILL.md"        ~/.claude/skills/account-research/SKILL.md
cp "$REPO_DIR/skills/account-question/SKILL.md"        ~/.claude/skills/account-question/SKILL.md
cp "$REPO_DIR/skills/demo-prep/SKILL.md"               ~/.claude/skills/demo-prep/SKILL.md
cp "$REPO_DIR/skills/weekly-gong-review/SKILL.md"      ~/.claude/skills/weekly-gong-review/SKILL.md
cp "$REPO_DIR/skills/quarterly-pipeline-report/SKILL.md" ~/.claude/skills/quarterly-pipeline-report/SKILL.md

# Copy scripts
cp "$REPO_DIR/gong_account_transcripts.py"  ~/claude-work/gong_account_transcripts.py
cp "$REPO_DIR/gong_json_to_markdown.py"     ~/claude-work/gong_json_to_markdown.py
cp "$REPO_DIR/scripts/quarterly_pipeline_context.py" ~/Scripts/quarterly_pipeline_context.py
chmod +x ~/Scripts/quarterly_pipeline_context.py

# Copy prompt templates
cp "$REPO_DIR/prompts/01_fit_scoring.md"    ~/claude-work/research-assistant/prompts/01_fit_scoring.md
cp "$REPO_DIR/prompts/02_account_research.md" ~/claude-work/research-assistant/prompts/02_account_research.md

echo "Files copied."
```

**Install Python dependencies:**
```bash
pip install requests python-dateutil 2>&1 | tail -1
```

---

### Step 7: Patch skill files with derived IDs

The installed skill files use placeholder values (`{YOUR_LEADFEEDER_ACCOUNT_ID}`, `{YOUR_APOLLO_FIELD_ID}`). Replace them with the actual values derived in Step 4:

```bash
python3 -c "
import json, os, re

cfg = json.load(open(os.path.expanduser('~/claude-work/astronomer-skills-config.json')))
lid = cfg.get('leadfeeder_account_id', '')
aid = cfg.get('apollo_field_id', '')

skill = os.path.expanduser('~/.claude/skills/account-research/SKILL.md')
content = open(skill).read()
if lid:
    content = content.replace('{YOUR_LEADFEEDER_ACCOUNT_ID}', lid)
if aid:
    content = content.replace('{YOUR_APOLLO_FIELD_ID}', aid)
open(skill, 'w').write(content)
print(f'Patched account-research/SKILL.md — leadfeeder_id={lid} apollo_field_id={aid}')
"
```

Note: this patches only the **installed** copy at `~/.claude/skills/`. The repo copy keeps placeholders — real IDs never enter the repo.

---

### Step 8: Sync Gong cache

```bash
python3 ~/claude-work/gong_account_transcripts.py --sync
```

This takes 1–5 minutes depending on call volume. Run in the background if the user wants to continue:

```bash
python3 ~/claude-work/gong_account_transcripts.py --sync &
echo "Gong sync running in background (PID $!). Skills work immediately — sync improves speed."
```

---

### Step 9: Verify and summarize

Run final checks:

```bash
# Test Gong API
AUTH=$(echo -n "$GONG_ACCESS_KEY:$GONG_SECRET_KEY" | base64)
GONG_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.gong.io/v2/users?limit=1" -H "Authorization: Basic $AUTH")

# Test Apollo API
APOLLO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  "https://api.apollo.io/v1/users/me?api_key=$APOLLO_API_KEY")

echo "GONG: $GONG_STATUS"
echo "APOLLO: $APOLLO_STATUS"
```

Present a summary table to the user:

```
Setup complete. Here is what is working:

CREDENTIAL / SOURCE     STATUS
─────────────────────────────────────────────
Gong API                [connected / failed]
Apollo API              [connected / failed]
Leadfeeder MCP          [connected / skipped — no token provided]
Common Room MCP         [connected / skipped]
Exa AI MCP              [connected / skipped]

SKILLS INSTALLED
─────────────────────────────────────────────
account-research        [installed]
account-question        [installed]
demo-prep               [installed]
weekly-gong-review      [installed]
quarterly-pipeline-report [installed]

NEXT STEP
─────────────────────────────────────────────
Restart Claude Code to activate the new skills, then try:
  "research Acme Corp, acme.com"
  "/weekly-gong-review"
```

If anything failed, explain exactly what is missing and what the user needs to do — do not leave them guessing.

---

## What this skill patches vs. what stays in the repo

| Value | In repo | Installed skill |
|-------|---------|----------------|
| Leadfeeder account ID | `{YOUR_LEADFEEDER_ACCOUNT_ID}` | Real ID (patched by setup) |
| Apollo field ID | `{YOUR_APOLLO_FIELD_ID}` | Real ID (patched by setup) |
| Gong workspace URL | `your-workspace.app.gong.io` | Unchanged (derived at runtime) |
| API keys | Never present | In `~/.zshrc` only |

---

**Begin setup now.**
