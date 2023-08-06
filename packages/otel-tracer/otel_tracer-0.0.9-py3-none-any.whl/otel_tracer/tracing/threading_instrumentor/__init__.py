import threading
from typing import Collection

from opentelemetry import context, trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import (get_current_span, get_tracer,
                                 get_tracer_provider)

from .package import _instruments
from .version import __version__


class _InstrumentedThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_span = None

    def start(self):
        self._parent_span = get_current_span()
        super().start()

    def run(self):
        parent_span = self._parent_span or get_current_span()
        ctx = trace.set_span_in_context(parent_span)
        context.attach(ctx)
        super().run()


class _InstrumentedTimer(_InstrumentedThread):
    def __init__(self, interval, function, *args, **kwargs):
        _InstrumentedThread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = threading.Event()

    def cancel(self):
        self.finished.set()

    def run(self):
        parent_span = self._parent_span or get_current_span()
        ctx = trace.set_span_in_context(parent_span)
        context.attach(ctx)
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


class ThreadingInstrumentor(
    BaseInstrumentor
):
    original_threadcls = threading.Thread
    original_timercls = threading.Timer

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, *args, **kwargs):
        tracer_provider = (
            kwargs.get("tracer_provider", None) or get_tracer_provider()
        )

        tracer = get_tracer(__name__, __version__, tracer_provider)
        threading.Thread = _InstrumentedThread
        _InstrumentedThread._tracer = tracer
        threading.Timer = _InstrumentedTimer
        _InstrumentedTimer._tracer = tracer

    def _uninstrument(self, **kwargs):
        threading.Thread = self.original_threadcls
        threading.Timer = self.original_timercls
