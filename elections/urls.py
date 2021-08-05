from django.urls import path

from . import views

app_name = 'elections'

urlpatterns = [
    path("", views.pulling_unit_result, name="pulling_unit_result"),
    path("lga-result", views.lga_result, name="lga_result"),
    path("poll-result-add", views.add_polling_unit_result,
         name="add_polling_unit_result"),
]
