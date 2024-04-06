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
    
    @classmethod
    def from_model(cls, model):
        seats_open = list(map(int, model.seats_open.split(','))) if model.seats_open else []
        days = model.days.split(',') if model.days else []
        print(model.start_time)
        print(type(model.start_time))
        return cls(
            model.section_name,
            model.course,
            model.course_section,
            model.title,
            model.instructor,
            seats_open,
            model.status,
            model.start_time.strftime('%H%M%S').replace(':', '')[:-2],
            model.end_time.strftime('%H%M%S').replace(':', '')[:-2],
            days,
            model.room,
            model.class_type,
            model.delivery_method
        )

    
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
    
    @classmethod
    def from_model(cls, model):
        sections = [Course.from_model(section) for section in model.sections.all()]
        schedule = cls(sections)
        schedule.walk_time = model.walk_time
        schedule.gap_time = model.gap_time
        return schedule

