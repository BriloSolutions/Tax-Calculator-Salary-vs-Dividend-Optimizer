from __future__ import annotations

from datetime import date

import streamlit as st

from tax_calculator.calculations import (
    build_tax_bases,
    calc_net_salary_for_job_lumpsum,
)
from tax_calculator.models import DeductionInputs, DividendInputs, PayrollInputs
from tax_calculator.rates import Rates2025


def main() -> None:
    st.set_page_config(page_title="Zurich 2025 Tax Calculator (Offline)")
    st.title("Zurich 2025 Tax Calculator (Offline)")
    st.caption(
        "Offline scaffold for Zurich 2025 tax bases (federal + canton). "
        "Tariff engines are still pending."
    )

    st.header("Salary & Payroll")
    gross_salary = st.number_input("Gross salary (annual)", value=108_000.0, step=1000.0)
    ahv = st.number_input("AHV/IV/EO employee", value=5_724.0, step=100.0)
    alv = st.number_input("ALV employee", value=1_188.0, step=100.0)
    nbu = st.number_input("UVG NBU employee", value=1_109.40, step=50.0)
    bvg = st.number_input("BVG employee", value=2_574.0, step=100.0)
    withholding = st.number_input(
        "Quellensteuer withheld", value=10_767.60, step=100.0
    )
    lohnausweis_net = st.number_input(
        "Lohnausweis net salary (optional, 0 = auto)",
        value=0.0,
        step=100.0,
    )
    lohnausweis_net_value = lohnausweis_net if lohnausweis_net > 0 else None

    st.header("Dividends")
    dividend_gross = st.number_input("Gross dividend", value=30_000.0, step=1000.0)
    dividend_withholding = st.number_input(
        "Dividend withholding tax (VST)", value=10_500.0, step=500.0
    )
    qualified = st.checkbox("Qualified participation", value=True)
    payment_date = st.date_input("Dividend payment date", value=date(2025, 6, 30))

    st.header("Deductions")
    health_premiums = st.number_input(
        "Health insurance premiums", value=4_392.0, step=100.0
    )
    job_method = st.selectbox(
        "Job expenses method",
        options=["lump_sum", "actual", "manual"],
        index=0,
    )
    job_manual = st.number_input(
        "Job expenses manual amount", value=0.0, step=100.0
    )
    commute_actual = st.number_input("Commuting actual", value=0.0, step=100.0)
    meals_actual = st.number_input("Meals actual", value=0.0, step=100.0)
    other_actual = st.number_input("Other actual job expenses", value=0.0, step=100.0)
    pillar_3a = st.number_input("Pillar 3a contribution", value=0.0, step=100.0)

    payroll = PayrollInputs(
        gross_salary_annual=gross_salary,
        ahv_iv_eo_employee=ahv,
        alv_employee=alv,
        uvg_nbu_employee=nbu,
        bvg_employee=bvg,
        withholding_tax_annual=withholding,
        lohnausweis_net_salary=lohnausweis_net_value,
    )
    dividends = DividendInputs(
        gross_dividend=dividend_gross,
        withholding_tax=dividend_withholding,
        payment_date=payment_date,
        qualified_participation=qualified,
    )
    deductions = DeductionInputs(
        health_insurance_premiums=health_premiums,
        job_expense_method=job_method,
        job_expense_manual_amount=job_manual if job_manual > 0 else None,
        commuting_actual=commute_actual,
        meals_actual=meals_actual,
        other_actual=other_actual,
        pillar_3a_contribution=pillar_3a,
    )

    rates = Rates2025()
    bases = build_tax_bases(payroll, dividends, deductions, rates)
    net_salary = calc_net_salary_for_job_lumpsum(payroll)

    st.header("Results")
    st.metric("Net salary (for job lump sum)", f"{net_salary:,.2f}")
    st.metric("Taxable income (federal)", f"{bases.taxable_income_federal:,.2f}")
    st.metric("Taxable income (Zurich)", f"{bases.taxable_income_zh:,.2f}")
    st.info(
        "Income tax tariff engines are not implemented yet. "
        "These values represent taxable income bases only."
    )


if __name__ == "__main__":
    main()
