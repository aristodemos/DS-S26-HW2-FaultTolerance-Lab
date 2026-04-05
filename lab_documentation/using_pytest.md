Here are the **most useful pytest patterns**:

---

# ▶️ Run a single test

### By test file

```bash
pytest test_file.py
```

### By test function

```bash
pytest test_file.py::test_function_name
```

### By test class

```bash
pytest test_file.py::TestClassName
```

### By class method

```bash
pytest test_file.py::TestClassName::test_method_name
```

---

# ▶️ Run tests by keyword (flexible targeting)

```bash
pytest -k "login"
```

* Runs any test with `"login"` in its name
* Supports logic:

```bash
pytest -k "login and not slow"
pytest -k "api or ui"
```

---

# ▶️ Run all tests except some

### 1. Exclude by keyword

```bash
pytest -k "not slow"
```

Or multiple:

```bash
pytest -k "not slow and not integration"
```

---

### 2. Use markers (best practice for real projects)

Mark tests in code:

```python
import pytest

@pytest.mark.slow
def test_big():
    ...
```

Then exclude:

```bash
pytest -m "not slow"
```

Multiple exclusions:

```bash
pytest -m "not slow and not integration"
```

---

### 3. Skip specific files or folders

```bash
pytest --ignore=tests/integration
pytest --ignore=tests/test_slow.py
```

---

### 4. Skip inside code (conditional)

```python
import pytest

@pytest.mark.skip(reason="not ready")
def test_feature():
    ...
```

Or dynamically:

```python
@pytest.mark.skipif(condition, reason="...")
```

---

# ▶️ Bonus: Run last failed tests only

```bash
pytest --lf
```

---

# Quick mental model

* **Target specific** → `::` or `-k`
* **Exclude groups** → `-k "not ..."` or `-m "not ..."`
* **Structure-based skip** → `--ignore`
* **Clean scaling** → use markers (`@pytest.mark.slow`)
