# n8n Node Configuration

Operation-aware node configuration guidance with property dependencies.

---

## Core Concept: Operation-Aware Configuration

**Not all fields are always required** - it depends on resource + operation!

```javascript
// Slack: post message
{resource: "message", operation: "post", channel: "#general", text: "Hello!"}

// Slack: update message (different required fields!)
{resource: "message", operation: "update", messageId: "123", text: "Updated!"}
// Note: channel NOT required for update
```

---

## Progressive Discovery: Which detail level to use?

```
Start with get_node (standard detail)     ← DEFAULT, 95% of cases
        ↓ still need more?
Use search_properties mode               ← find specific field
        ↓ still need more?
Use detail="full"                        ← complete schema, last resort
```

```javascript
// Step 1: Standard (DEFAULT)
get_node({nodeType: "nodes-base.httpRequest"})

// Step 2: Find specific property
get_node({nodeType: "nodes-base.httpRequest", mode: "search_properties", propertyQuery: "auth"})

// Step 3: Full schema (only if needed)
get_node({nodeType: "nodes-base.httpRequest", detail: "full"})
```

---

## Configuration Workflow

```
1. Identify node type + operation
2. get_node (standard detail)
3. Configure required fields
4. validate_node (profile: "runtime")
5. Fix errors, repeat until valid
6. Deploy
```

### Example: HTTP POST Request

```javascript
// Step 1: Start minimal
{method: "POST", url: "https://api.example.com/create", authentication: "none"}

// Step 2: Validate → Error: "sendBody required for POST"
// Add: sendBody: true

// Step 3: Validate → Error: "body required when sendBody=true"
// Add: body: {contentType: "json", content: {name: "={{$json.name}}"}}

// Step 4: Validate → Valid ✅
```

---

## Property Dependencies

Fields appear/disappear based on other field values:

```javascript
// HTTP Request: body only visible when
{method: "POST", sendBody: true}  // Both conditions needed

// IF node: singleValue for unary operators
{operation: "isEmpty"}  // → singleValue: true (auto-added)
{operation: "equals"}   // → value2 required (binary)
```

---

## Common Node Patterns

### Resource/Operation Nodes (Slack, Google Sheets, Airtable)
```javascript
{resource: "<entity>", operation: "<action>", ...operation-specific-fields}
```

### HTTP-Based Nodes
```javascript
{method: "GET/POST/...", url: "...", authentication: "none/predefined/..."}
// POST/PUT/PATCH → sendBody available
// sendBody=true → body required
```

### Database Nodes (Postgres, MySQL)
```javascript
{operation: "executeQuery/insert/update/delete", ...}
// executeQuery → query required
// insert → table + values required
```

### Conditional Logic (IF, Switch)
```javascript
{conditions: {string: [{value1: "...", operation: "equals", value2: "..."}]}}
// Binary operators: value1 + value2
// Unary operators: value1 + singleValue: true (auto-added)
```

---

## Anti-Patterns

### ❌ Over-configure Upfront
Start minimal, add fields only when validation requires them.

### ❌ Skip Validation
Always validate before deploying.

### ❌ Ignore Operation Context
Different operations = different required fields. Always check after changing operation.

### ❌ Jump to detail="full" Immediately
Try standard detail first (3-8K tokens vs 1-2K).

---

## Best Practices

✅ Start with `get_node` (standard detail is default)
✅ Configure required fields for operation only
✅ Validate iteratively (avg 2-3 cycles is normal)
✅ Use `search_properties` mode when a field seems missing
✅ Trust auto-sanitization for operator structure

❌ Add every possible optional field upfront
❌ Copy configs across operations without validating
❌ Manually manipulate singleValue
