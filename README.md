# Grad-U-Ace' Hack Jakarta Backend
## GrabFood Chatbot

Powered by the magical Django Rest Framework.

## Project Overview
The GrabFood Chatbot aims to revolutionize the food ordering experience by offering personalized recommendations to users and actionable insights to merchants. Leveraging AI, this chatbot enhances user engagement, reduces bounce rates, and drives economic growth for merchants.

## Key Features
- **Personalized Recommendations:** Tailored food suggestions based on user inputs such as cravings, distances, and price.
- **Advanced Filtering:** Refine searches by cuisine, user's review, and more.
- **Merchant Visibility:** Small merchants featured in recommendations to increase their exposure.

## Development Guide
1. Create a `.env` on the project root with the following keys:
   ```shell
   OPENAI_API_KEY=
   ```
2. Migrate the database
    ```shell
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
2. Populate restaurants and menu table:
    ```shell
    python3 manage.py populate_data 
    ```
3. Run the server
    ```shell
    python3 manage.py runserver
    ```

## Demo
Watch our [Demo Video](https://) to see the chatbot in action.

## Future Development
- **Ads for Merchants:** Integrate ad placements within recommendations to allow merchants to promote specific dishes or offers.
- **User Trend Analysis and Recommendations:** Develop a reporting feature to provide merchants with insights into popular keywords and trends based on user inputs, along with actionable AI-powered recommendations to help merchants align their offerings with current demand.
- **Mood-Based Recommendations:** Enhance the chatbot to provide suggestions based on user moods, making recommendations more contextually relevant.
