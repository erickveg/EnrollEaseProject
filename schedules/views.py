# schedules/views.py

from django.shortcuts import render
from schedules.models import Section
from .services import generate_course_list, grab_classes_with_selenium


def schedule_index(request):
    schedules = Section.objects.all()
    context = {
        "schedules": schedules
    }
    return render(request, "schedules/schedule_index.html", context)

def schedule_detail(request, pk):
    schedule = Section.objects.get(pk=pk)
    context = {
        "schedule": schedule
    }
    return render(request, "schedules/schedule_detail.html", context)

def generate_course_view(request):
    # grab_classes_with_selenium()
    simple_sections = generate_course_list()

    if len(simple_sections) > 0:
        return render(request, 'schedules/optimal_schedule.html', {'course_list': simple_sections})

