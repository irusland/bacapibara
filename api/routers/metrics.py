from fastapi import APIRouter
from fastapi import Response, Request
from starlette_exporter import handle_metrics

from api.prometheus.manager import PrometheusManager


class MetricsRouter(APIRouter):
    def __init__(self, prometheus_manager: PrometheusManager):
        super().__init__(tags=['metrics'])

        @self.get("/metrics")
        async def metrics(request: Request) -> Response:
            await prometheus_manager.write_system_usage()
            return handle_metrics(request=request)
