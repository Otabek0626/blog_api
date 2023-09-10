FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY . /app

RUN pip install -r requirements.txt

# RUN alembic upgrade head