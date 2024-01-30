from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Employee)
admin.site.register(Skill)
admin.site.register(Emp_Skill)
admin.site.register(Project)
admin.site.register(Emp_Project)
# admin.site.register(Chat_History)

# show timestamp field in chat history
class Chat_HistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('Timestamp',)
    list_display = ('ID', 'Employee_ID', 'Message', 'Response', 'Timestamp')
    list_filter = ('Employee_ID', 'Timestamp')
    search_fields = ('Message', 'Response')
    ordering = ('Timestamp',)
admin.site.register(Chat_History, Chat_HistoryAdmin)
