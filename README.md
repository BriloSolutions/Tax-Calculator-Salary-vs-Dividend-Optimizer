# Zurich 2025 Tax Calculator + Salary vs Dividend Optimizer (Offline)

This repository contains an offline-first tax calculator for Switzerland (Canton Zurich, City of Zurich — Seebach) for tax year 2025, with the long-term goal of optimizing salary vs dividend extraction for a wholly owned GmbH.

## Current status

* Data models, rates registry, and deduction logic are implemented.
* Official tariff-based tax engines (federal + Zurich) are **not implemented yet**.
* A baseline scenario runner prints taxable income bases for federal and Zurich logic.

## Quick start

```bash
python -m tax_calculator.scenario_runner
```

## UI runner

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Next implementation steps

1. Populate official 2025 constants and sources in `Rates2025`.
2. Implement tariff tables for federal and Zurich tax engines.
3. Add validation harness for official calculator spot checks.
4. Build GmbH optimizer module for salary/dividend splits.
