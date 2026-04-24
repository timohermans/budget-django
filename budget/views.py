import datetime
from typing import Any, cast

from dateutil.relativedelta import relativedelta
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

        date = datetime.date(context["year"], context["month"], 1)
        context["date_previous"] = date + relativedelta(months=-1)
        context["date_next"] = date + relativedelta(months=1)
        return context


class OverviewView(TemplateView):
    template_name = "budget/overview.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # date stuff
        year = context["year"]
        month = context["month"]
        date = datetime.date(year, month, 1)
        context["month_display"] = date.strftime("%B")
        context["month_start"] = date.strftime("%d %b")
        context["month_end"] = (date + relativedelta(months=1, days=-1)).strftime("%d %b")

        user = cast(User, self.request.user)
        context["summary"] = Transaction.objects.get_summary_for(
            year, month, iban=None, user=user
        )
        return context
