from django.urls import path

from budget import views


urlpatterns = [
    path('', views.IndexView.as_view()),
    path('<int:year>/<int:month>', views.IndexView.as_view()),
    path('overview/<int:year>/<int:month>', views.OverviewView.as_view())
]
