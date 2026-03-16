FROM python:3.11-slim

WORKDIR /app

COPY client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY client/ ./client/

ENV PYTHONPATH=/app
ENV CONSUL_HOST=consul

CMD ["sh", "-c", "sleep 5 && python -m client.client"]
