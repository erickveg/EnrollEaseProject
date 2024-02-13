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

class SimpleSection:
    def __init__(self, section_name, time, days):
        self.section_name = section_name
        self.time = time
        self.days = [d for d in days if d.isalpha()]

    def __str__(self):
        days_str = "".join(self.days)
        return f"{self.section_name} {self.time} {days_str}"
    
    def __repr__(self):
        days_str = "".join(self.days)
        return f"{self.section_name} {self.time} {days_str}"

def generate_course_list(): # The parameter should be a list of desired classes

    desired_classes = ["ED 444", "CHILD 210", "CSE 382", "BUS 100"] # input has to have a space between the course code and the course number
    # Fetch data from the database
    sections = Section.objects.all()

    simple_sections = []

    for section in sections:
        if section.course.course_code in desired_classes:
            section_name = section.section_name_id
            schedules = section.schedule.split(",")
            for schedule in schedules:
                days = ""
                times = ""

                if schedule != "00:00-00:00AM":
                    days = schedule.split(" ")[0] 
                    times = schedule.split(" ")[1]
                    times = _get_standard_time(times)
                else:
                    days = "X"
                    times = "00:00-00:00"

                simple_section = SimpleSection(section_name, times, days)
                simple_sections.append(simple_section)

    sections_combinations = generate_sections_combinations(simple_sections)    
    viable_combinations = select_viable_combinations(sections_combinations, desired_classes)

    course_list_dicts = [
    [
        {'section_name': section.section_name, 'time': section.time, 'days': section.days}
        for section in inner_list
    ]
    for inner_list in viable_combinations[:5]
    ]

    return course_list_dicts


    # Find the combination with the same length as the desired_classes
    # TODO:
    # Fix this cases [BUS100_A5 00:00-00:00 X, CSE382_01 1245-1345 MWF, ED444_01 1015-1115 TR, CHILD210_05 0945-1115 TR] ED444 and CHILD210 are crashing.


def same_code_in_combination(section, combination):
    for s in combination:
        if section.section_name.split("_")[0] in s.section_name.split("_")[0]:
            return True
    return False

def same_time_in_combination(section, combination):
    for s in combination:
        if section.time == s.time:
            return True
    return False

def same_days_in_combination(section, combination):
    for s in combination:
        return any(item in s.days for item in section.days)


def generate_sections_combinations(sections):
    
    master_combinations = []
    combinations = []

    for i in range(len(sections)):
        primary_course = sections[i]
        combinations.append([primary_course])

        for k in range(len(sections[i+1:])): # iterate through the rest of the lists
            secondary_course = sections[i+1+k]
            
            combinations_length = len(combinations)
            for c in range(combinations_length):
                combination = combinations[c]

                # if the secondary_course code is not in the list of combinations AND
                # if the seconday_course is not in the same list sub-list
                if not same_code_in_combination(secondary_course, combination) and\
                (not same_time_in_combination(secondary_course, combination) or\
                    (same_time_in_combination(secondary_course, combination) and not same_days_in_combination(secondary_course, combination))):   
                    temp_comb = combination[:]
                    temp_comb.append(secondary_course)
                    combinations.append(temp_comb)

        master_combinations.append(combinations)
        combinations = []
        
    return master_combinations

def select_viable_combinations(master_combinations, desired_classes):
    viable_combinations = []

    for m in master_combinations:
        for combination in m:
            if len(combination) == len(desired_classes):
                viable_combinations.append(combination)

    return viable_combinations

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



                            
                
    
