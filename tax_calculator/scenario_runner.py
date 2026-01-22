from __future__ import annotations

from datetime import date

from .calculations import build_tax_bases
from .models import (
    DeductionInputs,
    DividendInputs,
    PayrollInputs,
    PersonProfile,
    Scenario,
    WealthInputs,
)
from .rates import Rates2025


def build_baseline_scenario() -> Scenario:
    person = PersonProfile(
        age=30,
        civil_status="single",
        residence_municipality="Zurich (Seebach)",
        canton="ZH",
        has_children=False,
        pays_church_tax=False,
        permit_type="B",
        taxed_at_source=True,
        tax_year=2025,
    )
    payroll = PayrollInputs(
        gross_salary_annual=108_000.0,
        ahv_iv_eo_employee=5_724.0,
        alv_employee=1_188.0,
        uvg_nbu_employee=1_109.40,
        bvg_employee=2_574.0,
        withholding_tax_annual=10_767.60,
        lohnausweis_net_salary=None,
    )
    dividends = DividendInputs(
        gross_dividend=30_000.0,
        withholding_tax=10_500.0,
        payment_date=date(2025, 6, 30),
        qualified_participation=True,
    )
    deductions = DeductionInputs(
        health_insurance_premiums=4_392.0,
        job_expense_method="lump_sum",
        job_expense_manual_amount=None,
        commuting_actual=0.0,
        meals_actual=0.0,
        other_actual=0.0,
        pillar_3a_contribution=0.0,
    )
    wealth = WealthInputs(taxable_wealth=75_000.0)
    return Scenario(
        person=person,
        payroll=payroll,
        dividends=dividends,
        deductions=deductions,
        wealth=wealth,
    )


def run_baseline() -> None:
    scenario = build_baseline_scenario()
    rates = Rates2025()
    bases = build_tax_bases(
        scenario.payroll,
        scenario.dividends,
        scenario.deductions,
        rates,
    )
    print("Baseline taxable income (federal):", round(bases.taxable_income_federal, 2))
    print("Baseline taxable income (ZH):", round(bases.taxable_income_zh, 2))


if __name__ == "__main__":
    run_baseline()
