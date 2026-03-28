# n8n Code Python

Write Python code in n8n Code nodes.

## ⚠️ JavaScript First!

**Use JavaScript for 95% of use cases.** Only use Python when:
- You need specific Python standard library functions (`statistics`, `hashlib`, etc.)
- You're significantly more comfortable with Python syntax

---

## Quick Start

```python
items = _input.all()

processed = []
for item in items:
    processed.append({
        "json": {
            **item["json"],
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }
    })

return processed
```

---

## Mode Selection

Same as JavaScript:
- **Run Once for All Items** (DEFAULT): `_input.all()` — use 95% of the time
- **Run Once for Each Item**: `_input.item` — for independent per-item logic

---

## Data Access Patterns

```python
# All items (most common)
all_items = _input.all()

# First item
first_item = _input.first()
data = first_item["json"]

# Current item (Each Item mode only)
current_item = _input.item

# Reference other nodes
webhook_data = _node["Webhook"]["json"]
```

---

## CRITICAL: Webhook Data Structure

```python
# ❌ WRONG
name = _json["name"]          # KeyError!

# ✅ CORRECT - under ["body"]
name = _json["body"]["name"]

# ✅ SAFER - use .get()
name = _json.get("body", {}).get("name", "")
```

---

## Return Format

**CRITICAL**: Always return list of dicts with `"json"` key.

```python
# ✅ Single result
return [{"json": {"field": value}}]

# ✅ Multiple results
return [{"json": {"id": 1}}, {"json": {"id": 2}}]

# ✅ List comprehension
return [{"json": item["json"]} for item in _input.all() if item["json"].get("valid")]

# ✅ Empty
return []

# ❌ WRONG - dict without list
return {"json": {"field": value}}

# ❌ WRONG - list without json
return [{"field": value}]
```

---

## CRITICAL Limitation: No External Libraries

```python
import requests  # ❌ ModuleNotFoundError
import pandas   # ❌ ModuleNotFoundError
import numpy    # ❌ ModuleNotFoundError

# ✅ Standard library ONLY:
import json, re, base64, hashlib, math, random
import urllib.parse
from datetime import datetime, timedelta
from statistics import mean, median, stdev
```

**Workarounds:**
- HTTP requests → Use HTTP Request node before Code node, OR switch to JavaScript
- Data analysis → Use `statistics` module or switch to JavaScript
- Web scraping → Use HTTP Request + HTML Extract nodes

---

## Top 5 Errors to Avoid

### #1: Importing External Libraries
```python
import requests  # ❌ Use HTTP Request node instead
```

### #2: Missing Return Statement
```python
items = _input.all()
# processing...
# ❌ forgot return!
return [{"json": item["json"]} for item in items]  # ✅
```

### #3: Wrong Return Format
```python
return {"json": {"result": "ok"}}    # ❌ dict
return [{"json": {"result": "ok"}}]  # ✅ list
```

### #4: KeyError on Dictionary Access
```python
name = _json["user"]["name"]                          # ❌ crashes
name = _json.get("user", {}).get("name", "Unknown")   # ✅ safe
```

### #5: Webhook Body Nesting
```python
email = _json["email"]              # ❌ KeyError
email = _json["body"]["email"]      # ✅
email = _json.get("body", {}).get("email", "")  # ✅ safe
```

---

## Common Patterns

### Aggregation
```python
from statistics import mean, stdev
items = _input.all()
values = [item["json"].get("amount", 0) for item in items]
return [{"json": {"total": sum(values), "mean": mean(values), "count": len(values)}}]
```

### Transformation
```python
items = _input.all()
return [
    {"json": {
        "first_name": item["json"].get("name", "").split(" ")[0],
        "email": item["json"].get("email", "").lower()
    }}
    for item in items
]
```

### Regex Extraction
```python
import re
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails = set()
for item in _input.all():
    emails.update(re.findall(email_pattern, item["json"].get("text", "")))
return [{"json": {"emails": list(emails), "count": len(emails)}}]
```

### Data Validation
```python
items = _input.all()
validated = []
for item in items:
    data = item["json"]
    errors = []
    if not data.get("email"): errors.append("Email required")
    if not data.get("name"): errors.append("Name required")
    validated.append({"json": {**data, "valid": not errors, "errors": errors or None}})
return validated
```

---

## Python (Beta) vs Python (Native)

| | Python (Beta) | Python (Native) |
|--|--|--|
| Helpers | `_input`, `_now`, `_jmespath()` | None |
| Variables | `_input.all()`, `_json` | `_items`, `_item` only |
| **Use when** | **Most cases (recommended)** | Pure Python needed |

---

## Standard Library Highlights

```python
import json                     # JSON parsing
from datetime import datetime   # Date/time
import re                       # Regex
import base64                   # Encoding
import hashlib                  # Hashing (SHA256, MD5)
import urllib.parse              # URL encoding
from statistics import mean, median, stdev
import math, random
```

---

## Pre-Deploy Checklist

- [ ] Considered JavaScript first
- [ ] Return statement exists
- [ ] Return format: `[{"json": {...}}]`
- [ ] Data access: `_input.all()`, `_input.first()`, or `_input.item`
- [ ] No external imports (only standard library)
- [ ] Using `.get()` for safe dict access
- [ ] Webhook data accessed via `["body"]`
- [ ] Mode selection: "All Items" for most cases
