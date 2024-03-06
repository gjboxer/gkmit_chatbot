from .botservice import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

class EmployeeSuggestionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            text = request.data.get('text', '')
            response_data=BotService().chat_with_llm(text)
            chat_history_data = {
                'Message': text,
                'Response': response_data,
            }
            Chat_History.objects.create(**chat_history_data)

            return Response({'response': response_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)