from django.urls import path

from budget import views

app_name = "budget"
urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("<int:year>/<int:month>", views.IndexView.as_view(), name="index"),
    path("overview/<int:year>/<int:month>", views.OverviewView.as_view(), name="overview"),
    path("overview/<int:year>/<int:month>/<int:week>", views.OverviewView.as_view(), name="overview"),
]
