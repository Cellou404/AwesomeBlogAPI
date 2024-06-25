# Awesome Blog API

This is a simple blog API built using `Django` and `DjangoRestFramework` with PostgreSQL as the database management system. It allows users to create, read, update, and delete (CRUD) posts.

## Features

- User registration and login
- Create, read, update, and delete posts
- View all posts, individual posts, and create comments
- Sort and filter data using query parameters

## Requirements

The following tools and libraries are required to run the project.

- Python 3.6 and above
- PostgreSQL
- Django 3.2
- DjangoRESTFramework 3.13
- psycopg2-binary

## Quickstart

1. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run migrations:

    ```python
    python manage.py migrate
    ```

3. Create a superuser:

    ```python
    python manage.py createsuperuser
    ```

4. Start the server:

    ```python
    python manage.py runserver
    ```

5. Access the website using a browser or a REST client at `http://localhost:8000/api/V1/`.

## API Reference

- **Users**

**Create a new user:**

`POST` `/auth/users/`
`Authorization`: `None`
`Content-Type`: `application/json`

**List all users:**

`GET` `auth/users/`
`Authorization`: `Token` `<your_token>`

**Retrieve a user:**

`GET` `/users/<int:pk>/`
`Authorization`: `Token` `<your_token>`

**Update a user:**

`PUT` `/users/<int:pk>/`
`Authorization`: `Token` `<your_token>`
`Content-Type`: `application/json`
`Body`: `{ "username": "string", "email": "string", "bio": "string", "image": "string" }`

**Delete a user:**

`DELETE` `/users/<int:pk>/`
`Authorization`: `Token` `<your_token>`

- **Posts**

**Create a new post:**

`POST` `/posts/`
`Authorization`: `Token` `<your_token>`
`Content-Type`: `application/json`
`Body`: `{ "title": "string", "content": "string", "image": "string" }`

**List all posts:**

`GET` `/posts/`
`Authorization`: `Token` `<your_token>`
`Query Parameters`:
`search`, `ordering`, `limit`, `offset`

**Retrieve a post:**

`GET` `/posts/<slug:slug>/`
`Authorization`: `Token` `<your_token>`

**Update a post:**

`PUT` `/posts/<slug:slug>/`
`Authorization`: `Token` `<your_token>`
`Content-Type`: `application/json`
`Body`: `{ "title": "string", "content": "string", "image": "string" }`

**Delete a post:**

`DELETE` `/posts/<slug:slug>/`
`Authorization`: `Token` `<your_token>`

- **Comments**

**Create a new comment:**

`POST` `/posts/<slug:post_slug>/comments/`
`Authorization`: `Token` `<your_token>`
`Content-type`: `application/json`
`Body`: `{ "content": "string" }`

**List all comments:**

`GET` `/posts/<slug:post_slug>/comments/`
