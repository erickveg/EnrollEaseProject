# schedules/views.py

from django.shortcuts import render
from schedules.models import Section
from .services import generate_course_list, grab_sections_with_selenium

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

available_sections = []

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
    available_sections = grab_sections_with_selenium()

    print(available_sections)
    return render(request, 'schedules/optimal_schedule.html', {'schedules': []})


@require_POST
def generate_schedules(request):    
    try:
        data = json.loads(request.body)

        # Get the 'courses' list from the data
        selected_courses = data.get('courses')
        # Your logic to generate schedules goes here
        schedules = generate_course_list(available_sections, selected_courses)
        return JsonResponse({'success': True, 'schedules': schedules})
        # return render(request, 'schedules/optimal_schedule.html', {'schedules': schedules})
    except Exception as e:
        return JsonResponse({'success': False, 'error_message': str(e)})
    
@require_POST
def update_scheduler(request):

    # Your logic to generate schedules goes here
    data = json.loads(request.body)

    # Get the 'courses' list from the data
    schedules = data.get('schedules')
    return render(request, 'schedules/scheduler.html', {'schedules': schedules})
