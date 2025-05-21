from flask import Flask, request, jsonify
from opentelemetry.sdk.metrics import MeterProvider, Meter
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.semconv.resource import ResourceAttributes


#Name
resource = Resource.create({ResourceAttributes.SERVICE_NAME:"flask-otel-app"})

#Initialize Opentelemetry SDK

#Metrics

# resource = Resource(attributes={SERVICE_NAME: "flask-app"})
exporter = OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

#Metrics instruments
compute_request_count = meter.create_counter(
    name='app_compute_request_count',
    description='Counts the requests to compute-service',
    unit='1'
)

app = Flask(__name__)

@app.route('/home')
def home():
    compute_request_count.add(1, {"endpoint": "/home"})
    return "Home"

@app.route('/cart')
def cart():
    compute_request_count.add(1, {"endpoint": "/cart"})
    return "Cart"

@app.route('/payment')
def payment():
    compute_request_count.add(1, {"endpoint": "/payment"})
    return "Payment"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)