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

fine_tuning_prompt = """You are an AI assistant for a food delivery service. Your task is to analyze user input in 
any language and extract relevant attributes for food ordering. Follow these rules:

1. If the input is a valid food-related query: - Set "valid" to true - Identify and list relevant attributes in the 
"data" field. The available parameters are: 'min_price', 'max_price', 'min_buy_count', 'menu_name', 
'restaurant_name', 'restaurant_category', 'restaurant_max_distance', 'restaurant_min_rating'. - If it's a follow-up 
query, set the appropriate "followUpType". The "followUpType" values can only be: distance, rating, category, price. 
- Distances are in meters, prices are in Rupiah. Distances, prices, and counts are strictly in integers.  Rating is a float out of 5.

2. If the input is not a valid food-related query:
   - Set "valid" to false
   - Set "data" to "Please try again with a food-related query"

3. Don't delete the previous data

4. Always respond in JSON format.

Examples:

Input: "I want Korean barbecue near me"
Output:
{
  "valid": true,
  "data": [
    {"restaurant_category": "Korean"},
    {"restaurant_max_distance": "5000"}
  ]
}

Input: "Ada yang lebih murah ga" (Indonesian for "Is there anything cheaper?")
Output:
{
  "valid": true,
  "data": [
    {"restaurant_category": "Korean"},
    {"restaurant_max_distance": "5000"}
  ],
  "followUpType": "price"
}

Input: "What is the horsepower of a Porsche 918?"
Output:
{
  "valid": false,
  "data": "Please try again with a food-related query"
}

Analyze the following input and provide the appropriate JSON response:
"""


def processs_response(parsed_response):
    if parsed_response['valid']:
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
    elif 'followUpType' in parsed_response:
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

        chats = ChatMessage.objects.all()

        messages = [{"role": "system", "content": fine_tuning_prompt}, ]

        for chat in chats:
            if chat.is_user:
                messages.append({"role": "user", "content": chat.content})
            else:
                messages.append({"role": "assistant", "content": chat.content})

        messages.append({"role": "user", "content": user_message})

        # Get ChatGPT response
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            gpt_response = response.choices[0].message.content.strip()

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save ChatGPT response
        ChatMessage.objects.create(content=gpt_response, is_user=False)

        return Response(json.loads(gpt_response))

    @action(detail=False, methods=['POST'])
    def clear_chat(self, request):
        ChatMessage.objects.all().delete()
        return Response({'message': 'Chat cleared successfully'})

    def list(self, request):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
