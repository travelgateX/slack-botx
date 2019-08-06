import os
import logging

from fastapi import APIRouter

from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.requests import Request
from starlette.responses import Response
from app.common.config import Config

Config.init_config()
logger = logging.getLogger(__name__)
logger.info("prometheus start")

router = APIRouter()

@router.get("/metrics", tags=["prometheus","metrics"])
def metrics(request: Request) -> Response:
    if "prometheus_multiproc_dir" in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
        logger.info(f"Metrics multiprocess :[{os.environ['prometheus_multiproc_dir']}]")
    else:
        registry = REGISTRY
        logger.info(f"Metrics no multiprocess")

    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)