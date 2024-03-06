from django.urls import path
from . import views

urlpatterns = [
    path("chat", views.EmployeeSuggestionView.as_view(), name="chat"),
]
