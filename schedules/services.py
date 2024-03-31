import datetime
import pickle
from .models import Section, Course, School
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
    def __init__(self, section_name, title, start_time, end_time, days):
        self.section_name = section_name
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.days = [d for d in days if d.isalpha()]

    def __str__(self):
        days_str = "".join(self.days)
        return f"{self.section_name} {self.time} {days_str}"
    
    def __repr__(self):
        days_str = "".join(self.days)
        return f"{self.section_name} {self.time} {days_str}"
    
class Schedule:
    def __init__(self, sections):
        self.sections = sections
        self.walk_time = 0
        self.gap_time = 0

    def __str__(self):
        return f"{self.sections} {self.walk_time} {self.gap_time}"
    
    def __repr__(self):
        return f"{self.sections} {self.walk_time} {self.gap_time}"
    
    def to_dict(self):
        return {
            'sections': [section.to_dict() for section in self.sections],
            'walk_time': self.walk_time,
            'gap_time': self.gap_time
        }

def generate_course_list(available_sections, selected_courses): 
    desired_classes = selected_courses

    filtered_available_sections = []

    for section in available_sections:
        if section.course in desired_classes:
            filtered_available_sections.append(section)

    sections_combinations = generate_sections_combinations(filtered_available_sections)    
    viable_combinations = select_viable_combinations(sections_combinations, desired_classes)
    schedules = generate_schedule_objects(viable_combinations)
    schedules = add_gap_time(schedules)

    return get_top_10_schedules(schedules)

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
        # if section.section_name == "CHILD210_05" and s.section_name == "ED444_01":
        #     print("hello")
        if (s.start_time <= section.start_time <= s.end_time) or (s.start_time <= section.end_time <= s.end_time):
            return True
    return False

def same_days_in_combination(section, combination):
    for s in combination:
        # if section.section_name == "CHILD210_05" and s.section_name == "ED444_01":
        #     print("hello")
        if any(item in s.days for item in section.days):
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

    for m in master_combinations:
        for combination in m:
            # TODO: Deal when not all the desired classes are in the combination
            if len(combination) == len(desired_classes):
                viable_combinations.append(combination)
    return viable_combinations

def add_gap_time(schedules):
    # Function to calculate time difference between two times
    from datetime import datetime

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
                    sum_diffs += time_diff
                    # print(f"On {day}, between {sections_in_day[i-1]['section_name']} and {sections_in_day[i]['section_name']}: {time_diff} minutes")
        
        # Add gap time to the schedule
        # schedule.gap_time = sum_diffs / days_computed if days_computed > 0 else 0
        schedule.gap_time = sum_diffs
        sections_by_day = {}
    
    return schedules
                    
def get_top_10_schedules(schedules):
    # Sort the list of Schedule objects based on their gap_time attribute
    sorted_schedules = sorted(schedules, key=lambda x: x.gap_time)
    
    # Return the top 10 schedules
    return sorted_schedules[:10]

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

def grab_sections_with_selenium():

    from selenium import webdriver
    from selenium.webdriver.common.by import By
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
    value = element.text
    print(value)

    # Click button on pop-up window
    try:
        button = driver.find_element(By.ID, "CP_V_Button1")
        button.click()
        print("Button clicked successfully!")
    except Exception as e:
        print("Button not found or does not exist on the page.")

    # Click on the "Add or Drop Classes" button
    link_element = driver.find_element(By.ID, "pg1_V_lnkAddDrop")
    link_element.click()

    # Put a "." in the Course Title search box and press "Enter
    # This will return all courses
    input_element = driver.find_element(By.ID, "pg0_V_tabSearch_txtTitleRestrictor")
    input_element.send_keys(" ")
    input_element.send_keys(Keys.ENTER)

    # TODO: Click on the "Show All" link to display all courses
    # show_all = wait.until(EC.visibility_of_element_located((By.ID, "pg0_V_lnkShowAll")))
    # show_all.click()

    # Wait until the table with id "tableCourses" is visible and all its rows are present
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#tableCourses tbody tr")))

    # TODO: Click on the "Show All" link to display all courses
    # show_all = wait.until(EC.visibility_of_element_located((By.ID, "pg0_V_lnkShowAll")))
    # show_all.click()

    # Wait until the table with id "tableCourses" is visible and all its rows are present
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#tableCourses tbody tr")))

    # Now find all table rows in the tbody
    rows = driver.find_elements(By.CSS_SELECTOR, "#tableCourses tbody tr")

    # List to hold Course objects
    courses = []
    course_codes = []

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

    # # Specify the file path where you want to save the list
    with open("course_list.pkl", "wb") as f:
        pickle.dump(courses, f)

    return courses
                
    
