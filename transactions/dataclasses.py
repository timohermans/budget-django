from dataclasses import field, dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transactions.models import Transaction


@dataclass
class WeekSummary:
    week_number: int
    budget: Decimal
    spent: Decimal
    left: Decimal
    transactions: list["Transaction"] = field(default_factory=list)


@dataclass
class BalanceSummary:
    iban: str
    balance: Decimal
    transactions: list["Transaction"] = field(default_factory=list)


@dataclass
class Summary:
    income: Decimal
    expenses: Decimal
    spent: Decimal
    left: Decimal
    budget: Decimal
    weeks: dict[int, WeekSummary] = field(default_factory=dict)
    income_transactions: list["Transaction"] = field(default_factory=list)
    expense_transactions: list["Transaction"] = field(default_factory=list)
    iban_balances: dict[str, BalanceSummary] = field(default_factory=dict)
