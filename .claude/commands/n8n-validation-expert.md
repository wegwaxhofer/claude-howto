# n8n Validation Expert

Expert guidance for interpreting and resolving n8n validation errors.

---

## Core Philosophy: Validate Early, Validate Often

Typical cycle: Configure → Validate → Fix → Validate (2-3 iterations, ~23s thinking, ~58s fixing per cycle)

---

## Error Severity Levels

| Severity | Blocks Execution | Examples |
|----------|-----------------|---------|
| **Errors** | Yes | missing_required, invalid_value, type_mismatch, invalid_reference, invalid_expression |
| **Warnings** | No | best_practice, deprecated, performance |
| **Suggestions** | No | optimization, alternative |

---

## Validation Profiles

| Profile | Use When |
|---------|----------|
| `minimal` | Quick checks during editing |
| `runtime` | **Pre-deployment (recommended)** |
| `ai-friendly` | Fewer false positives for AI workflows |
| `strict` | Maximum safety for production |

```javascript
validate_node({
  nodeType: "nodes-base.slack",
  config: {...},
  profile: "runtime"  // Always specify explicitly
})
```

---

## Validation Loop Pattern

```javascript
// Step 1: Validate
const result = validate_node({nodeType, config, profile: "runtime"});

// Step 2: Check errors
if (!result.valid) {
  console.log(result.errors);  // "Missing required field: name"
}

// Step 3: Fix config
config.name = "general";

// Step 4: Validate again (repeat until clean)
```

---

## Common Error Types & Fixes

### missing_required
```
Error: "channel is required for operation 'post'"
Fix: Add required field based on operation
```

### invalid_value
```
Error: "method must be one of: GET, POST, PUT, PATCH, DELETE"
Fix: Use valid enum value
```

### type_mismatch
```
Error: "limit must be a number, got string"
Fix: Convert "100" → 100
```

### invalid_expression
```
Error: "Expression syntax error: {{$json.field name}}"
Fix: Use bracket notation: {{$json['field name']}}
```

### invalid_reference
```
Error: "Node 'HTTP Request' not found"
Fix: Check node name spelling (case-sensitive!)
```

---

## Auto-Sanitization System

Auto-sanitization runs on **ALL nodes** during **ANY** workflow update.

**What it fixes automatically:**
- Binary operators (equals, contains) → removes `singleValue`
- Unary operators (isEmpty, isNotEmpty) → adds `singleValue: true`
- IF/Switch nodes → adds missing metadata

**What it CANNOT fix:**
- Broken connections
- Branch count mismatches
- Paradoxical corrupt states

→ **Trust auto-sanitization. Don't manually add/remove `singleValue`.**

---

## False Positives: When to Accept Warnings

**Acceptable warnings:**
- Missing error handling (when prototype/test workflow)
- No retry logic (when idempotent operations)
- Unbounded queries (when data size is known)
- Deprecated nodes (when migration not yet needed)

**Always fix:**
- Missing required fields
- Invalid expressions
- Type mismatches
- Invalid references

---

## Auto-Fix Capabilities

```javascript
// Preview fixes (default - no changes applied)
n8n_autofix_workflow({
  id: "workflow-id",
  applyFixes: false,  // default
  confidenceThreshold: "medium"
})

// Apply fixes
n8n_autofix_workflow({
  id: "workflow-id",
  applyFixes: true,
  confidenceThreshold: "medium"
})
```

Can auto-fix:
- Expression format issues
- Node type version upgrades
- Webhook configuration
- Operator structure (singleValue)

---

## Best Practices

✅ Use `profile: "runtime"` for pre-deployment validation
✅ Read complete error messages before fixing
✅ Validate after every significant change
✅ Use `n8n_validate_workflow({id})` for complete workflow check
✅ Trust auto-sanitization for operator structure

❌ Ignore warnings without understanding them
❌ Skip validation and deploy directly
❌ Manually manipulate singleValue property
❌ Fix one error and assume all fixed
