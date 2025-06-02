# BudgetManager Documentation

Welcome to the **BudgetManager** documentation. This site provides comprehensive information on how to use, configure, and contribute to BudgetManager, a command-line application for personal finance management.

## Table of Contents

- [Getting Started](#getting-started)  
- [Usage Guide](usage.md)  
- [Reports](reports.md)  
- [Project Structure](project_structure.txt)  
- [API Reference](#api-reference)  
- [Contributing](#contributing)

---

## Getting Started

To begin using BudgetManager, please refer to the [Usage Guide](usage.md). This guide covers installation steps, configuration options, and detailed command examples.

## Usage Guide

The [Usage Guide](usage.md) describes how to interact with BudgetManager via the CLI, including adding transactions, generating summaries, managing budgets, and creating charts.

## Reports

The [Reports](reports.md) page explains how to generate financial summaries for specific periods, export to CSV, and use the reporting API directly in Python.

## Project Structure

Refer to [project_structure.txt](project_structure.txt) for a detailed overview of the repository layout, including source code modules, configuration files, and test directories.

## API Reference

BudgetManager exposes several core modules for advanced users and integration:

- **Transaction**: `src/budgetmanager/core/transaction.py`  
- **Ledger**: `src/budgetmanager/core/ledger.py`  
- **Budget**: `src/budgetmanager/core/budget.py`  
- **ReportGenerator**: `src/budgetmanager/core/report.py`  
- **Chart**: `src/budgetmanager/core/chart.py`  
- **SQLiteHandler**: `src/budgetmanager/file/sqlite_handler.py`  
- **FileHandler**: `src/budgetmanager/file/file_handler.py`  
- **JSONHandler**: `src/budgetmanager/file/json_handler.py`  
- **Timestamp**: `src/budgetmanager/utils/timestamp.py`

For detailed code documentation and examples, consult the source files located under `src/budgetmanager/`.

## Contributing

We welcome contributions! Please see the [Contributing](#contributing) section for guidelines.

### Contribution Guidelines

1. Fork the repository.  
2. Create a new branch for your feature or bugfix.  
3. Implement changes, ensuring all tests pass.  
4. Follow code style guidelines (PEP 8, type hints, Google-style docstrings).  
5. Submit a pull request with a clear description of changes.

---

Thank you for using BudgetManager! If you encounter any issues or have suggestions, please open an issue on GitHub.
