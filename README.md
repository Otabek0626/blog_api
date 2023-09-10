# blog_api
## FastAPI Starter Project

```
├── app
│   ├── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   └── v1
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── comment.py
│   │   │       ├── post.py
│   │   │       ├── swagger.py
│   │   │       └── user.py
│   │   ├── config.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── oauth2.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── jwt_auth
│   │   ├── __init__.py
│   │   ├── auth_config.py
│   │   ├── auth_jwt.py
│   │   ├── config.py
│   │   └── exceptions.py
│   └── main.py
|── static
|   └── file
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 1c692dced13a_initial.py
│       ├── 5c130782fc48_users.py
│       └── e3d5ac52e612_posts_photos_and_comments_table_has_.py
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── alembic.ini
├── prestart.sh
├── requirements.txt
└── docker-compose.yml
```

# Setting up the project without Docker

1. Clone the repository from GitHub.
    ```
    git clone https://github.com/Otabek0626/blog_api.git
    ```

2. Enter the cloned project folder.
    ```
    cd FastAPI_Starter
    ```

3. Create a virtual environment using Python's `venv` module:

    ```
    python -m venv .venv
    ```
    or
    ```
    python3 -m venv .venv
    ```

4. Activate the virtual environment:

    - For Windows:

        ```
        .\.venv\Scripts\activate.ps1
        ```

    - For Linux or macOS:

        ```
        source .venv/bin/activate
        ```

5. Install the required dependencies using `pip`:

    ```
    pip install -r requirements.txt
    ```

5. Create a database using pgadmin. ex: `fastapi`

6. Update `.env` file with your own values.




7. Set up the database using alembic by running the following command:
    - makemigrations
        ```
        alembic revision --autogenerate -m "initial"
        ```
    - migrate
        ```
        alembic upgrade head
        ```

8. Start the server:

    ```
    uvicorn app.main:app --reload
    ```

8. Navigate to http://localhost:8000/docs to see the Swagger UI and interact with the API. 
    `Note`: the Swagger credentials are in `.env` file


# Setting up the project with Docker

1. Clone the repository from GitHub.
    ```
    git clone https://github.com/Otabek0626/blog_api.git
    ```

2. Enter the cloned project folder.
    ```
    cd blog_api
    ```

3. Build the docker compose:
    ```
    docker-compose up --build -d
    ```

5. Navigate to http://localhost:8000/api/v1/swagger to see the Swagger UI and interact with the API. 
    `Note`: the Swagger credentials are in `.env` file
