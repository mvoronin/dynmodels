# -*- coding: utf-8 -*-
from django.db import models, migrations


def emerge_departments(apps, schema_editor):
    list_department_names = ['HR', 'Security', 'Development', 'Research', 'Sales']

    Department = apps.get_model("hr", "Department")
    for dname in list_department_names:
        d = Department(name=dname)
        d.save()


def emerge_rooms(apps, schema_editor):
    list_room_dsc = [
        {"number": "1", "department": 1, "spots": 10},
        {"number": "2", "department": 2, "spots": 5},
        {"number": "3", "department": 3, "spots": 20},
        {"number": "3a", "department": 4, "spots": 17},
        {"number": "4", "department": 5, "spots": 24}
    ]

    Room = apps.get_model("hr", "Room")
    for d in list_room_dsc:
        r = Room(number=d['number'], department_id=d['department'], spots=d['spots'])
        r.save()


def emerge_employees(apps, schema_editor):
    list_emp_dsc = [
        {"name": "John Doe", "email": "doe@mail.com", "salary": 50000.00, "begin_date": "2015-01-01", "department": 1},
        {"name": "John Galt", "email": "galt@mail.com", "salary": 150000.00, "begin_date": "2015-01-01", "department": 4},
        {"name": "Tyler Durden", "email": "fightclub@mail.com", "salary": 104500.00, "begin_date": "2015-01-01", "department": 2},
        {"name": "Cornelius Vanderbilt", "email": "vanderbilt@mail.com", "salary": 111000.00, "begin_date": "2015-01-01", "department": 5},
        {"name": "Marla Singer", "email": "singer@mail.com", "salary": 152000.00, "begin_date": "2015-01-01", "department": 1}
    ]

    Employee = apps.get_model("hr", "Employee")
    for d in list_emp_dsc:
        e = Employee(name=d['name'], email=d['email'], salary=d['salary'], begin_date=d['begin_date'], department_id=d['department'])
        e.save()


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(emerge_departments),
        migrations.RunPython(emerge_rooms),
        migrations.RunPython(emerge_employees),
    ]
