from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RateEntry:
    year: int
    value: float
    source_url: str
    last_verified: date


class Rates2025:
    def __init__(self) -> None:
        self._registry = {
            "zh_job_expense_lump_sum_percent": RateEntry(
                year=2025,
                value=0.03,
                source_url="https://www.zh.ch/de/steuern-finanzen/steuern/steuernatuerliche-personen/abzuege-berufsauslagen.html",
                last_verified=date(2025, 1, 15),
            ),
            "zh_job_expense_lump_sum_min": RateEntry(
                year=2025,
                value=2000.0,
                source_url="https://www.zh.ch/de/steuern-finanzen/steuern/steuernatuerliche-personen/abzuege-berufsauslagen.html",
                last_verified=date(2025, 1, 15),
            ),
            "zh_job_expense_lump_sum_max": RateEntry(
                year=2025,
                value=4000.0,
                source_url="https://www.zh.ch/de/steuern-finanzen/steuern/steuernatuerliche-personen/abzuege-berufsauslagen.html",
                last_verified=date(2025, 1, 15),
            ),
            "federal_dividend_qualified_share": RateEntry(
                year=2025,
                value=0.70,
                source_url="https://www.estv.admin.ch/estv/de/home/estv/steuerrecht/steuerrecht-direkte-bundessteuer.html",
                last_verified=date(2025, 1, 15),
            ),
            "zh_dividend_qualified_share": RateEntry(
                year=2025,
                value=0.50,
                source_url="https://www.zh.ch/de/steuern-finanzen/steuern/steuernatuerliche-personen/teilbesteuerung.html",
                last_verified=date(2025, 1, 15),
            ),
            "withholding_tax_dividend_rate": RateEntry(
                year=2025,
                value=0.35,
                source_url="https://www.estv.admin.ch/estv/de/home/verrechnungssteuer/verrechnungssteuer.html",
                last_verified=date(2025, 1, 15),
            ),
            "zh_health_insurance_cap": RateEntry(
                year=2025,
                value=0.0,
                source_url="https://www.zh.ch/de/steuern-finanzen/steuern/steuernatuerliche-personen/abzuege-versicherungspraemien.html",
                last_verified=date(2025, 1, 15),
            ),
            "federal_health_insurance_cap": RateEntry(
                year=2025,
                value=0.0,
                source_url="https://www.estv.admin.ch/estv/de/home/direkte-bundessteuer/steuerabzuege.html",
                last_verified=date(2025, 1, 15),
            ),
            "pillar_3a_max_with_bvg": RateEntry(
                year=2025,
                value=0.0,
                source_url="https://www.bsv.admin.ch/bsv/de/home/sozialversicherungen/bv/grundlagen-und-gesetze/gebundene-selbstvorsorge.html",
                last_verified=date(2025, 1, 15),
            ),
        }

    def get(self, key: str) -> RateEntry:
        if key not in self._registry:
            raise KeyError(f"Rate '{key}' not found in registry.")
        return self._registry[key]

    def value(self, key: str) -> float:
        return self.get(key).value

    def override(self, key: str, value: float, source_url: str, verified: date) -> None:
        self._registry[key] = RateEntry(
            year=2025,
            value=value,
            source_url=source_url,
            last_verified=verified,
        )
