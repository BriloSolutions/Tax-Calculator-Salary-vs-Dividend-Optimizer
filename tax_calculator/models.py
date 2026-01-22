from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class PersonProfile:
    age: int
    civil_status: str
    residence_municipality: str
    canton: str
    has_children: bool
    pays_church_tax: bool
    permit_type: str
    taxed_at_source: bool
    tax_year: int


@dataclass(frozen=True)
class PayrollInputs:
    gross_salary_annual: float
    ahv_iv_eo_employee: float
    alv_employee: float
    uvg_nbu_employee: float
    bvg_employee: float
    withholding_tax_annual: float
    lohnausweis_net_salary: Optional[float] = None


@dataclass(frozen=True)
class DividendInputs:
    gross_dividend: float
    withholding_tax: float
    payment_date: date
    qualified_participation: bool


@dataclass(frozen=True)
class DeductionInputs:
    health_insurance_premiums: float
    job_expense_method: str
    job_expense_manual_amount: Optional[float]
    commuting_actual: float
    meals_actual: float
    other_actual: float
    pillar_3a_contribution: float


@dataclass(frozen=True)
class WealthInputs:
    taxable_wealth: float


@dataclass(frozen=True)
class Scenario:
    person: PersonProfile
    payroll: PayrollInputs
    dividends: DividendInputs
    deductions: DeductionInputs
    wealth: WealthInputs
