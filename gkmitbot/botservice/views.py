from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Case, When, Value, CharField, Q
from .models import Employee, Skill, Chat_History
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Create your views here

def index(request):
    return HttpResponse('This is Index')

@csrf_exempt
def search_skills(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sentence = data.get('sentence', '')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if sentence:
            keywords = sentence.split()
            conditions = Q()
            for keyword in keywords:
                conditions |= Q(emp_skill__Skill_ID__Skill_Name__icontains=keyword)
            employees = Employee.objects.filter(conditions).distinct().values('ID', 'First_Name', 'Last_Name', 'Email_Address', 'Phone_Number', 'Job_Level', 'Designation', 'Is_Remote_Employee', 'emp_skill__Skill_ID__Skill_Name', 'emp_skill__Skill_Proficiency')

            starting_messages = [
                "Certainly, here is the list of some people related with the skill:",
                "Sure, here are the details of employees with the skill you provided:",
                "Great! Let me show you the employees who have the skill you're looking for:"
            ]

            starting_message = random.choice(starting_messages)

            if employees:
                encountered_employees = {}
                for employee in employees:
                    employee_id = employee['ID']
                    if employee_id not in encountered_employees:
                        encountered_employees[employee_id] = {
                            'ID': employee_id,
                            'First_Name': employee['First_Name'],
                            'Last_Name': employee['Last_Name'],
                            'Email_Address': employee['Email_Address'],
                            'Phone_Number': employee['Phone_Number'],
                            'Job_Level': employee['Job_Level'],
                            'Designation': employee['Designation'],
                            'Is_Remote_Employee': employee['Is_Remote_Employee'],
                            'Skills': [{
                                'Name': employee['emp_skill__Skill_ID__Skill_Name'],
                                'Proficiency': employee['emp_skill__Skill_Proficiency']
                            }]
                        }
                    else:
                        encountered_employees[employee_id]['Skills'].append({
                            'Name': employee['emp_skill__Skill_ID__Skill_Name'],
                            'Proficiency': employee['emp_skill__Skill_Proficiency']
                        })
                
                proficiency_order = {'Expert': 3, 'Intermediate': 2, 'Beginner': 1}
                sorted_employees = sorted(encountered_employees.values(), key=lambda x: proficiency_order.get(x['Skills'][0]['Proficiency'], 0), reverse=True)
                
                response_data = {
                    'message': starting_message,
                    'employees': list(encountered_employees.values())
                }
                
                chat_entry = Chat_History.objects.create(Message=sentence, Response=response_data)
                
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({'message': 'No employee found.'}, status=404)

        else:
            return JsonResponse({'error': 'Sentence is required'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

