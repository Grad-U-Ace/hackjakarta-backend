from django.shortcuts import render
from openai import OpenAI

# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
import openai


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
        print(gpt_response)
        ChatMessage.objects.create(content=gpt_response, is_user=False)

        return Response({
            'user_message': user_message,
            'gpt_response': gpt_response
        })

    @action(detail=False, methods=['POST'])
    def clear_chat(self, request):
        ChatMessage.objects.all().delete()
        return Response({'message': 'Chat cleared successfully'})

    def list(self, request):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
