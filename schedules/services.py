import datetime
import pickle
import random
# from .models import Section, Course, School
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .definitions import Course, Schedule

# def create_and_save_objects(courses_data):
#     try:
#         # Define your School instance (if needed)
#         school_instance = School.objects.create(name="byui")

#         # Create and save objects
#         for course_data in courses_data:
#             course_instance = Course.objects.create(
#                 school=school_instance,
#                 course_code=course_data["course_code"],
#             )

#             for section_data in course_data["sections"]:
#                 Section.objects.create(
#                     course=course_instance,
#                     course_section=section_data["course_section"],
#                     title=section_data["title"],
#                     credits=section_data["credits"],
#                     instructor=section_data["instructor"],
#                     seats_open=section_data["seats_open"],
#                     status=section_data["status"],
#                     schedule=section_data["schedule"],
#                     room=section_data["room"],
#                     class_type=section_data["class_type"],
#                     delivery_method=section_data["delivery_method"],
#                 )

#         print("Objects created and saved successfully.")

#     except School.DoesNotExist:
#         print("School with the specified name does not exist.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# class SimpleSection:
#     def __init__(self, section_name, title, start_time, end_time, days):
#         self.section_name = section_name
#         self.title = title
#         self.start_time = start_time
#         self.end_time = end_time
#         self.days = [d for d in days if d.isalpha()]

#     def __str__(self):
#         days_str = "".join(self.days)
#         return f"{self.section_name} {self.time} {days_str}"
    
#     def __repr__(self):
#         days_str = "".join(self.days)
#         return f"{self.section_name} {self.time} {days_str}"

# class Course:
#     def __init__(self, section_name, course, course_section, title, instructor, seats_open, status, start_time, end_time, days, room, class_type, delivery_method):
#         self.section_name = section_name
#         self.course = course
#         self.course_section = course_section
#         self.title = title
#         self.instructor = instructor
#         self.seats_open = seats_open
#         self.status = status
#         self.start_time = start_time
#         self.end_time = end_time
#         self.days = days
#         self.room = room
#         self.class_type = class_type
#         self.delivery_method = delivery_method

#     def to_dict(self):
#         return {
#             'section_name': self.section_name,
#             'course': self.course,
#             'course_section': self.course_section,
#             'title': self.title,
#             'instructor': self.instructor,
#             'seats_open': self.seats_open,
#             'status': self.status,
#             'start_time': self.start_time,
#             'end_time': self.end_time,
#             'days': self.days,
#             'room': self.room,
#             'class_type': self.class_type,
#             'delivery_method': self.delivery_method
#         }
    
#     @classmethod
#     def from_model(cls, model):
#         seats_open = list(map(int, model.seats_open.split(','))) if model.seats_open else []
#         days = model.days.split(',') if model.days else []
#         return cls(
#             model.section_name,
#             model.course,
#             model.course_section,
#             model.title,
#             model.instructor,
#             seats_open,
#             model.status,
#             model.start_time,
#             model.end_time,
#             days,
#             model.room,
#             model.class_type,
#             model.delivery_method
#         )

    
# class Schedule:
#     def __init__(self, sections):
#         self.sections = sections
#         self.walk_time = 0
#         self.gap_time = 0

#     def __str__(self):
#         return f"{self.sections} {self.walk_time} {self.gap_time}"
    
#     def __repr__(self):
#         return f"{self.sections} {self.walk_time} {self.gap_time}"
    
#     def to_dict(self):
#         return {
#             'sections': [section.to_dict() for section in self.sections],
#             'walk_time': self.walk_time,
#             'gap_time': self.gap_time
#         }
    
#     @classmethod
#     def from_model(cls, model):
#         sections = [Course.from_model(section) for section in model.sections.all()]
#         schedule = cls(sections)
#         schedule.walk_time = model.walk_time
#         schedule.gap_time = model.gap_time
#         return schedule



    

def generate_course_list(available_sections, selected_courses): 
    selected_courses = [course.upper().replace(" ", "") for course in selected_courses]

    filtered_available_sections = []

    for section in available_sections:
        if section.course in selected_courses:
            filtered_available_sections.append(section)

    sections_combinations = generate_sections_combinations(filtered_available_sections)    
    viable_combinations = select_viable_combinations(sections_combinations, selected_courses)
    schedules = generate_schedule_objects(viable_combinations)
    schedules = add_gap_time(schedules)

    return get_top_10_schedules(schedules), "579376121"

def generate_schedule_objects(viable_combinations):
    schedules = []

    for combination in viable_combinations:
        sections = []
        for section in combination:
            sections.append(section)
        schedules.append(Schedule(sections))

    return schedules

def same_code_in_combination(section, combination):
    for s in combination:
        if section.section_name.split("-")[0] in s.section_name.split("-")[0]:
            return True
    return False

def same_time_in_combination(section, combination):
    for s in combination:
        if (s.start_time <= section.start_time <= s.end_time) or (s.start_time <= section.end_time <= s.end_time):
            return True
    return False

def same_days_in_combination(section, combination):
    for s in combination:
        if any(item in s.days for item in section.days if item != "X"):
            return True
    return False


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

                if (not same_code_in_combination(secondary_course, combination)) and\
                (not same_days_in_combination(secondary_course, combination) and (same_time_in_combination(secondary_course, combination)) or\
                 not same_time_in_combination(secondary_course, combination)):   

                    temp_comb = combination[:]
                    temp_comb.append(secondary_course)
                    combinations.append(temp_comb)

        master_combinations.append(combinations)
        combinations = []
        
    return master_combinations

def select_viable_combinations(master_combinations, desired_classes):
    viable_combinations = []

    # sorted_schedules = sorted(master_combinations, key=lambda x: max(len(schedule) for schedule in x), reverse=True)

    for m in master_combinations:
        for combination in m:            
            if len(combination) == len(desired_classes):
                viable_combinations.append(combination)

    if len(viable_combinations) == 0:
        for m in master_combinations:
            for combination in m:
                if len(combination) == len(desired_classes) - 1:
                    viable_combinations.append(combination)
       
    return viable_combinations

def add_gap_time(schedules):
    # Function to calculate time difference between two times
    from datetime import datetime

    building_coords = {
        "STC": (43.81482716609083, -111.78465188594157),
        "Smith": (43.81946844117841, -111.78156583159867),
        "Hart": (43.819477716299964, -111.78513488179013),
        "Benson BEN": (43.81581970258082, -111.78326664570383), 
        "Spori": (43.82112976198168, -111.7824281188138),
        "Taylor": (43.81708422905652, -111.7820116861666),
        "Snow": (43.821432751162114, -111.78307591092198),
        "Kimball": (43.81711275584295, -111.78144440383853),
        "Clarke": (43.820310064473176, -111.78163751349007),
        "Austin": (43.81559920195993, -111.78406273556696),
        "Hinckley": (43.81626025760197, -111.77995970276748),
        "Romney": (43.820188076471176, -111.78326427081778),
        "Ricks": (43.815141193070275, -111.78117033348093),
        "Biddulph": (43.81730480509058, -111.78499971786952),
        "McKay": (43.81962547189932, -111.78268142783612),
        "ETC": (43.81419950065544, -111.78284905411786),
        "Rigby": (43.81729334232883, -111.78434583292083),
    }

    def time_difference(start_time1, end_time1, start_time2):                    
        time_format = "%H%M"
        time1 = datetime.strptime(end_time1, time_format)
        time2 = datetime.strptime(start_time2, time_format)
        return (time2 - time1).total_seconds() // 60  # Difference in minutes

    # Group sections by day
    sections_by_day = {}
    for schedule in schedules:

        days_computed = 0
        sum_diffs = 0
        walk_distance_m = 0
        walk_time = 0

        for section in schedule.sections:
            for day in section.days:
                if day not in sections_by_day:
                    sections_by_day[day] = []
                sections_by_day[day].append(section)

        # Calculate time difference between classes on the same day
        for day, sections_in_day in sections_by_day.items():
            if len(sections_in_day) > 1:  # Only consider days with more than one section
                days_computed += 1

                sections_in_day.sort(key=lambda x: x.start_time)  # Sort sections by start time
                for i in range(1, len(sections_in_day)):
                    time_diff = time_difference(                        
                        sections_in_day[i - 1].start_time,
                        sections_in_day[i - 1].end_time,
                        sections_in_day[i].start_time
                    )

                    room1 = sections_in_day[i - 1].room.split(" ")[0]
                    room2 = sections_in_day[i].room.split(" ")[0]

                    if "Online" not in [room1, room2]:
                        walk_distance_m += haversine(building_coords[room1], building_coords[room2])
                        walk_time += walking_time(walk_distance_m, 4.82) # 4.82 km/h is the average walking speed for people < 30 years old

                    sum_diffs += time_diff
        
        # Add gap time to the schedule
        schedule.gap_time = sum_diffs
        schedule.walk_time = walk_time
        sections_by_day = {}
    
    return schedules

def haversine(coord1: object, coord2: object):
    '''
    Calculate distance using the Haversine Formula
    '''
    import math

    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    # km = meters / 1000.0  # output distance in kilometers
     # km = round(km, 3)
    
    return round(meters, 3)

def walking_time(distance_meters, average_speed_kph):
    # Convert distance from meters to kilometers
    distance_km = distance_meters / 1000
    
    # Calculate time in hours
    time_hours = distance_km / average_speed_kph
    
    # Convert time from hours to minutes
    time_minutes = time_hours * 60
    
    return round(time_minutes, 1)
                    
def get_top_10_schedules(schedules):
    # Sort the list of Schedule objects based on gap_time in ascending order
    # sorted_schedules = sorted(schedules, key=lambda x: x.gap_time)

    # Sort the sorted_schedules based on the length of sections in descending order
    # sorted_schedules = sorted(sorted_schedules, key=lambda x: len(x.sections), reverse=True)
    # TODO: Prioritize non-online classes.

    # Sort the sorted_schedules based on the length of unique days in sections in ascending order
    sorted_schedules = sorted(schedules, key=lambda x: len(set(day for course in x.sections for day in course.days)))

    # Define a custom sorting key function
    # Define a custom sorting key function
    def custom_sort_key(schedule):
        # Non-online courses have higher priority, so they are sorted first
        # non_online_courses = [course for course in schedule.sections if "Online" not in course.room]
        # num_non_online_courses = len(non_online_courses)
        day_class_type_courses = [course for course in schedule.sections if course.class_type == "DAY"]
        num_day_class_type_courses = len(day_class_type_courses)

        # Return a tuple containing the gap time and the number of non-online courses
        return (-num_day_class_type_courses, schedule.gap_time )

    # Sort the sorted_schedules using the custom sorting key function
    sorted_schedules = sorted(sorted_schedules, key=custom_sort_key)

    # Return the top 10 schedules, if there are more than 10 schedules available return the top 10 and 10 random schedules
    if len(sorted_schedules) <= 20:
        return sorted_schedules[:20]
    else:
        return sorted_schedules[:10] + random.sample(sorted_schedules[10:], 10)

def _get_standard_time(time_str : str):
    times = time_str.split("-")
    
    first_time = True
    standard_time = []


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

        standard_time.append(time) 

    return standard_time

class Course:
    def __init__(self, section_name, course, course_section, title, instructor, seats_open, status, start_time, end_time, days, room, class_type, delivery_method):
        self.section_name = section_name
        self.course = course
        self.course_section = course_section
        self.title = title
        self.instructor = instructor
        self.seats_open = seats_open
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.days = days
        self.room = room
        self.class_type = class_type
        self.delivery_method = delivery_method

    def to_dict(self):
        return {
            'section_name': self.section_name,
            'course': self.course,
            'course_section': self.course_section,
            'title': self.title,
            'instructor': self.instructor,
            'seats_open': self.seats_open,
            'status': self.status,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'days': self.days,
            'room': self.room,
            'class_type': self.class_type,
            'delivery_method': self.delivery_method
        }

def grab_sections_with_selenium(selected_classes):

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup

    def get_schedules_text(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        # Find all <li> elements within the <ul> with class "schedules"
        schedule_elements = soup.select('ul.schedules li')
        schedules_list = []
        
        for schedule in schedule_elements:
            days = []
            times = ""
            room = schedule.find_all("div")[-1].get_text(strip=True)

            if room in ["Online Class", "Arranged", "Blended (part-online)", "Flexible Location"]:
                days = ["X"]
                times = "00:00-00:00AM"
            else:
                days = [d for d in schedule.get_text().split()[0] if d.isalpha()]
                times = schedule.get_text().split()[1]


            schedules_list.append({
                'days': days,
                'times': times,
                'room': room
            })

        return schedules_list


    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # Start the WebDriver and load the page
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 240) # 4 minutes
    driver.maximize_window()
    driver.get("https://student.byui.edu/ICS/Academics/")

    # Click on the "Login" button
    login_button = driver.find_element(By.ID, "jics-login-redirect-simple-button")
    login_button.click()    

    # Wait until the byui number is visible
    element = wait.until(EC.visibility_of_element_located((By.ID, "siteNavBar_welcomeBackBarLoggedIn_byuiINumber")))

    # Get the text content of the element
    user_id = element.text

    # Click button on pop-up window
    try:
        button = driver.find_element(By.ID, "CP_V_Button1")
        button.click()
        print("Button clicked successfully!")
    except Exception as e:
        print("Button not found or does not exist on the page.")

    # Click on the "Add or Drop Classes" button
    link_element = driver.find_element(By.ID, "pg1_V_lblAdvancedSearch")
    link_element.click()

    courses = []

    for selected_class in selected_classes:

        input_element = driver.find_element(By.ID, "pg0_V_txtCourseRestrictor")
        input_element.clear()
        input_element.send_keys(f"{selected_class}")
        input_element.send_keys(Keys.ENTER)

        # Wait until the table with id "tableCourses" is visible and all its rows are present
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#tableCourses tbody tr")))

        # Now find all table rows in the tbody
        rows = driver.find_elements(By.CSS_SELECTOR, "#tableCourses tbody tr")


        # Iterate through each row and extract data
        for row in rows:    
            
            cells = row.find_elements(By.CSS_SELECTOR, "td")

            if cells:
                section_name = str(cells[1].text.replace(" ", ""))
                course = str(section_name.split("-")[0])          
                course_section = str(section_name.split("-")[1])
                title = str(cells[2].text)
                instructor = str(cells[4].text)
                seats_open = [int(num.strip()) for num in str(cells[5].text).split('∕')]
                status = str(cells[6].text)
                class_type = cells[8].text
                delivery_method = cells[9].text
                schedules = get_schedules_text(cells[7].get_attribute('innerHTML'))

                for schedule in schedules:
                    room = schedule['room']
                    days = schedule['days']
                    times = _get_standard_time(schedule['times'])
                    start_time = times[0]
                    end_time = times[1]
                        
                    # Create Course object and append to list
                    course_obj = Course(section_name, course, course_section, title, instructor, seats_open, status, start_time, end_time, days, room, class_type, delivery_method)
                    courses.append(course_obj)

        # Click on the "Search Again" button
        search_again = driver.find_element(By.ID, "pg0_V_glbSearchAgain")
        search_again.click()


    # Specify the file path where you want to save the list
    # with open("md_sections_pack.pkl", "wb") as f:
    #     pickle.dump(courses, f)

    return courses
                
    
