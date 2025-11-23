# Utilities Module — Python Testing Project

This project contains a small collection of utility functions and accompanying unit tests.  
It is designed to help you understand Python mappings, nested data access, JSON retrieval, and memoization, while practicing writing unit tests using `unittest` and `parameterized`.

---

## 📂 Project Structure

project/
│
├── utils.py              # Contains access_nested_map, get_json, memoize
├── test_utils.py         # Unit tests for utils.py
└── README.md             # Documentation


---

## 🔧 utils.py — Functions Overview

### 1. **access_nested_map(nested_map, path)**  
Accesses values inside a nested dictionary using a sequence of keys.

**Example:**

```python
from utils import access_nested_map

nested = {"a": {"b": {"c": 1}}}
print(access_nested_map(nested, ["a", "b", "c"]))  # Output: 1
