from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Employee, Skill, Emp_Skill, Project, Emp_Project, Chat_History])