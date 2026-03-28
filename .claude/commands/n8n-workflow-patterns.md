# n8n Workflow Patterns

Proven workflow architectural patterns from real n8n workflows.

---

## The 5 Core Patterns

1. **Webhook Processing** (Most Common)
   - Pattern: Webhook → Validate → Transform → Respond/Notify

2. **HTTP API Integration**
   - Pattern: Trigger → HTTP Request → Transform → Action → Error Handler

3. **Database Operations**
   - Pattern: Schedule → Query → Transform → Write → Verify

4. **AI Agent Workflow**
   - Pattern: Trigger → AI Agent (Model + Tools + Memory) → Output

5. **Scheduled Tasks**
   - Pattern: Schedule → Fetch → Process → Deliver → Log

---

## Pattern Selection Guide

**Webhook Processing** - Receiving data from external systems, integrations
**HTTP API Integration** - Fetching data from external APIs, data pipelines
**Database Operations** - Syncing between databases, ETL workflows
**AI Agent Workflow** - Conversational AI, multi-step reasoning with tools
**Scheduled Tasks** - Recurring reports, periodic data fetching

---

## Workflow Creation Checklist

### Planning
- [ ] Identify the pattern (webhook, API, database, AI, scheduled)
- [ ] List required nodes (use search_nodes)
- [ ] Plan error handling strategy

### Implementation
- [ ] Create workflow with appropriate trigger
- [ ] Add data source nodes
- [ ] Configure authentication/credentials
- [ ] Add transformation nodes (Set, Code, IF)
- [ ] Add output/action nodes

### Validation
- [ ] Validate each node (validate_node)
- [ ] Validate complete workflow (validate_workflow)
- [ ] Test with sample data

### Deployment
- [ ] Activate with `activateWorkflow` operation
- [ ] Monitor first executions

---

## Data Flow Patterns

**Linear**: `Trigger → Transform → Action → End`

**Branching**: `Trigger → IF → [True Path] / [False Path]`

**Parallel**: `Trigger → [Branch 1] → Merge / [Branch 2] ↗`

**Loop**: `Trigger → Split in Batches → Process → Loop`

**Error Handler**: `Main Flow → [Success] / [Error Trigger → Handler]`

---

## Common Gotchas

### Webhook Data Structure
```javascript
❌ {{$json.email}}
✅ {{$json.body.email}}
```

### Node Execution Order
- v0: Top-to-bottom (legacy)
- v1: Connection-based (recommended) — set in workflow settings

### Expression Errors
Always use `{{}}` around expressions in node fields.

---

## Quick Start Examples

### Webhook → Slack
```
1. Webhook (POST)
2. Set (map fields)
3. Slack (post to #notifications)
```

### Scheduled Report
```
1. Schedule (daily 9 AM)
2. HTTP Request (fetch data)
3. Code (aggregate)
4. Email (send report)
5. Error Trigger → Slack (on failure)
```

### AI Assistant
```
1. Webhook (receive message)
2. AI Agent
   ├─ OpenAI Chat Model (ai_languageModel)
   ├─ HTTP Request Tool (ai_tool)
   └─ Window Buffer Memory (ai_memory)
3. Webhook Response
```

### Database Sync
```
1. Schedule (every 15 min)
2. Postgres (query new records)
3. IF (check if records exist)
4. MySQL (insert records)
5. Postgres (update sync timestamp)
```

---

## Pattern Statistics

| Trigger | Usage |
|---------|-------|
| Webhook | 35% |
| Schedule | 28% |
| Manual | 22% |
| Service triggers | 15% |

| Transformation | Usage |
|----------------|-------|
| Set | 68% |
| Code | 42% |
| IF | 38% |
| Switch | 18% |

---

## Best Practices

✅ Start with the simplest pattern
✅ Use error handling on all workflows
✅ Test with sample data before activation
✅ Use descriptive node names
✅ Build iteratively (avg 56s between edits)

❌ Skip validation before activation
❌ Hardcode credentials in parameters
❌ Forget to handle empty data cases
❌ Deploy without testing
