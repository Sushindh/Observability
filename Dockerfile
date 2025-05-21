FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-exporter-otlp-proto-http

CMD ["python", "app.py"]
