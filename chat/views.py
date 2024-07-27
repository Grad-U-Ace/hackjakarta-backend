import json

from django.shortcuts import render
from openai import OpenAI

# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from menu.models import Menu
from menu.serializers import MenuSerializer
from .models import ChatMessage
from .serializers import ChatMessageSerializer
import openai


def processs_response(parsed_response):
    if parsed_response['action'] == 'recommend':
        # Filter menu items based on parameters
        queryset = Menu.objects.all()
        if 'category' in parsed_response['parameters']:
            queryset = queryset.filter(restaurant__category=parsed_response['parameters']['category'])
        if 'ordering' in parsed_response['parameters']:
            queryset = queryset.order_by(parsed_response['parameters']['ordering'])

        # Limit to top 5 results
        menu_items = queryset[:5]
        serializer = MenuSerializer(menu_items, many=True)
        response_data = {
            'action': 'recommend',
            'menu_items': serializer.data
        }
    elif 'question' in parsed_response:
        response_data = parsed_response
    else:
        response_data = {'error': 'Invalid response format from ChatGPT'}

        # Save ChatGPT response
    ChatMessage.objects.create(content=json.dumps(response_data), is_user=False)

    return Response(response_data)


class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    @action(detail=False, methods=['POST'])
    def send_message(self, request):
        user_message = request.data.get('content')
        if not user_message:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        ChatMessage.objects.create(content=user_message, is_user=True)

        # Get ChatGPT response
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"You are a helpful assistant that generates content."},
                    {"role": "user",
                     "content": user_message}
                ]
            )
            gpt_response = response.choices[0].message.content.strip()

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save ChatGPT response
        ChatMessage.objects.create(content=gpt_response, is_user=False)

        return Response(processs_response(json.loads(gpt_response)))

    @action(detail=False, methods=['POST'])
    def clear_chat(self, request):
        ChatMessage.objects.all().delete()
        return Response({'message': 'Chat cleared successfully'})

    def list(self, request):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
