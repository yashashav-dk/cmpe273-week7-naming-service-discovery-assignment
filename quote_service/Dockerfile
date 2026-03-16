FROM python:3.11-slim

WORKDIR /app

COPY quote_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quote_service/ ./quote_service/

ENV PYTHONPATH=/app
ENV INSTANCE_NAME=quote-svc
ENV SERVICE_PORT=5001
ENV CONSUL_HOST=consul

CMD ["python", "-m", "quote_service.run"]
