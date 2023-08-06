from flask import request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .threading_instrumentor import ThreadingInstrumentor
from .queue_instrumentor import QueueInstrumentor


def init_flask(app, servicename, endpoint):
    FlaskInstrumentor().instrument_app(app)

    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({"service.name": servicename})
        )
    )

    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint  # Use the address and port of your OpenTelemetry Collector
    )
    span_processor = BatchSpanProcessor(otlp_exporter)

    trace.get_tracer_provider().add_span_processor(span_processor)

    @app.before_request
    def start_span():
        span_name = request.path or "root"
        request.span = trace.get_tracer(__name__).start_span(span_name)

    @app.after_request
    def end_span(response):
        request.span.end()
        return response
    return app


def init_requests():
    RequestsInstrumentor().instrument()


def init_redis():
    RedisInstrumentor().instrument()


def init_pika():
    PikaInstrumentor().instrument()

def init_threading():
    ThreadingInstrumentor().instrument()

def init_queue():
    QueueInstrumentor().instrument()