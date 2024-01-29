from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Case, When, Value, CharField, Q
from .models import Employee, Skill, Chat_History
from django.views.decorators.csrf import csrf_exempt
import json

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
            # Filter employees based on matched skills
            employees = Employee.objects.filter(
                emp_skill__Skill__Skill_Name__icontains=sentence  # Match skill name
            ).distinct().values(
                'First_Name', 'Last_Name', 'Email_Address', 'Phone_Number', 'Job_Level', 
                'Is_Remote_Employee', 'Designation'
            )

            employee_details = "\n".join([f"{employee['First_Name']} {employee['Last_Name']} ({employee['Email_Address']}) - {employee['Job_Level']}, {employee['Designation']}" for employee in employees])
            response_message = f"Certainly, here is the list of some people related with the skill:\n{employee_details}"
            
            chat_entry = Chat_History.objects.create(Message=sentence, Response=response_message)
            
            return JsonResponse({'response': response_message}, status=200)
        else:
            return JsonResponse({'error': 'Sentence is required'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)











# @csrf_exempt
# def search_skills(request):
#     if request.method == 'POST':
#         # Parse JSON data from request body
#         try:
#             data = json.loads(request.body)
#             sentence = data.get('sentence', '')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)

#         if sentence:
#             # Your existing code here
#             # Define order based on skill proficiency
#             # Retrieve employees and order them based on skill proficiency
#             # Construct response message
#             # Save chat history
#             skill_names = Skill.objects.values_list('Skill_Name', flat=True)
#             matched_skills = [skill for skill in skill_names if skill.lower() in sentence.lower()]
            
#             # Define order based on skill proficiency
#             order = Case(
#                 When(emp_skill__Skill_Proficiency='Expert', then=Value(1)),
#                 When(emp_skill__Skill_Proficiency='Intermediate', then=Value(2)),
#                 When(emp_skill__Skill_Proficiency='Beginner', then=Value(3)),
#                 default=Value(4),
#                 output_field=CharField(),
#             )

#             # Retrieve employees and order them based on skill proficiency
#             employees = Employee.objects.filter(emp_skill__Skill_Name__in=matched_skills).distinct().order_by(order).values(
#                 'First_Name', 'Last_Name', 'Email_Address', 'Phone_Number', 'Job_Level', 
#                 'Is_Remote_Employee', 'Designation', 'emp_skill__Skill_Proficiency'
#             )

#             # Construct response message
#             # employee_details = "\n".join([f"{employee['First_Name']} {employee['Last_Name']} ({employee['Email_Address']}) - {employee['Job_Level']}, {employee['Designation']}" for employee in employees])
#             # response_message = f"Certainly, here is the list of some people related with the skill:\n{employee_details}"
#             response_message = {'employees': list(employees)}

#             # Save chat history
#             chat_entry = Chat_History.objects.create(Message=sentence, Response=response_message)
            
#             return JsonResponse({'response': response_message}, status=200)
#         else:
#             return JsonResponse({'error': 'Sentence is required'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)




# @csrf_exempt
# def search_skills(request):
#     if request.method == 'POST':
#         print(request.body)
#         sentence = request.POST.get('sentence', '')
#         if sentence:
#             skill_names = Skill.objects.values_list('Skill_Name', flat=True)
#             matched_skills = [skill for skill in skill_names if skill.lower() in sentence.lower()]
            
#             # Define order based on skill proficiency
#             order = Case(
#                 When(emp_skill__Skill_Proficiency='Expert', then=Value(1)),
#                 When(emp_skill__Skill_Proficiency='Intermediate', then=Value(2)),
#                 When(emp_skill__Skill_Proficiency='Beginner', then=Value(3)),
#                 default=Value(4),
#                 output_field=CharField(),
#             )

#             # Retrieve employees and order them based on skill proficiency
#             employees = Employee.objects.filter(emp_skill__Skill_Name__in=matched_skills).distinct().order_by(order).values(
#                 'First_Name', 'Last_Name', 'Email_Address', 'Phone_Number', 'Job_Level', 
#                 'Is_Remote_Employee', 'Designation', 'emp_skill__Skill_Proficiency'
#             )

#             # Construct response message
#             employee_details = "\n".join([f"{employee['First_Name']} {employee['Last_Name']} ({employee['Email_Address']}) - {employee['Job_Level']}, {employee['Designation']}" for employee in employees])
#             response_message = f"Certainly, here is the list of some people related with the skill:\n{employee_details}"
            
#             # Save chat history
#             chat_entry = Chat_History.objects.create(Message=sentence, Response=response_message)
            
#             return JsonResponse({'response': response_message}, status=200)
#         else:
#             return JsonResponse({'error': 'Sentence is required'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)




# @csrf_exempt
# def save_chat_history(request):
#     if request.method == 'POST':
#         message = request.POST.get('message', '')
#         response = request.POST.get('response', '')
#         if message and response:
#             chat_entry = Chat_History.objects.create(Message=message, Response=response)
#             return JsonResponse({'chat_entry_id': chat_entry.id}, status=201)
#         else:
#             return JsonResponse({'error': 'Message and response are required'}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
