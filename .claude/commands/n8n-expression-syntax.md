# n8n Expression Syntax

All dynamic content in n8n uses **double curly braces**: `{{expression}}`

## Core Variables

**$json** - Access current node output:
```javascript
{{$json.fieldName}}
{{$json.nested.property}}
{{$json.items[0].name}}
```

**$node** - Reference other nodes:
```javascript
{{$node["Node Name"].json.fieldName}}
```
Node names must be in quotes, are case-sensitive, and must match exactly.

**$now** - Current timestamp:
```javascript
{{$now}}
{{$now.toFormat('yyyy-MM-dd')}}
{{$now.plus({days: 7})}}
```

**$env** - Environment variables:
```javascript
{{$env.API_KEY}}
```

## Critical: Webhook Data Structure

Webhook data is **NOT** at root level. The structure wraps user data under `.body`:

```javascript
{
  "headers": {...},
  "params": {...},
  "query": {...},
  "body": {
    "name": "John",
    "email": "john@example.com"
  }
}
```

**Correct access**: `{{$json.body.name}}` NOT `{{$json.name}}`

## Common Patterns

- Nested fields: `{{$json.user.email}}`
- Array access: `{{$json.data[0].name}}`
- Bracket notation for spaces: `{{$json['field name']}}`
- Reference nodes: `{{$node["HTTP Request"].json.data}}`

## When NOT to Use Expressions

**Code Nodes** use direct JavaScript:
```javascript
// ✅ CORRECT
const email = $json.email;

// ❌ WRONG
const email = '={{$json.email}}';
```

**Webhook paths and credentials** don't use expressions.

## Validation Rules

1. Always wrap in `{{ }}`
2. Use quotes for names with spaces
3. Match exact node names (case-sensitive)
4. No nested `{{{}}}`

## Common Quick Fixes

| Error | Fix |
|-------|-----|
| `$json.field` | `{{$json.field}}` |
| `{{$json.field name}}` | `{{$json['field name']}}` |
| `{{$node.HTTP Request}}` | `{{$node["HTTP Request"]}}` |
| `{{$json.name}}` (webhook) | `{{$json.body.name}}` |
| `'={{$json.email}}'` (Code) | `$json.email` |

## Essential Best Practices

✅ Always use `{{ }}` for dynamic content
✅ Use bracket notation for spaced field names
✅ Reference webhook data from `.body`
❌ Don't use expressions in Code nodes
❌ Don't forget quotes around spaced node names
