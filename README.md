# Grad-U-Ace' Hackjakarta Backend

Powered by the magical Django Rest Framework.

## Background

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



