# pull official base image
FROM python:3.11-slim

# set work directory
WORKDIR /app
COPY ./requirements.txt /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt    
RUN pip install -U channels["daphne"]

# copy project
COPY . /app/

# Expose port and specify the command to run
EXPOSE 5000
CMD ["daphne", "-b", "0.0.0.0", "-p", "5000", "project_chat.asgi:application"]
