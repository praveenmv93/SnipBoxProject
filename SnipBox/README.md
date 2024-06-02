# SnipBox

SnipBox is a short note-saving app that allows users to save and manage short text snippets, group them with tags, and
view, update, and delete them as needed. The app also includes user authentication via JWT.

## Features

- User authentication using JWT.
- Create, read, update, and delete snippets.
- Tag management for grouping snippets.
- Overview API to get total count and list of snippets.
- List snippets by tag.
- Responsive API responses with meaningful messages.

## Technologies Used

- Django
- Django Rest Framework
- Simple JWT for authentication

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django Rest Framework

### Steps

1. Clone the repository:

git clone https://github.com/praveenmv93/snipbox.git

cd SnipBox

2. Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

3. Install the required dependencies:

pip install -r ../requirements.txt # Should check the path 

4. Apply the migrations:

python manage.py migrate

5. Run the development server:

python manage.py runserver



Usage
API Endpoints
Authentication

    Login: /login/ (POST)
    Refresh Token: /refresh/ (POST)

Snippets

    Overview: /api/snippets/overview/ (GET)
    Create: /api/snippets/ (POST)
    List: /api/snippets/ (GET)
    Detail: /api/snippets/<id>/ (GET)
    Update: /api/snippets/<id>/ (PUT/PATCH)
    Delete: /api/snippets/<id>/ (DELETE)

Tags

    List: /api/tags/ (GET)
    Detail: /api/tags/<id>/snippets/ (GET)



## Sample Requests
Authentication

To authenticate, obtain a token by posting to /api/token/ with your username and password:


{
    "username": "yourusername",
    "password": "yourpassword"
}
Use the received token in the Authorization header for subsequent requests:

Authorization: Bearer your_token_here


## Create Snippet

POST /api/snippets/
Content-Type: application/json
Authorization: Bearer your_token_here

{
    "title": " Snippet",
    "note": "This is a snippet.",
    "tags": [
        {"tag_title": "Tag 4"}
    ]
}

## ORs CURL 

curl --location 'http://127.0.0.1:8000/api/snippets/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE3MzU0Mzg0LCJpYXQiOjE3MTczNTQwODQsImp0aSI6ImYzMGI0ZGYyNzM3MzQ3OGViZmEyYjA3ZDAwM2NmOTVjIiwidXNlcl9pZCI6MX0.wObTuBhWw7Dompxhw7RP9zTCRIcSVTs5pJtUtscDai0' \
--data '{
    "title": "Updated Snippet",
    "note": "This is an updated snippet.",
    "tags": [
        {"tag_title": "u Tag 4"}
    ]
}'


