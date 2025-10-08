FROM python:3.14.0-alpine

WORKDIR /app
COPY *.py .
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "-u", "main.py"]