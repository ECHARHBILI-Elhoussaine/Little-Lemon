# Little Lemon Backend 
Simple Project from Meta Back-End Developer Professional Certificate

## Installation
Python Version 
```sh
Python 3.12.1
```
Install pip
```sh
python get-pip.py
```
Install Django
```sh
pip install django
```
Install other dependency
```sh
pip install psycopg2 Pillow djangorestframework djangorestframework_simplejwt python-dotenv drf-yasg
```

## Running project 
Migrations
```sh
python manage.py makemigrations
python manage.py migrate   
```
Running Server 
```sh
python manage.py runserver    
```
Testing
```sh
 python manage.py test    
```

## Api Endpoints
1. Booking:
   - List all bookings and create new bookings:
     GET /api/bookings/
     POST /api/bookings/

   - Retrieve, update, and delete a specific booking:
     GET /api/bookings/<booking_id>/
     PUT /api/bookings/<booking_id>/
     DELETE /api/bookings/<booking_id>/
2. Registration:
   - Register a new user:
     POST /api/registration/

read Readme.txt for more endpoints.
