import datetime
from typing import Any, cast

from django.views.generic import TemplateView

from transactions.models import Transaction
from user.type import User


class IndexView(TemplateView):
    template_name = "budget/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if "year" not in context:
            context["year"] = datetime.date.today().year
            context["month"] = datetime.date.today().month
        return context


class OverviewView(TemplateView):
    template_name = "budget/overview.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        year = context["year"]
        month = context["month"]
        user = cast(User, self.request.user)
        context["summary"] = Transaction.objects.get_summary_for(
            year, month, iban=None, user=user
        )
        return context
