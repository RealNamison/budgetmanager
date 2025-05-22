# Reporting Guide

This guide explains how to generate and interpret reports and charts with **BudgetManager**.

## Summary Reports

### Monthly Summary

```bash
budgetmgr summary -y 2025 -m 5
```

**Example Output**

```
Category       Total
------------   --------
groceries      -350.75
salary         2500.00
entertainment  -120.00
```

### Yearly Summary

```bash
budgetmgr summary -y 2025
```

**CSV Export**

```bash
budgetmgr summary -y 2025 -e csv > summary_2025.csv
```

CSV format:

```
category,amount
groceries,-350.75
salary,2500.00
entertainment,-120.00
```

## Chart Visualization

### ASCII Chart

```bash
budgetmgr chart -s 2025-05-01 -e 2025-05-31
```

**Example Output**

```
groceries       ████████████████ 350.75
entertainment   ██████ 120.00
transport       █████████ 90.50
```

### Image Export

Export chart to PNG:

```bash
budgetmgr chart -s 2025-05-01 -e 2025-05-31 --png
```

Creates `chart.png` in 'data/processed/charts/' directory.

## Combining Reports

```bash
budgetmgr summary -y 2025 -e csv > summary_2025.csv
budgetmgr chart -s 2025-05-01 -e 2025-05-31 --svg
```
