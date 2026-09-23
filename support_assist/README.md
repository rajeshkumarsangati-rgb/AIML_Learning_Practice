# Support Assist

Support Assist is a Python package that bundles Zepto policy-reference documents and exposes them through a simple module interface.

## Package structure

- `support_assist/__init__.py` – package entry point
- `support_assist/support.py` – support assistant starter class
- `support_assist/docs/` – eight Zepto policy documents

## Included policy documents

- `doc_01.txt` — Delivery Policy
- `doc_02.txt` — Returns & Refunds
- `doc_03.txt` — Membership Tiers
- `doc_04.txt` — Order Tracking
- `doc_05.txt` — Order Cancellation Policy
- `doc_06.txt` — Damaged or Missing Items
- `doc_07.txt` — Gift Cards
- `doc_08.txt` — Customer Support Hours

## Example usage

```python
from support_assist import list_policy_docs, load_policy_doc

print(list_policy_docs())
print(load_policy_doc("doc_01.txt"))
```

## Notes

This package is designed to serve as a lightweight reference module for Zepto policies and can be extended with search or Q&A logic later.
