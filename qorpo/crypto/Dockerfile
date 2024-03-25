FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Default values for build arguments
ARG DATABASE_HOST=postgres
ARG DATABASE_PORT=5432
ARG DATABASE_NAME=crypto
ARG DATABASE_USER=crypto
ARG DATABASE_PASSWORD=crypto

# Set environment variables based on build arguments
ENV DATABASE_HOST=$DATABASE_HOST
ENV DATABASE_PORT=$DATABASE_PORT
ENV DATABASE_NAME=$DATABASE_NAME
ENV DATABASE_USER=$DATABASE_USER
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD

CMD ["gunicorn", "-w", "4", "-k", "aiohttp.GunicornWebWorker", "-b", "0.0.0.0:8000", "api:main_app_factory"]
