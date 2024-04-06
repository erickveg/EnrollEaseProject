# schedules/views.py

import pickle
import traceback
from django.shortcuts import render
from schedules.models import SectionModel, ScheduleModel
from .services import generate_course_list, grab_sections_with_selenium, Course, Schedule

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
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
    return render(request, 'schedules/optimal_schedule.html', {'schedules': []})

def my_schedule(request):
    return render(request, 'schedules/my-schedule.html')

def donate(request):
    return render(request, 'schedules/donate.html')

def profile(request):
    return render(request, 'schedules/profile.html')


@require_POST
def generate_schedules(request):    
    try:
        global available_sections
        data = json.loads(request.body)

        # Get the 'courses' list from the data
        selected_courses = data.get('courses')

        # with open("md_sections_pack.pkl", "rb") as f:
        #     available_sections = pickle.load(f)

        available_sections = grab_sections_with_selenium(selected_courses)
        
        # Your logic to generate schedules goes here
        schedules, user_id = generate_course_list(available_sections, selected_courses)
        schedule_dicts = [schedule.to_dict() for schedule in schedules]

        return JsonResponse({'success': True, 'schedules': schedule_dicts, 'user_id': user_id})
            # return render(request, 'schedules/optimal_schedule.html', {'schedules': schedules})
    except Exception as e:
        print()
        print("////////////////////////////////////")
        print("Error generating schedules")
        print(e)
        print(traceback.format_exc())
        print()
        return JsonResponse({'success': False, 'error_message': str(e)})
    
@require_POST
def update_scheduler(request):

    # Your logic to generate schedules goes here
    data = json.loads(request.body)

    # Get the 'courses' list from the data
    schedules = data.get('schedules')
    user_id = data.get('user_id')
    return render(request, 'schedules/scheduler.html', {'schedules': schedules, 'user_id': user_id})

@require_POST
def save_schedule(request):
    data = json.loads(request.body)
    schedule_data = data.get('schedule')
    user_id = data.get('userId')

        
     # Get or create the user
    user, created = User.objects.get_or_create(id=user_id)

    # Create a new schedule for the user
    schedule = ScheduleModel.objects.create(user=user, walk_time=schedule_data.get('walk_time'), gap_time=schedule_data.get('gap_time'))

    # Add the sections to the schedule
    for section_data in schedule_data.get('sections'):
        # Create a new section
        section = SectionModel.objects.create(
            section_name=section_data.get('section_name'),
            course=section_data.get('course'),
            course_section=section_data.get('course_section'),
            title=section_data.get('title'),
            instructor=section_data.get('instructor'),
            seats_open=','.join(str(num) for num in section_data.get('seats_open')),
            status=section_data.get('status'),
            start_time=section_data.get('start_time'),
            end_time=section_data.get('end_time'),
            days=','.join(section_data.get('days')),
            room=section_data.get('room'),
            class_type=section_data.get('class_type'),
            delivery_method=section_data.get('delivery_method')
        )
        schedule.sections.add(section)

    return JsonResponse({'success': True})

@require_GET
def get_saved_schedules(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    schedules = ScheduleModel.objects.filter(user=user)
    schedule_objects = [Schedule.from_model(schedule) for schedule in schedules]
    schedule_dicts = [schedule.to_dict() for schedule in schedule_objects if len(schedule.sections) > 0]
    return JsonResponse({'success': True, 'schedules': schedule_dicts})