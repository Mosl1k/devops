FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY data/ ./data/

ENV PYTHONPATH=/app
ENV QUESTIONS_PATH=/app/data/questions.json

EXPOSE 2113

CMD ["python", "-m", "app.main"]
