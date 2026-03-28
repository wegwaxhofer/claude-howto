# n8n MCP Tools Expert

Master guide for using n8n-mcp MCP server tools to build workflows.

---

## Tool Categories

n8n-mcp provides tools organized into categories:

1. **Node Discovery** - search_nodes, get_node
2. **Configuration Validation** - validate_node, validate_workflow
3. **Workflow Management** - create, update, delete, activate workflows
4. **Template Library** - Search and deploy 2,700+ real workflows
5. **Data Tables** - Manage n8n data tables and rows (`n8n_manage_datatable`)
6. **Documentation & Guides** - Tool docs, AI agent guide, Code node guides

---

## Quick Reference

### Most Used Tools (by success rate)

| Tool | Use When | Speed |
|------|----------|-------|
| `search_nodes` | Finding nodes by keyword | <20ms |
| `get_node` | Understanding node operations (detail="standard") | <10ms |
| `validate_node` | Checking configurations (mode="full") | <100ms |
| `n8n_create_workflow` | Creating workflows | 100-500ms |
| `n8n_update_partial_workflow` | Editing workflows (MOST USED!) | 50-200ms |
| `validate_workflow` | Checking complete workflow | 100-500ms |
| `n8n_deploy_template` | Deploy template to n8n instance | 200-500ms |
| `n8n_manage_datatable` | Managing data tables and rows | 50-500ms |
| `n8n_autofix_workflow` | Auto-fix validation errors | 200-1500ms |

---

## Critical: nodeType Formats

**Two different formats** for different tools!

### Format 1: Search/Validate Tools
```javascript
"nodes-base.slack"
"nodes-base.httpRequest"
"nodes-langchain.agent"
```

### Format 2: Workflow Tools
```javascript
"n8n-nodes-base.slack"
"n8n-nodes-base.httpRequest"
"@n8n/n8n-nodes-langchain.agent"
```

search_nodes returns BOTH:
```javascript
{
  "nodeType": "nodes-base.slack",           // For search/validate
  "workflowNodeType": "n8n-nodes-base.slack" // For workflow tools
}
```

---

## Common Mistakes

### Mistake 1: Wrong nodeType Format
```javascript
// WRONG
get_node({nodeType: "slack"})
get_node({nodeType: "n8n-nodes-base.slack"})

// CORRECT
get_node({nodeType: "nodes-base.slack"})
```

### Mistake 2: Using detail="full" by Default
```javascript
// WRONG - 3-8K tokens, use sparingly
get_node({nodeType: "nodes-base.slack", detail: "full"})

// CORRECT - 1-2K tokens, covers 95%
get_node({nodeType: "nodes-base.slack"})  // detail="standard" is default
```

### Mistake 3: Not Using Validation Profiles
```javascript
// WRONG
validate_node({nodeType, config})

// CORRECT
validate_node({nodeType, config, profile: "runtime"})
```

### Mistake 4: Not Using Smart Parameters
```javascript
// OLD way
{type: "addConnection", source: "IF", target: "Handler", sourceIndex: 0}

// NEW way - semantic branch names
{type: "addConnection", source: "IF", target: "True Handler", branch: "true"}
{type: "addConnection", source: "Switch", target: "Handler A", case: 0}
```

### Mistake 5: Not Including intent Parameter
```javascript
// CORRECT - better AI responses
n8n_update_partial_workflow({
  id: "abc",
  intent: "Add error handling for API failures",
  operations: [...]
})
```

---

## Workflow Patterns

### Node Discovery
```javascript
search_nodes({query: "slack"})
// → nodes-base.slack, nodes-base.slackTrigger

get_node({nodeType: "nodes-base.slack", includeExamples: true})
```

### Validation Loop
```javascript
validate_node({nodeType: "nodes-base.slack", config, profile: "runtime"})
// Fix errors, repeat until clean
```

### Workflow Building (iterative, avg 56s between edits)
```javascript
n8n_create_workflow({name, nodes, connections})
n8n_validate_workflow({id})
n8n_update_partial_workflow({id, intent: "...", operations: [...]})
// Activate:
n8n_update_partial_workflow({id, operations: [{type: "activateWorkflow"}]})
```

---

## Template Usage

```javascript
// Search
search_templates({query: "webhook slack", limit: 20})
search_templates({searchMode: "by_nodes", nodeTypes: ["n8n-nodes-base.httpRequest"]})
search_templates({searchMode: "by_task", task: "webhook_processing"})

// Deploy directly
n8n_deploy_template({templateId: 2947, name: "My Workflow", autoFix: true})
```

---

## Data Tables

```javascript
n8n_manage_datatable({action: "createTable", name: "Contacts", columns: [{name: "email", type: "string"}]})
n8n_manage_datatable({action: "getRows", tableId: "dt-123", filter: {filters: [{columnName: "status", condition: "eq", value: "active"}]}})
n8n_manage_datatable({action: "insertRows", tableId: "dt-123", data: [{email: "a@b.com"}]})
n8n_manage_datatable({action: "updateRows", tableId: "dt-123", filter: {...}, data: {status: "inactive"}, dryRun: true})
```

---

## Tool Availability

**Always Available** (no n8n API needed):
- search_nodes, get_node, validate_node, validate_workflow
- search_templates, get_template, tools_documentation

**Requires n8n API** (N8N_API_URL + N8N_API_KEY):
- n8n_create_workflow, n8n_update_partial_workflow, n8n_update_full_workflow
- n8n_list_workflows, n8n_get_workflow, n8n_delete_workflow
- n8n_test_workflow, n8n_executions, n8n_deploy_template
- n8n_workflow_versions, n8n_autofix_workflow, n8n_manage_datatable

---

## Best Practices

✅ Use `get_node({detail: "standard"})` for most use cases
✅ Specify validation profile explicitly (`profile: "runtime"`)
✅ Use smart parameters (`branch`, `case`) for clarity
✅ Include `intent` parameter in workflow updates
✅ Iterate workflows (avg 56s between edits)
✅ Validate after every significant change
✅ Use `n8n_deploy_template` for quick starts

❌ Use `detail: "full"` unless necessary
❌ Forget nodeType prefix (`nodes-base.*`)
❌ Skip validation profiles
❌ Try to build workflows in one shot
❌ Use full prefix with search/validate tools
