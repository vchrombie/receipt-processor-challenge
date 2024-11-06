FROM python:3.9-slim

WORKDIR /app

COPY src .

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]
