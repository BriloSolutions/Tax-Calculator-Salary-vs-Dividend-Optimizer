from __future__ import annotations

from dataclasses import dataclass

from .calculations import TaxBases
from .models import WealthInputs


@dataclass(frozen=True)
class TaxResult:
    federal_income_tax: float
    zh_state_tax: float
    zh_municipal_tax: float
    zh_wealth_tax: float

    @property
    def total_income_tax(self) -> float:
        return self.federal_income_tax + self.zh_state_tax + self.zh_municipal_tax

    @property
    def total_tax(self) -> float:
        return self.total_income_tax + self.zh_wealth_tax


class TaxEngine:
    def compute_federal_tax(self, bases: TaxBases) -> float:
        raise NotImplementedError("Federal tax engine is not implemented yet.")

    def compute_zh_state_and_municipal_tax(self, bases: TaxBases) -> tuple[float, float]:
        raise NotImplementedError("Zurich tax engine is not implemented yet.")

    def compute_zh_wealth_tax(self, wealth: WealthInputs) -> float:
        raise NotImplementedError("Zurich wealth tax engine is not implemented yet.")

    def compute(self, bases: TaxBases, wealth: WealthInputs) -> TaxResult:
        federal_tax = self.compute_federal_tax(bases)
        zh_state, zh_municipal = self.compute_zh_state_and_municipal_tax(bases)
        zh_wealth = self.compute_zh_wealth_tax(wealth)
        return TaxResult(
            federal_income_tax=federal_tax,
            zh_state_tax=zh_state,
            zh_municipal_tax=zh_municipal,
            zh_wealth_tax=zh_wealth,
        )
