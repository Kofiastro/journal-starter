import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from prometheus_client import make_asgi_app

from api.routers.journal_router import router as journal_router

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
logging.info("Starting Journal API...")

# 🔥 Setup Prometheus metrics
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])

# Create app
app = FastAPI(
    title="Journal API",
    description="A simple journal API for tracking daily work, struggles, and intentions",
)

# 🔥 Instrument FastAPI (auto metrics)
FastAPIInstrumentor.instrument_app(app)

# 🔥 Add /metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Existing router
app.include_router(journal_router)
