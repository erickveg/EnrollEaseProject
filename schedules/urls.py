# schedules/urls.py

from django.urls import path
from schedules import views

urlpatterns = [
    path("", views.schedule_index, name="schedule_index"),
    path("<int:pk>/", views.schedule_detail, name="schedule_detail"),
    path("optimal_schedule", views.generate_course_view, name="optimal_schedule"),
]