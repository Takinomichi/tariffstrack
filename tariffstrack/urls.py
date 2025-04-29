from django.urls import path

from . import views

app_name = "tariffstrack"
urlpatterns = [
    # ex: /tariffstrack/
    path("", views.index, name="index"),
    # ex: /poltariffsls/CA/
    path("<str:country_id>/", views.country, name="country"),
]
