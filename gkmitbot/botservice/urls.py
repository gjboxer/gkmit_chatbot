from django.urls import path
from . import views

urlpatterns = [
    path("index",views.index,name="index"),
    path("employee-suggestion", views.EmployeeSuggestionView.as_view(), name="employee-suggestion"),
]
