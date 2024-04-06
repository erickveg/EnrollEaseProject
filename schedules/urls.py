# schedules/urls.py

from django.urls import path
from schedules import views

urlpatterns = [
    # path("", views.schedule_index, name="schedule_index"),
    # path("<int:pk>/", views.schedule_detail, name="schedule_detail"),
    path("", views.generate_course_view, name="schedule_generator"),
    path("my-schedule/", views.my_schedule, name="my_schedule"),
    path("donate/", views.donate, name="donate"),
    path("profile/", views.profile, name="profile"),
]