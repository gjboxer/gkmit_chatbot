from django.contrib import admin
from .models import *
# Register your models here.
# register all models here from .models.py
admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(Emp_Skill)
admin.site.register(Project)
admin.site.register(Emp_Project)
admin.site.register(Chat_History)
