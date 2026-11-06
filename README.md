# Coffee Shop Order — Software Testing Lab Suite

This repository contains two independent software testing laboratory assignments:
- **Lab 6**: Code and Branch Coverage Analysis
- **Lab 7**: Fuzz Testing for Input Validation Bugs

---

## Repository Structure

```text
L6_L7_03_coffee_shop_order/
├── Lab6/
│   ├── coffee_shop_order.py   # Application module under test
│   ├── test_coffee_shop.py    # Test suite for line and branch coverage
│   ├── screenshots/           # Test execution and coverage reports
│   └── README.md              # Lab 6 instructions and coverage results
├── Lab7/
│   ├── processor.py           # Application module under test
│   ├── test_processor.py      # Hypothesis fuzz testing suite
│   ├── screenshots/           # Fuzz test execution and hardening reports
│   └── README.md              # Lab 7 instructions and fuzz testing findings
├── requirements.txt           # Project dependencies
├── .gitignore                 # Ignored files and directories
└── README.md                  # Project overview (this file)
```

---

## Setup and Environment

1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Lab Execution

### Lab 6: Code and Branch Coverage
Navigate to `Lab6/` and execute coverage checks:
```bash
cd Lab6
pytest --cov=coffee_shop_order --cov-report=term-missing --cov-branch test_coffee_shop.py
```

### Lab 7: Fuzz Testing with Hypothesis
Navigate to `Lab7/` and run Hypothesis tests:
```bash
cd Lab7
pytest -v test_processor.py
```
