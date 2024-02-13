# schedules/management/commands/populate_data.py

from django.core.management.base import BaseCommand
from schedules.services import create_and_save_objects

class Command(BaseCommand):
    help = 'Populate data in the database'

    def handle(self, *args, **options):
        # Your data creation code
        courses_data = [
    {
        "course_code": "ARCH 100",
        "sections": [
            {
                "course_section": "01",
                "title": "Survey Architecture & Const.",
                "credits": 1.0,
                "instructor": "Sessions, Michael Douglas",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "M 10:15-11:15AM, R 11:30AM-12:30PM",
                "room": "Austin 221",
                "class_type": "Arranged",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "02",
                "title": "Survey Architecture & Const.",
                "credits": 1.0,
                "instructor": "Sessions, Michael Douglas",
                "seats_open": 5,
                "status": "Reopened",
                "schedule": "W 10:15-11:15AM, R 11:30AM-12:30PM",
                "room": "Austin 221",
                "class_type": "Arranged",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "03",
                "title": "Survey Architecture & Const.",
                "credits": 1.0,
                "instructor": "Sessions, Michael Douglas",
                "seats_open": 7,
                "status": "Open",
                "schedule": "M 10:15-11:15AM, R 11:30AM-12:30PM",
                "room": "Austin 221",
                "class_type": "Arranged",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "04",
                "title": "Survey Architecture & Const.",
                "credits": 1.0,
                "instructor": "Sessions, Michael Douglas",
                "seats_open": 18,
                "status": "Open",
                "schedule": "W 10:15-11:15AM, R 11:30AM-12:30PM",
                "room": "Austin 221",
                "class_type": "Arranged",
                "delivery_method": "In-Person",
            },
            # Add more sections for ARCH 100 if needed
        ],
    },
    {
        "course_code": "BUS 100",
        "sections": [
            {
                "course_section": "01",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Morley, Robert Brinton",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "MW 10:15-11:15AM",
                "room": "Smith 220",
                "class_type": "Winter Second Block",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "02",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Morley, Robert Brinton",
                "seats_open": 10,
                "status": "Open",
                "schedule": "TR 12:45-01:45PM",
                "room": "STC 361",
                "class_type": "Winter First Block",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "03",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Hales, Michael David",
                "seats_open": 0,
                "status": "Waitlist(2)",
                "schedule": "MW 12:45-01:45PM",
                "room": "Smith 330",
                "class_type": "Winter Second Block",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "05",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Morris, Mark O.",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "M 10:15-11:15AM",
                "room": "Smith 331",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "06",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Morris, Mark O.",
                "seats_open": 7,
                "status": "Reopened",
                "schedule": "W 10:15-11:15AM",
                "room": "Smith 331",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "A1",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Holliday, Sean Patrick",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "Winter First Block",
                "delivery_method": "Online",
            },
            {
                "course_section": "A2",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Holliday, Sean Patrick",
                "seats_open": 13,
                "status": "Open",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "Winter Second Block",
                "delivery_method": "Online",
            },
            {
                "course_section": "A3",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Hansen, Andrew O.",
                "seats_open": 2,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "Online",
                "delivery_method": "Online",
            },
            {
                "course_section": "A5",
                "title": "Bus. Exploration/Orientation",
                "credits": 1.0,
                "instructor": "Saunders, Seth D.",
                "seats_open": 6,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "Online",
                "delivery_method": "Online",
            },
            # Add more sections for BUS 100 if needed
        ],
    },
    {
        "course_code": "CE 250",
        "sections": [
            {
                "course_section": "01",
                "title": "Civil Eng. Materials Science",
                "credits": 3.0,
                "instructor": "Smith, Aaron B.",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "MWF 07:45-08:45AM",
                "room": "Austin 206 Classroom",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            # Add more sections for CE 250 if needed
        ],
    },
    {
        "course_code": "CSE 325",
        "sections": [
            {
                "course_section": "A1",
                "title": ".NET Software Development",
                "credits": 3.0,
                "instructor": "Ferguson, Joshua B.",
                "seats_open": 4,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "Online",
                "delivery_method": "Online",
            },
            {
                "course_section": "A2",
                "title": ".NET Software Development",
                "credits": 3.0,
                "instructor": "Ericson, Parker Levi",
                "seats_open": 20,
                "status": "Open",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "Winter First Block",
                "delivery_method": "Online",
            },
            # Add more sections for CSE 325 if needed
        ],
    },
    {
        "course_code": "CSE 382",
        "sections": [
            {
                "course_section": "01",
                "title": "Patterns Functional Prog.",
                "credits": 3.0,
                "instructor": "Macbeth, Chad Nephi",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "MWF 12:45-01:45PM",
                "room": "STC 394",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            # Add more sections for CSE 382 if needed
        ],
    },
    {
        "course_code": "ECSE 421",
        "sections": [
            {
                "course_section": "01",
                "title": "Family/Comm. Relationships",
                "credits": 2.0,
                "instructor": "Cranmer, Jillisa",
                "seats_open": 3,
                "status": "Reopened",
                "schedule": "MW 03:15-04:15PM",
                "room": "Hinckley 333",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            # Add more sections for ECSE 421 if needed
        ],
    },
    {
        "course_code": "ED 444",
        "sections": [
            {
                "course_section": "01",
                "title": "Elem. Soc. Studies Methods",
                "credits": 2.0,
                "instructor": "Sellers, Matthew David",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "TR 10:15-11:15AM",
                "room": "Hinckley 307 Conference",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            {
                "course_section": "02",
                "title": "Elem. Soc. Studies Methods",
                "credits": 2.0,
                "instructor": "Davis, Lorie Lynn",
                "seats_open": 11,
                "status": "Open",
                "schedule": "MW 10:15-11:15AM",
                "room": "Hinckley 227",
                "class_type": "Day In-Person",
                "delivery_method": "In-Person",
            },
            # Add more sections for ED 444 if needed
        ],
    },
    {
        "course_code": "CHILD 210",
        "sections": [
            {
                "course_section": "01",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Dennis, Steven A.",
                "seats_open": -7,
                "status": "Closed",
                "schedule": "MWF 10:15-11:15AM",
                "room": "Clarke 214",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "02",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Seamons, Rhonda",
                "seats_open": 5,
                "status": "Reopened",
                "schedule": "MWF 02:00-03:00PM",
                "room": "Clarke 216",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "03",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Johnson, Bryanna",
                "seats_open": 1,
                "status": "Reopened",
                "schedule": "MWF 12:45-01:45PM",
                "room": "Clarke 351",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "04",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Hendershot, Shawnee Marie",
                "seats_open": 4,
                "status": "Reopened",
                "schedule": "TR 12:45-02:15PM",
                "room": "Clarke 214",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "05",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Godfrey, Michael Kent",
                "seats_open": 14,
                "status": "Open",
                "schedule": "TR 09:45-11:15AM",
                "room": "Clarke 216",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "06",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "McQuain, Betty H.",
                "seats_open": 1,
                "status": "Reopened",
                "schedule": "MW 01:15-02:45PM",
                "room": "Clarke 317",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "08",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Rane, Thomas R.",
                "seats_open": 5,
                "status": "Open",
                "schedule": "MWF 11:30AM-12:30PM",
                "room": "Clarke 225",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "09",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "McLaughlin, Lisa",
                "seats_open": 0,
                "status": "Closed",
                "schedule": "TR 08:00-09:30AM",
                "room": "Hinckley 371",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "11",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Hendershot, Shawnee Marie",
                "seats_open": 13,
                "status": "Open",
                "schedule": "MW 03:15-04:45PM",
                "room": "Clarke 216",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "12",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Dennis, Steven A.",
                "seats_open": 41,
                "status": "Open",
                "schedule": "MWF 11:30AM-12:30PM",
                "room": "Clarke 216",
                "class_type": "DAY",
                "delivery_method": "In-Person"
            },
            {
                "course_section": "A1",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Thedell, Lynn",
                "seats_open": 2,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A2",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Davis, Sarah",
                "seats_open": 2,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A3",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Giles, Amber",
                "seats_open": 1,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A4",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Hall, Dee Ann",
                "seats_open": 1,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A5",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Parkinson, Shanda",
                "seats_open": 4,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A6",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Nilsen, Stephanie",
                "seats_open": 2,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A7",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Pottle, Hannah Sarah",
                "seats_open": 2,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A8",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Dartt, Kevin Maurine",
                "seats_open": 1,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "A9",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Giles, Amber",
                "seats_open": 5,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            },
            {
                "course_section": "B1",
                "title": "Child Development",
                "credits": 3.0,
                "instructor": "Allred, Sarah",
                "seats_open": 6,
                "status": "Reopened",
                "schedule": "00:00-00:00AM",
                "room": "Online Class",
                "class_type": "ONLN",
                "delivery_method": "Online"
            }
        ]
    }
]

        create_and_save_objects(courses_data)
        self.stdout.write(self.style.SUCCESS('Successfully populated data'))