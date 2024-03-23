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

def generate_course_list(available_sections, selected_courses): # The parameter should be a list of desired classes
    desired_classes = selected_courses
    # desired_classes = ["ED 444", "CHILD 210", "CSE 382", "BUS 100"] # input has to have a space between the course code and the course number
    # Fetch data from the database
    # sections = Section.objects.all()

    # simple_sections = []

    # for section in sections:
    #     if section.course.course_code in desired_classes:
    #         section_name = section.section_name_id
    #         title = section.title
    #         schedules = section.schedule.split(",")
    #         for schedule in schedules:
    #             days = ""
    #             start_time = ""
    #             end_time = ""

    #             if schedule != "00:00-00:00AM":
    #                 days = schedule.split(" ")[0] 
    #                 times = schedule.split(" ")[1]
    #                 times = _get_standard_time(times)
    #                 start_time = times[0]
    #                 end_time = times[1]
    #             else:
    #                 days = "X"
    #                 start_time = "00:00"
    #                 end_time = "00:00"

    #             simple_section = SimpleSection(section_name, title, start_time, end_time, days)
    #             simple_sections.append(simple_section)

    sections_combinations = generate_sections_combinations(available_sections)    
    viable_combinations = select_viable_combinations(sections_combinations, desired_classes)

    course_list_dicts = [
    [
        {'section_name': section.section_name, 
         'title' : section.title,
         'start_time': section.start_time,
         'end_time' : section.end_time,
         'days': section.days}
        for section in inner_list
    ]
    for inner_list in viable_combinations[:5]
    ]

    return course_list_dicts


    # Find the combination with the same length as the desired_classes
    # TODO:
    # Fix this cases [BUS100_A5 00:00-00:00 X, CSE382_01 1245-1345 MWF, ED444_01 1015-1115 TR, CHILD210_05 0945-1115 TR] ED444 and CHILD210 are crashing.
    # To fix it we might need to store times individually, and then modify the same_time_in_combination function.


def same_code_in_combination(section, combination):
    for s in combination:
        if section.section_name.split("_")[0] in s.section_name.split("_")[0]:
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

                # if the secondary_course code is not in the list of combinations AND
                # if the seconday_course is not in the same list sub-list

                # if secondary_course.section_name == "CHILD210_05" and combination[-1].section_name == "ED444_01":
                #     print("hello")

                # smd = same_days_in_combination(secondary_course, combination)
                # stc = same_time_in_combination(secondary_course, combination)
                # scic = same_code_in_combination(secondary_course, combination)

                if (not same_code_in_combination(secondary_course, combination)) and\
                (not same_days_in_combination(secondary_course, combination) and (same_time_in_combination(secondary_course, combination)) or\
                 not same_time_in_combination(secondary_course, combination)):   
                    if secondary_course.section_name == "CHILD210_05" and combination[-1].section_name == "ED444_01":
                        print("hello")

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
    def __init__(self, course, course_section, title, instructor, seats_open, status, start_time, end_time, days, room, class_type, delivery_method):
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

            if room == "Online Class":
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
    input_element.send_keys(".")
    input_element.send_keys(Keys.ENTER)

    # Wait until the table with id "tableCourses" is visible and all its rows are present
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#tableCourses tbody tr")))

    # Now find all table rows in the tbody
    rows = driver.find_elements(By.CSS_SELECTOR, "#tableCourses tbody tr")

    # List to hold Course objects
    courses = []

    # Iterate through each row and extract data
    for row in rows:    
        
        cells = row.find_elements(By.CSS_SELECTOR, "td")

        if cells:
            section_name_id = str(cells[1].text.replace(" ", ""))
            course = str(section_name_id.split("-")[0])
            course_section = str(section_name_id.split("-")[1])
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
                course_obj = Course(course, course_section, title, instructor, seats_open, status, start_time, end_time, days, room, class_type, delivery_method)
                courses.append(course_obj)

    return courses
                            
                
    
