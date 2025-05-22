---
title: BudgetManager Documentation
---

# Welcome to BudgetManager

**BudgetManager** is a simple, open-source command-line tool to help you track income and expenses, view balances, and generate detailed reports of your personal finances.

---

## Table of Contents

- [Quick Start](#quick-start)  
- [Installation](#installation)  
- [CLI Commands](#cli-commands)  
- [Reporting & Charts](#reporting--charts)  
- [Testing](#testing)  
- [License](#license)  
- [Troubleshooting](#troubleshooting)  

---

## Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/RealNamison/budgetmanager.git
   cd budgetmanager
   ```
2. **Install**  
   ```bash
   pip install .
   ```
3. **Add a transaction**  
   ```bash
   budgetmgr add -c groceries -a -25.50 -d "Lunch"
   ```
4. **View balance**  
   ```bash
   budgetmgr balance
   ```

---

## Installation

Follow these steps to get BudgetManager up and running:

1. **Requirements**  
   - Python ≥ 3.10  
   - pip (the Python package manager)

2. **Install**  
   ```bash
   pip install .
   ```

3. **Verify**  
   ```bash
   budgetmgr --help
   ```

---

## CLI Commands

| Command             | Description                                         |
|---------------------|-----------------------------------------------------|
| `budgetmgr add`     | Add income or expense transaction                   |
| `budgetmgr list`    | List all recorded transactions                      |
| `budgetmgr balance` | Show total income, expenses, and current balance    |
| `budgetmgr summary` | Generate monthly/yearly summary (with CSV export)   |
| `budgetmgr chart`   | Display ASCII chart or export PNG/SVG visualization |

For full usage and flags, see [Usage Guide](usage.md).

---

## Reporting & Charts

- **Summary**:  
  ```bash
  budgetmgr summary -y 2025 -m 5
  ```
- **CSV export**:  
  ```bash
  budgetmgr summary -y 2025 -m 5 -e csv
  ```
- **ASCII chart**:  
  ```bash
  budgetmgr chart -s 2025-05-01 -e 2025-05-31
  ```
- **PNG/SVG export**:  
  ```bash
  budgetmgr chart -s 2025-05-01 -e 2025-05-31 --png
  ```

See [Reporting Guide](reports.md) for detailed examples.

---

## Testing

Run the full test suite with:

```bash
pytest
```

Coverage reports are generated in the `coverage/` directory.

---

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for full text.

---

## Troubleshooting

- **“Command not found” error:** Make sure your Python environment’s `bin` directory is on your `PATH`.  
- **Unexpected errors?** Open an issue on GitHub with logs (`--verbose` flag).
