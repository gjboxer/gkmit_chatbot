from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Employee, Skill, Emp_Skill, Project, Emp_Project])

# Adding Timestamp
class ChatHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('Timestamp',)
    list_display = ('ID', 'Employee_ID', 'Message', 'Response', 'Timestamp') 

admin.site.register(Chat_History, ChatHistoryAdmin)