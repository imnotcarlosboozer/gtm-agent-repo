# Notion Auto To-Do Sync

Hourly cron that pulls action items from your Gong calls and adds them to a Notion database. Scoped to your calls only — never overwrites or removes existing rows, only appends new ones.

## What it does

Every hour, the cron:
1. Reads `~/claude-work/.todo-last-run` to find when it last synced (defaults to 1 hour ago if missing)
2. Searches Gong for your calls since that timestamp
3. For each new call: fetches the call summary and extracts your action items
4. Deduplicates against existing rows by Source Call URL
5. Creates new Notion pages for any new action items
6. Updates `~/claude-work/.todo-last-run` with the current timestamp
7. Silent finish if no new items

If you were offline, the next run catches up from the last timestamp — no gaps.

## Setup

### 1. Prerequisites

- Claude Code with Gong and Notion MCP servers connected
- Your Gong user ID (see below)
- A Notion database to write to

### 2. Find your Gong user ID

```bash
AUTH=$(echo -n "$GONG_ACCESS_KEY:$GONG_SECRET_KEY" | base64)
# Paginate until you find your email
curl -s "https://api.gong.io/v2/users?limit=100" \
  -H "Authorization: Basic $AUTH" | python3 -c "
import json,sys
data=json.load(sys.stdin)
for u in data.get('users',[]):
    if 'your.email@company.com' in u.get('emailAddress','').lower():
        print(u['id'], u['emailAddress'])
"
```

Store the ID — you'll need it in the cron prompt.

### 3. Create the Notion database

In Claude Code, ask:
> "Create a Notion database called 'Auto To-Do (Gong)' in my private Scratchpad page with columns: Task (title), Status (select: To Do/In Progress/Done), Source Call (url), Account (text), Call Date (date), Notes (text)"

Note the data source ID from the created database URL.

### 4. Register the cron

In Claude Code, use `CronCreate` with the prompt below, substituting your values:

**Schedule**: `7 * * * *` (every hour at :07)
**Type**: recurring

### Cron prompt template

```
You are running the Auto To-Do sync. Follow these steps exactly:

1. Read ~/claude-work/.todo-last-run. If it doesn't exist, use 1 hour ago as the start time (ISO 8601 UTC).

2. Call mcp__gong__search_calls with:
   - primaryUserIds: ["{YOUR_GONG_USER_ID}"]
   - fromDateTime: <timestamp from step 1>
   - toDateTime: <now>

3. For each call returned:
   a. Call mcp__gong__get_call_summary to get the summary
   b. Extract only action items assigned to you (the rep) — skip action items for the prospect
   c. For each action item, check if a Notion page already exists with that Source Call URL to avoid duplicates
   d. Create a Notion page in data source {YOUR_NOTION_DATASOURCE_ID} with:
      - Task: the action item text
      - Status: "To Do"
      - Source Call: the Gong call URL
      - Account: the account/company name from the call
      - Call Date: the call date
      - Notes: any relevant context from the summary

4. Write the current UTC time in ISO 8601 format to ~/claude-work/.todo-last-run

5. If no new calls or no action items found, finish silently.
```

## Notion database schema

| Property | Type | Purpose |
|----------|------|---------|
| Task | Title | The action item text |
| Status | Select | To Do / In Progress / Done |
| Source Call | URL | Gong call link (used for deduplication) |
| Account | Text | Company name from the call |
| Call Date | Date | When the call happened |
| Notes | Text | Context from the call summary |

## Notes

- The cron only adds rows — it never deletes or modifies existing ones
- Deduplication is by Source Call URL — if a call is re-processed, no duplicate rows are created
- Gong MCP `search_calls` with `primaryUserIds` scopes results to calls where you were the primary host
- The `.todo-last-run` file persists the sync state across sessions
- Claude Code crons auto-expire after 7 days — re-register with `CronCreate` if the sync stops
- Granola MCP can be added to step 3 if it is connected in Claude Code (check with `ToolSearch "granola"`)
