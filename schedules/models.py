# models.py

from django.db import models

from django.contrib.auth.models import User

class SectionModel(models.Model):
    section_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    course_section = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    seats_open = models.CharField(max_length=50)
    status = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(max_length=50)
    room = models.CharField(max_length=200)
    class_type = models.CharField(max_length=200)
    delivery_method = models.CharField(max_length=200)

class ScheduleModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sections = models.ManyToManyField(SectionModel)
    walk_time = models.IntegerField(default=0)
    gap_time = models.IntegerField(default=0)

# class School(models.Model):
#     name = models.CharField(max_length=255)

# class Course(models.Model):
#     school = models.ForeignKey(School, on_delete=models.CASCADE)
#     course_code = models.CharField(max_length=255)

# class Section(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     course_section = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     credits = models.FloatField()
#     instructor = models.CharField(max_length=255)
#     seats_open = models.IntegerField()
#     status = models.CharField(max_length=255)
#     schedule = models.CharField(max_length=255)
#     room = models.CharField(max_length=255)
#     class_type = models.CharField(max_length=255)
#     delivery_method = models.CharField(max_length=255)
#     section_name_id = models.CharField(max_length=255, unique=True, editable=False)  # Add this field

#     def save(self, *args, **kwargs):
#         # Combine course_code and course_section to create the custom_id
#         self.section_name_id = f"{self.course.course_code}_{self.course_section}"

#         # Remove spaces from the custom_id
#         self.section_name_id = self.section_name_id.replace(" ", "")

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.section_name_id
