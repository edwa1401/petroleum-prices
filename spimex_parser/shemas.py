from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, kw_only=True, slots=True)
class ContractSchema:
    code: str
    name: str
    base: str
    volume: str
    amount: str
    price_change_amount: str | None
    price_change_ratio: str | None
    price_min: str | None
    price_avg: str | None
    price_max: str | None
    price_market: str | None
    price_best_bid: str | None
    price_best_call: str | None
    num_of_lots: str | None


@dataclass(frozen=True, kw_only=True, slots=True)
class SectionSchema:
    name: str
    metric: str
    contracts: list[ContractSchema]


@dataclass(frozen=True, kw_only=True, slots=True)
class TradeDaySchema:
    day: date
    sections: list[SectionSchema]
