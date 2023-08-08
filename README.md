# Watchlist App

The **Watchlist App** is a Django-based web application that allows users to create, manage, and review movies and TV shows. It provides API endpoints for user registration, authentication, managing watchlists, posting reviews, and more.

## Features

- User registration and authentication using JWT (JSON Web Tokens).
- Create and manage watchlists of movies and TV shows from various streaming platforms.
- Post reviews and ratings for individual items on the watchlist.
- API endpoints for bulk creation of watchlist items, reviews, and users.
- Throttling to limit the rate of API requests.
- User and admin permissions for various actions.

## Setup

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/your-username/watchlist-app.git
   cd watchlist-app
   ```
2. Install the required dependencies:
   ```shell
   pip install -r requirements.txt
   ```
3. Set up the database:
   Edit `settings.py` to configure your database settings. By default, the project is set up to use a PostgreSQL database.
   
4. Apply migrations:
   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser for admin access:
   ```shell
    python manage.py createsuperuser
   ```
6. Run the development server:
   ```shell
    python manage.py runserver
   ```
7. Access the application:
   Open your web browser and navigate to http://localhost:8000 to access the API and interact with the endpoints.


## API Endpoints
- User Registration: /user/register/ (POST)
- User Login: /user/login/ (POST)
- User Logout: /user/logout/ (POST)
- List Watchlists: /watchlist/ (GET, POST)
- Watchlist Detail: /watchlist/<int:pk>/ (GET, PUT, DELETE)
- List Watchlist Items: /watchlist/<int:pk>/items/ (GET, POST)
- Watchlist Item Detail: /watchlist/<int:pk>/items/<int:item_pk>/ (GET, PUT, DELETE)
- List Reviews: /reviews/ (GET, POST)
- Review Detail: /reviews/<int:pk>/ (GET, PUT, DELETE)
- Bulk Create: /bulkcreate/ (POST)
