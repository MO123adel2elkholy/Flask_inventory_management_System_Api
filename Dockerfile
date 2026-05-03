FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# system deps (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt

# copy project
COPY . /app

# expose port
EXPOSE 5000

# use gunicorn with eventlet worker (Socket.IO friendly)
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "Ecommerce.app:app", "-b", "0.0.0.0:5000"]