import logging
import os
from app.config.settings import Settings


def configure_logging(settings: Settings):
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
