# Grad-U-Ace' Hack Jakarta Backend
## GrabFood Chatbot

Powered by the magical Django Rest Framework.

## Project Overview
The GrabFood Chatbot aims to revolutionize the food ordering experience by offering personalized recommendations to users and actionable insights to merchants. Leveraging AI, this chatbot enhances user engagement, reduces bounce rates, and drives economic growth for merchants.

## Key Features
- **Personalized Recommendations:** Tailored food suggestions based on user inputs such as cravings, distances, and price.
- **Advanced Filtering:** Refine searches by cuisine, user's review, and more.
- **Merchant Visibility:** Small merchants featured in recommendations to increase their exposure.

## Testing Guide

Live backend are accessible [here](https://grabin-food-be-kv422ek6cq-et.a.run.app/).

Powered by Google Cloud Run.

API Docs: https://grabin-food-be-kv422ek6cq-et.a.run.app/api/schema/swagger-ui/

## Development Guide
1. Create a `.env` on the project root with the following keys:
   ```shell
   DEBUG=True
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
   
The app is containerized. For production purposes, we can set up a connection to a more persistent database of choice in settings. Mind the credentials.

#### Example: Postgres

1. The following environment variables need to be set (lcoally in a `.env` file):
   ```shell
   DEBUG=False
   OPENAI_API_KEY=
   
   PG_NAME=
   PG_USER=
   PG_PASSWORD=
   PG_HOST=
   PG_PORT=
   ```
2. Build the image
   ```shell
   docker build . -t grabin-food-be
   ```
3. The build image can be run locally, pushed to docker hub, or run anywhere. To run locally, do:
   ```shell
   docker run -d -p 8000:8000 --name grabin-food-be --env-file=.env  grabin-food-be
   ```

## Tech Stack
- **Django:** We chose Django for its rapid development capabilities, scalability for high loads, and extensive community resources. It provides a powerful foundation for efficient development and maintenance.
- **Cloud Run:** For deployment, we chose Cloud Run because of its automatic scaling, serverless architecture, cost-effectiveness, quick containerized app deployment, and seamless GCP integration. It offers a flexible, efficient hosting solution that grows with our needs.
  
## Demo
Watch our [Demo Video](https://) to see the chatbot in action.

## Future Development
- **Ads for Merchants:** Integrate ad placements within recommendations to allow merchants to promote specific dishes or offers.
- **User Trend Analysis and Recommendations:** Develop a reporting feature to provide merchants with insights into popular keywords and trends based on user inputs, along with actionable AI-powered recommendations to help merchants align their offerings with current demand.
- **Mood-Based Recommendations:** Enhance the chatbot to provide suggestions based on user moods, making recommendations more contextually relevant.
- **Jaccard Index-Based Recommendations:** Use the Jaccard Index to analyze the similarity between a user's order history and other users' histories, providing personalized food recommendations.
- **Integration with GrabFamily:** Enhance the chatbot to prompt meal decisions for other family members.
