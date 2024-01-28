from .models import Section, Course, School

def create_and_save_objects(courses_data):
    try:
        # Define your School instance (if needed)
        school_instance = School.objects.create(name="byui")

        # Create and save objects
        for course_data in courses_data:
            course_instance = Course.objects.create(
                school=school_instance,
                course_code=course_data["course_code"],
            )

            for section_data in course_data["sections"]:
                Section.objects.create(
                    course=course_instance,
                    course_section=section_data["course_section"],
                    title=section_data["title"],
                    credits=section_data["credits"],
                    instructor=section_data["instructor"],
                    seats_open=section_data["seats_open"],
                    status=section_data["status"],
                    schedule=section_data["schedule"],
                    room=section_data["room"],
                    class_type=section_data["class_type"],
                    delivery_method=section_data["delivery_method"],
                )

        print("Objects created and saved successfully.")

    except School.DoesNotExist:
        print("School with the specified name does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_course_list(): # The parameter should be a list of desired classes

    desired_classes = ["ED 444", "CHILD 210", "CSE 382", "BUS 100"] # inpur has to have a space between the course code and the course number
    # Fetch data from the database
    sections = Section.objects.all()

    # Separate sections by day and time
    days_times_sections = {}
    for section in sections:
        if section.course.course_code in desired_classes:
            schedules = section.schedule.split(",")
            for schedule in schedules:
                print(schedule)
                if schedule != "00:00-00:00AM":
                    days = schedule.split(" ")[0] 
                    times = schedule.split(" ")[1]
                    times = _get_standard_time(times)

                    for day in days:
                        if day in days_times_sections:
                            if times in days_times_sections[day]:
                                days_times_sections[day][times].append(section.custom_id)
                            else:
                                days_times_sections[day][times] = [section.custom_id]
                        else:
                            days_times_sections[day] = {times : [section.custom_id]}

    # Calculate optimal schedules (return a a list of sections, that should be enough to get section details)
    

    ## OPTIMAL SCHEDULES
                            
    # FIRST OPTION                              # SECOND OPTION (Winner if earliest classes are prioritized)
    
    # M: 10:15-11:15AM   : ED444_02             # M: 10:15-11:15AM   : BUS100_01
    # M: 11:30AM-12:30PM : CHILD210_08          # M: 11:30AM-12:30PM : CHILD210_08
    # M: 12:45AM-01:45PM : CSE382_01            # M: 12:45AM-01:45PM : CSE382_01
                            
    # T: 12:45AM-01:45PM  : BUS100_02           # T: 10:15-11:15AM  : ED444_01

    return days_times_sections


def _get_standard_time(time_str : str):
    times = time_str.split("-")
    
    first_time = True
    standard_time = ""


    for time in times:
        if "AM" in time:
            time = time.replace("AM", "")
            time = time.split(":")
            if time[0] == "12":
                time[0] = "00"
            time = "".join(time)
        
        elif "PM" in time:
            time = time.replace("PM", "")
            time = time.split(":")
            if time[0] != "12":
                time[0] = str(int(time[0]) + 12)
            time = "".join(time)  

        elif "PM" in time_str and ( time.split(":")[0] <= times[1].split(":")[0]):
            time = time.split(":")
            time[0] = str(int(time[0]) + 12)
            time = "".join(time)  

        else:
            time = time.replace(":", "")


        if first_time:
            standard_time += f"{time}-"
            first_time = False
        else:
            standard_time += time

    return standard_time



                            
                
    
