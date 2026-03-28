# n8n Code JavaScript

Write JavaScript code in n8n Code nodes.

---

## Quick Start

```javascript
const items = $input.all();

const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}));

return processed;
```

---

## Mode Selection

**Run Once for All Items** (DEFAULT - use 95% of the time):
- Code executes once regardless of input count
- Access: `$input.all()`
- Use for: aggregation, filtering, batch processing

**Run Once for Each Item** (specialized cases):
- Code executes per item
- Access: `$input.item`
- Use for: per-item API calls, independent operations

**Decision**: Need to look at multiple items? → All Items. Fully independent? → Each Item. Not sure? → All Items.

---

## Data Access Patterns

```javascript
// All items (most common)
const allItems = $input.all();

// First item only
const firstItem = $input.first();
const data = firstItem.json;

// Current item (Each Item mode only)
const currentItem = $input.item;

// Reference other nodes
const webhookData = $node["Webhook"].json;
const httpData = $node["HTTP Request"].json;
```

---

## CRITICAL: Webhook Data Structure

```javascript
// ❌ WRONG
const name = $json.name;

// ✅ CORRECT - webhook data is under .body
const name = $json.body.name;
const webhookData = $input.first().json.body;
```

---

## Return Format

**CRITICAL**: Always return array of objects with `json` property.

```javascript
// ✅ Single result
return [{json: {field1: value1}}];

// ✅ Multiple results
return [{json: {id: 1}}, {json: {id: 2}}];

// ✅ Transformed array
return $input.all()
  .filter(item => item.json.valid)
  .map(item => ({json: {id: item.json.id}}));

// ✅ Empty result
return [];

// ❌ WRONG - object without array
return {json: {field: value}};

// ❌ WRONG - array without json wrapper
return [{field: value}];
```

---

## Top 5 Errors to Avoid

### #1: Missing Return Statement
```javascript
const items = $input.all();
// ... processing ...
// ❌ forgot return!
return items.map(item => ({json: item.json}));  // ✅
```

### #2: Expression Syntax in Code Node
```javascript
const value = "{{ $json.field }}";  // ❌
const value = $input.first().json.field;  // ✅
```

### #3: Wrong Return Format
```javascript
return {json: {result: 'ok'}};     // ❌ object
return [{json: {result: 'ok'}}];   // ✅ array
```

### #4: Missing Null Checks
```javascript
const value = item.json.user.email;           // ❌ crashes if null
const value = item.json?.user?.email || '';   // ✅ safe
```

### #5: Webhook Body Nesting
```javascript
const email = $json.email;        // ❌
const email = $json.body.email;   // ✅
```

---

## Built-in Functions

### $helpers.httpRequest()
```javascript
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data',
  headers: {'Authorization': 'Bearer token'}
});
return [{json: {data: response}}];
```

### DateTime (Luxon)
```javascript
const now = DateTime.now();
const formatted = now.toFormat('yyyy-MM-dd');
const tomorrow = now.plus({days: 1});
const lastWeek = now.minus({weeks: 1});
```

### $jmespath()
```javascript
const adults = $jmespath(data, 'users[?age >= `18`]');
const names = $jmespath(data, 'users[*].name');
```

---

## Common Patterns

### Aggregation
```javascript
const items = $input.all();
const total = items.reduce((sum, item) => sum + (item.json.amount || 0), 0);
return [{json: {total, count: items.length, average: total / items.length}}];
```

### Transformation
```javascript
return $input.all().map(item => {
  const parts = item.json.name.split(' ');
  return {json: {first: parts[0], last: parts.slice(1).join(' '), email: item.json.email}};
});
```

### Filtering + Ranking
```javascript
return $input.all()
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0))
  .slice(0, 10)
  .map(item => ({json: item.json}));
```

### Error Handling
```javascript
try {
  const response = await $helpers.httpRequest({url: '...'});
  return [{json: {success: true, data: response}}];
} catch (error) {
  return [{json: {success: false, error: error.message}}];
}
```

---

## Pre-Deploy Checklist

- [ ] Code is not empty
- [ ] Return statement exists
- [ ] Return format: `[{json: {...}}]`
- [ ] Data access: `$input.all()`, `$input.first()`, or `$input.item`
- [ ] No `{{ }}` expressions (use JS directly)
- [ ] Null checks for optional fields
- [ ] Webhook data accessed via `.body`
- [ ] Mode selection: "All Items" for most cases
