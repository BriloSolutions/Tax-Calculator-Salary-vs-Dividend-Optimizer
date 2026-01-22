from __future__ import annotations

from dataclasses import dataclass

from .models import DeductionInputs, DividendInputs, PayrollInputs
from .rates import Rates2025


@dataclass(frozen=True)
class TaxBases:
    taxable_income_federal: float
    taxable_income_zh: float


def calc_net_salary_for_job_lumpsum(payroll: PayrollInputs) -> float:
    if payroll.lohnausweis_net_salary is not None:
        return payroll.lohnausweis_net_salary
    deductions = (
        payroll.ahv_iv_eo_employee
        + payroll.alv_employee
        + payroll.uvg_nbu_employee
        + payroll.bvg_employee
    )
    return payroll.gross_salary_annual - deductions


def calc_job_expense_deduction(
    payroll: PayrollInputs,
    deductions: DeductionInputs,
    rates: Rates2025,
) -> float:
    method = deductions.job_expense_method
    if method == "manual":
        if deductions.job_expense_manual_amount is None:
            raise ValueError("Manual job expense method selected without a value.")
        return max(deductions.job_expense_manual_amount, 0.0)
    if method == "actual":
        return max(
            deductions.commuting_actual
            + deductions.meals_actual
            + deductions.other_actual,
            0.0,
        )

    net_salary = calc_net_salary_for_job_lumpsum(payroll)
    lump_sum = net_salary * rates.value("zh_job_expense_lump_sum_percent")
    return min(
        max(lump_sum, rates.value("zh_job_expense_lump_sum_min")),
        rates.value("zh_job_expense_lump_sum_max"),
    )


def calc_insurance_premium_deduction(
    deductions: DeductionInputs,
    rates: Rates2025,
    *,
    scope: str,
) -> float:
    premiums = deductions.health_insurance_premiums
    if scope == "zh":
        cap = rates.value("zh_health_insurance_cap")
    elif scope == "federal":
        cap = rates.value("federal_health_insurance_cap")
    else:
        raise ValueError("Insurance scope must be 'zh' or 'federal'.")
    if cap <= 0:
        return premiums
    return min(premiums, cap)


def calc_dividend_taxable_federal(dividends: DividendInputs, rates: Rates2025) -> float:
    if not dividends.qualified_participation:
        return dividends.gross_dividend
    return dividends.gross_dividend * rates.value("federal_dividend_qualified_share")


def calc_dividend_taxable_zh(dividends: DividendInputs, rates: Rates2025) -> float:
    if not dividends.qualified_participation:
        return dividends.gross_dividend
    return dividends.gross_dividend * rates.value("zh_dividend_qualified_share")


def build_tax_bases(
    payroll: PayrollInputs,
    dividends: DividendInputs,
    deductions: DeductionInputs,
    rates: Rates2025,
) -> TaxBases:
    job_expense = calc_job_expense_deduction(payroll, deductions, rates)
    insurance_federal = calc_insurance_premium_deduction(
        deductions, rates, scope="federal"
    )
    insurance_zh = calc_insurance_premium_deduction(deductions, rates, scope="zh")

    bvg = payroll.bvg_employee
    pillar_3a = deductions.pillar_3a_contribution

    taxable_income_federal = (
        payroll.gross_salary_annual
        - job_expense
        - insurance_federal
        - bvg
        - pillar_3a
        + calc_dividend_taxable_federal(dividends, rates)
    )
    taxable_income_zh = (
        payroll.gross_salary_annual
        - job_expense
        - insurance_zh
        - bvg
        - pillar_3a
        + calc_dividend_taxable_zh(dividends, rates)
    )
    return TaxBases(
        taxable_income_federal=max(taxable_income_federal, 0.0),
        taxable_income_zh=max(taxable_income_zh, 0.0),
    )
