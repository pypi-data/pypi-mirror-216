import inspect
import uuid
import json
from functools import wraps
from typing import Optional
from nats.aio.msg import Msg
from panini.app import get_app
from opentelemetry import trace
from dataclasses import dataclass
from panini.middleware import Middleware
from panini.managers.event_manager import Listen
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


@dataclass
class SpanConfig:
    span_name: str
    span_attributes: Optional[dict]


def register_trace(**decorator_kwargs):  # the decorator
    def wrapper(f):  # a wrapper for the function
        if inspect.iscoroutinefunction(f):
            @wraps(f)
            async def decorated_function(*args, **kwargs):  # the decorated function
                ctx = trace.get_current_span().get_span_context()
                link = trace.Link(ctx)
                _tracer = trace.get_tracer(__name__)
                with _tracer.start_as_current_span(decorator_kwargs.get("span_name", f"unknown-{uuid.uuid4().hex}"),
                                                  links=[link]):
                    result = await f(*args, **kwargs)
                return result
        else:
            @wraps(f)
            def decorated_function(*args, **kwargs):  # the decorated function
                ctx = trace.get_current_span().get_span_context()
                link = trace.Link(ctx)
                _tracer = trace.get_tracer(__name__)
                with _tracer.start_as_current_span(decorator_kwargs.get("span_name", f"unknown-{uuid.uuid4().hex}"),
                                                  links=[link]):
                    result = f(*args, **kwargs)
                return result

        return decorated_function

    return wrapper


class OTELTracer:
    def __init__(self, tracing_config: dict, **kwargs):
        self._config = tracing_config
        self.service_name = self._config["service_name"]
        self._exporter_config = self._config["exporter_config"]
        self._provider_config = self._config["provider_config"]
        self._custom_config = self._config["custom_config"]
        self._custom_config.update(**kwargs)
        self.tracer = self.create_tracer()

    def create_tracer(self):
        resource = Resource(attributes={
            SERVICE_NAME: self.service_name
        })
        provider = TracerProvider(resource=resource, **self._provider_config)
        processor = BatchSpanProcessor(OTLPSpanExporter(**self._exporter_config))
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        return trace.get_tracer(__name__)


class TracingMiddleware(Middleware):
    def __init__(
            self,
            tracing_config: dict,
            **kwargs
    ):
        self._otel_tracer = OTELTracer(tracing_config=tracing_config, **kwargs)
        self.tracer: Tracer = self._otel_tracer.tracer
        self.parent = TraceContextTextMapPropagator()
        super().__init__()

    def _create_uuid(self) -> str:
        return uuid.uuid4().hex

    async def send_any(self, subject: str, message: Msg, send_func, *args, **kwargs):
        carrier = {}
        headers = {}
        span_config = kwargs.get("span_config")
        use_tracing = kwargs.get("use_tracing", True)
        if kwargs.get("use_current_span", False):
            ctx = trace.get_current_span().get_span_context()
            link = [trace.Link(ctx)]
        else:
            link = []
        if not isinstance(span_config, SpanConfig):
            span_config = SpanConfig(
                span_name=self._create_uuid(),
                span_attributes={})
        if use_tracing is True and span_config:
            with self.tracer.start_as_current_span(span_config.span_name, links=link) as span:
                for attr_key, attr_value in span_config.span_attributes.items():
                    span.set_attribute(attr_key, attr_value)
                self.parent.inject(carrier=carrier)
                headers = {
                    "tracing_span_name": span_config.span_name,
                    "tracing_span_carrier": json.dumps(carrier)
                }
        if "use_tracing" in kwargs:
            del kwargs['use_tracing']
        response = await send_func(subject, message, headers=headers)
        return response

    async def listen_any(self, msg: Msg, callback):
        context = {}
        app = get_app()
        assert app is not None
        listen_obj_list = app._event_manager.subscriptions[msg.subject]
        for index in range(0, len(listen_obj_list)):
            listen_object: Listen = listen_obj_list[index]
            use_tracing = listen_object._meta.get("use_tracing", True)
            if use_tracing:
                if id(callback) == id(listen_object.callback) and callback.__name__ == listen_object.callback.__name__:
                    headers = msg.headers
                    if headers:
                        context = self.parent.extract(carrier=json.loads(msg.headers.get("tracing_span_carrier", "{}")))
                    span_config = listen_object._meta.get("span_config")
                    if not isinstance(span_config, SpanConfig):
                        span_config = SpanConfig(
                            span_name=self._create_uuid(),
                            span_attributes={})
                    with self.tracer.start_as_current_span(span_config.span_name, context=context) as span:
                        for attr_key, attr_val in span_config.span_attributes.items():
                            span.set_attribute(attr_key, attr_val)
                        response = await callback(msg)
                        return response
        return await callback(msg)
