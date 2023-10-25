FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


CMD ["python3", "proj/manage.py", "runserver", "0.0.0.0:8000"]