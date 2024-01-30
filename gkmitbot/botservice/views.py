from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db.models import Q
import random
# Create your views here.
def index(request):
    return HttpResponse("Hello World")

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializers import *
from .models import Employee, Skill, Emp_Skill

class EmployeeSuggestionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            text = request.data.get('text', '')
            words = word_tokenize(text)
            stop_words = set(stopwords.words('english'))
            words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
            query = Q()
            for word in words:
                query |= Q(emp_skill__Skill_ID__Skill_Name__icontains=word)

            employees = Employee.objects.filter(query).distinct()
            starting_lines = [
                "Hello! I found some employees who can help you learn the skills you asked for:",
                "Great question! Here are the employees with the skills you're looking for:",
                "Hi there! Check out these employees who can assist you with the skills you mentioned:",
                "Greetings! I've identified employees specializing in the skills you're interested in:",
                "Fantastic! Here are the employees that match your skill inquiry:",
                "Welcome! Explore the expertise of these employees in the requested skills:",
                "Hey! I've got the perfect employees for you. Take a look:",
                "Good to see you! Meet these skilled employees who can help:",
                "Nice inquiry! Here are the employees with the skills you're after:",
                "Hello there! Discover the talented individuals matching your skill requirements:",
                "Awesome question! Dive into the profiles of these employees:",
                "Hey, check this out! Here are some employees you'd love to connect with:",
                "Exciting news! I've found employees specializing in the skills you're interested in:",
                "Howdy! Take a look at these talented individuals with the skills you asked about:",
                "Glad you asked! Here are the employees ready to share their expertise:",
                "Impressive choice! Here are the employees who can help you with the skills you seek:",
                "Welcome aboard! Explore the talents of these employees with the requested skills:",
                "Superb! Here are the employees you've been looking for with the skills you mentioned:",
                "Good choice! Here are the skilled employees who can assist you:",
                "You're in luck! Meet the talented individuals ready to share their skills with you:",
            ]

            response_data = f"{random.choice(starting_lines)}\n"
            
            for employee in employees:
                skills = Skill.objects.filter(emp_skill__Employee_ID=employee)
                serialized_skills = SkillSerializer(skills, many=True).data
                serialized_employee = EmployeeSerializer(employee).data

                skills_str = ', '.join(skill['Skill_Name'] for skill in serialized_skills)

                response_data += f"""{serialized_employee['First_Name']} {serialized_employee['Last_Name']} - """
                response_data += f"""Address: {serialized_employee['Address']}, Phone Number: {serialized_employee['Phone_Number']}, """
                response_data += f"""Email: {serialized_employee['Email_Address']}, Joining Date: {serialized_employee['Joining_Date']}, """
                response_data += f"""Job Level: {serialized_employee['Job_Level']}, Remote Employee: {serialized_employee['Is_Remote_Employee']}, """
                response_data += f"""Job Description: {serialized_employee['Job_Description']}, Designation: {serialized_employee['Designation']} - """
                response_data += f"""Skills: {skills_str}\n"""

            chat_history_data = {
                'Message': text,
                'Response': response_data,
            }
            Chat_History.objects.create(**chat_history_data)

            return Response({'response': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)