# social-network
This is a Django Rest Framework (DRF) based API for a social networking application with various functionalities including user login/signup, searching users, managing friend requests, and listing friends.

# Installation
Follow these steps to set up the project locally:

# Prerequisites
Python 3.6+

Docker (optional for containerization)

# Set Up Environment
python3 -m venv env

source env/bin/activate  # for Linux/Mac

env\Scripts\activate  # for Windows

# clone the repository

git clone https://github.com/afalmuhammad/social-network.git

cd social-network



# Install Dependencies

pip install -r requirements.txt

# Environment Variables

Create a .env file in the project root directory and add the following environment variables:

SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=your_database_url

# Database Setup
Update the database settings in settings.py according to your database configuration. You can use PostgreSQL, MySQL, or any other database supported by Django.

# Run Migrations

python manage.py migrate

# Start the Server

python manage.py runserver

# Docker Setup (Optional)
If you prefer Docker, you can containerize the application. Make sure Docker is installed on your system.

# Build Docker Image
docker-compose build


# Start Docker Container
docker-compose up

Make sure you are setting all the required environment variables specified in the docker-compose file

Note: we used postgresql here.

# API endpoints
- **User Login: /api/login/**
- **User Signup: /api/signup/**
- **Search Users: /api/search/**
- **Send Friend Request: /api/friend-request//**
- **Accept Friend Request: /api/friend-request/{id}/accept/**
- **Reject Friend Request: /api/friend-request/{id}/reject/**
- **List Friends: /api/friends/**
- **List Pending Friend Requests: /api/pending-requests/**

# Postman Collection

You can find the postman collection [here](https://api.postman.com/collections/28304391-ea7f4760-36c5-4749-88c8-f7726afff6ff?access_key=PMAT-01HZZ0C2BZXZDMCM74N4BTZFQJ)