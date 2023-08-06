import queue
from typing import Collection
from opentelemetry import context, trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_current_span, get_tracer, get_tracer_provider

from .package import _instruments
from .version import __version__

class EventWithSpan:
    def __init__(self, event, span: trace.Span):
        self.event = event
        self.span = span
        
class _InstrumentedQueue(queue.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracer = trace.get_tracer(__name__, __version__, get_tracer_provider())

    def put(self, item, block=True, timeout=None, *args, **kwargs):
        current_span = get_current_span()
        ctx = trace.set_span_in_context(current_span)
        with self.tracer.start_as_current_span("queue_put_event", context=ctx):
            event_span = trace.get_current_span()
            super().put(EventWithSpan(item, event_span), block=block, timeout=timeout)

    def get(self, block=True, timeout=None, *args, **kwargs):
        event_with_span = super().get(block=block, timeout=timeout)
        parent_span = event_with_span.span
        ctx = trace.set_span_in_context(parent_span)
        with self.tracer.start_as_current_span("queue_get_event", context=ctx):
            return event_with_span.event


class QueueInstrumentor(BaseInstrumentor):
    original_queuecls = queue.Queue

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, *args, **kwargs):
        tracer_provider = (
            kwargs.get("tracer_provider", None) or get_tracer_provider()
        )

        tracer = get_tracer(__name__, __version__, tracer_provider)
        queue.Queue = _InstrumentedQueue
        _InstrumentedQueue._tracer = tracer

    def _uninstrument(self, **kwargs):
        queue.Queue = self.original_queuecls
