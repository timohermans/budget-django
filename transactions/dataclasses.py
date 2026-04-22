from dataclasses import field, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transactions.models import Transaction


@dataclass
class WeekSummary:
    week_number: int
    budget: float
    spent: float
    left: float
    transactions: list["Transaction"] = field(default_factory=list)


@dataclass
class BalanceSummary:
    iban: str
    balance: float
    transactions: list["Transaction"] = field(default_factory=list)


@dataclass
class Summary:
    income: float
    expenses: float
    spent: float
    left: float
    budget: float
    weeks: dict[int, WeekSummary] = field(default_factory=dict)
    income_transactions: list["Transaction"] = field(default_factory=list)
    expense_transactions: list["Transaction"] = field(default_factory=list)
    income_transactions: list["Transaction"] = field(default_factory=list)
    expense_transactions: list["Transaction"] = field(default_factory=list)
    iban_balances: dict[str, BalanceSummary] = field(default_factory=dict)
