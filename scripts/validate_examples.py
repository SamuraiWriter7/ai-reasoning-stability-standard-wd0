#!/usr/bin/env python3
"""
Validate ARSS-WD0 example YAML files against JSON Schema files.

Required Python packages:

* PyYAML
* jsonschema

Usage:
python scripts/validate_examples.py
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    print("Missing dependency: PyYAML")
    print("Install with: pip install pyyaml")
    raise SystemExit(1) from exc

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:
    print("Missing dependency: jsonschema")
    print("Install with: pip install jsonschema")
    raise SystemExit(1) from exc

REPO_ROOT = Path(__file__).resolve().parents[1]

VALIDATION_TARGETS = [
{
"name": "stability assessment example",
"example": REPO_ROOT / "examples" / "stability-assessment.example.yaml",
"schema": REPO_ROOT / "schemas" / "stability-assessment.schema.json",
"required": True,
},
{
"name": "conformance statement example",
"example": REPO_ROOT / "examples" / "conformance-statement.example.yaml",
"schema": REPO_ROOT / "schemas" / "conformance-statement.schema.json",
"required": True,
},
{
"name": "trace record example",
"example": REPO_ROOT / "examples" / "trace-record.example.yaml",
"schema": REPO_ROOT / "schemas" / "trace-record.schema.json",
"required": True,
},
{
"name": "requirement mapping example",
"example": REPO_ROOT / "examples" / "requirement-mapping.example.yaml",
"schema": REPO_ROOT / "schemas" / "requirement-mapping.schema.json",
"required": False,
},
]

def load_yaml(path):
"""Load a YAML file."""
with path.open("r", encoding="utf-8") as file:
return yaml.safe_load(file)

def load_json(path):
"""Load a JSON file."""
with path.open("r", encoding="utf-8") as file:
return json.load(file)

def format_error_path(error):
"""Return a readable JSON path for a validation error."""
if not error.absolute_path:
return "$"

```
parts = ["$"]

for part in error.absolute_path:
    if isinstance(part, int):
        parts.append(f"[{part}]")
    else:
        parts.append(f".{part}")

return "".join(parts)
```

def validate_file(example_path, schema_path):
"""Validate one example file against one schema file."""
try:
data = load_yaml(example_path)
except Exception as exc:
return [f"Failed to load YAML: {example_path}\n  {exc}"]

```
try:
    schema = load_json(schema_path)
except Exception as exc:
    return [f"Failed to load JSON Schema: {schema_path}\n  {exc}"]

try:
    Draft202012Validator.check_schema(schema)
except SchemaError as exc:
    return [f"Invalid JSON Schema: {schema_path}\n  {exc.message}"]

validator = Draft202012Validator(schema, format_checker=FormatChecker())

validation_errors = sorted(
    validator.iter_errors(data),
    key=lambda err: list(err.absolute_path),
)

errors = []

for error in validation_errors:
    path = format_error_path(error)
    errors.append(f"{path}: {error.message}")

return errors
```

def main():
"""Run all validations."""
print("ARSS-WD0 example validation")
print(f"Repository root: {REPO_ROOT}")
print("")

```
total_errors = 0
skipped = 0

for target in VALIDATION_TARGETS:
    name = target["name"]
    example_path = target["example"]
    schema_path = target["schema"]
    required = target["required"]

    print(f"Validating: {name}")
    print(f"  Example: {example_path.relative_to(REPO_ROOT)}")
    print(f"  Schema:  {schema_path.relative_to(REPO_ROOT)}")

    if not example_path.exists():
        message = f"Example file not found: {example_path}"

        if required:
            print(f"  ERROR: {message}")
            total_errors += 1
        else:
            print(f"  SKIP: {message}")
            skipped += 1

        print("")
        continue

    if not schema_path.exists():
        message = f"Schema file not found: {schema_path}"

        if required:
            print(f"  ERROR: {message}")
            total_errors += 1
        else:
            print(f"  SKIP: {message}")
            skipped += 1

        print("")
        continue

    errors = validate_file(example_path, schema_path)

    if errors:
        print("  FAILED")
        for error in errors:
            print(f"    - {error}")
        total_errors += len(errors)
    else:
        print("  PASSED")

    print("")

print("Validation summary")
print(f"  Errors:  {total_errors}")
print(f"  Skipped: {skipped}")

if total_errors > 0:
    print("")
    print("Validation failed.")
    return 1

print("")
print("All available example validations passed.")
return 0
```

if **name** == "**main**":
sys.exit(main())


