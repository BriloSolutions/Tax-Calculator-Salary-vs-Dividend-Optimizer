"""Zurich 2025 tax calculator and salary/dividend optimizer (offline)."""

from .calculations import (
    build_tax_bases,
    calc_dividend_taxable_federal,
    calc_dividend_taxable_zh,
    calc_insurance_premium_deduction,
    calc_job_expense_deduction,
    calc_net_salary_for_job_lumpsum,
)
from .engine import TaxEngine
from .models import (
    DeductionInputs,
    DividendInputs,
    PayrollInputs,
    PersonProfile,
    Scenario,
    WealthInputs,
)
from .rates import Rates2025

__all__ = [
    "Rates2025",
    "TaxEngine",
    "PersonProfile",
    "PayrollInputs",
    "DividendInputs",
    "DeductionInputs",
    "WealthInputs",
    "Scenario",
    "calc_net_salary_for_job_lumpsum",
    "calc_job_expense_deduction",
    "calc_insurance_premium_deduction",
    "calc_dividend_taxable_federal",
    "calc_dividend_taxable_zh",
    "build_tax_bases",
]
