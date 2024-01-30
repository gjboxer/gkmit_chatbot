from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db.models import Q

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

            response_data = []
            for employee in employees:
                skills = Skill.objects.filter(emp_skill__Employee_ID=employee)
                serialized_skills = SkillSerializer(skills, many=True).data
                serialized_employee = EmployeeSerializer(employee).data
                response_data.append({'employee': serialized_employee, 'skills': serialized_skills})
            Chat_History.objects.create(Message=text,Response=response_data)
            return Response({'employees': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)