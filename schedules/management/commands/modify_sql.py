from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        UPDATE schedules_section
        SET custom_id = REPLACE(custom_id, ' ', '')
    """)