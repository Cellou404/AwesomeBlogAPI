# Here'se an Awesome Blog API

## Summary

This is a simple blog api that allows users to create , read, update and delete posts. It uses `Django` & `DjangoRestFramework` as the server framework with Postgres for database management.

## Screenshots

![Screenshot](./docs/img/API_Screenshot_from_thunder_client.png)

## How to use ?

### Clone the repo

```bash
git clone https://github.com/Cellou404/AwesomeBlogAPI.git
```

### Create a virtual environment

```bash
python3 -m venv venv
```

### Activate the virtual environment

```bash
source venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Create a .env file

```bash
touch .env
```

Fill the .env file with the following values:

```python
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```

### Migrate the database

```bash
python manage.py makemigrations # you can specify the app name. e.g. python manage.py makemigrations blog
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run the server

```bash
python manage.py runserver
```

### Access the server

#### For example: Posts

```bash
http://127.0.0.1:8000/api/v1/blog/posts/
```

## Endpoints

### For example: Posts Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /api/v1/blog/posts/ | Get all posts |
| GET | /api/v1/blog/posts/{id}/ | Get a post by id |
| POST | /api/v1/blog/posts/ | Create a post |
| PUT | /api/v1/blog/posts/{id}/ | Update a post by id |
| DELETE | /api/v1/blog/posts/{id}/ | Delete a post by id |

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
