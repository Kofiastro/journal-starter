import logging

from dotenv import load_dotenv
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

from api.routers.journal_router import router as journal_router

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
logging.info("Starting Journal API...")

# Create app
app = FastAPI(
    title="Journal API",
    description="A simple journal API for tracking daily work, struggles, and intentions",
)

# 🔥 Instrument FastAPI (auto metrics)
FastAPIInstrumentor.instrument_app(app)

# Expose Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app)

# Existing router
app.include_router(journal_router)
