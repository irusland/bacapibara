import psutil as psutil
from prometheus_client import Gauge


class PrometheusManager:
    def __init__(self):
        self._system_usage = Gauge(
            "system_resources_usage",
            "Hold current system resource usage",
            ["resource_type"],
        )

    async def write_system_usage(self):
        self._system_usage.labels("CPU").set(psutil.cpu_percent())
        self._system_usage.labels("Memory").set(psutil.virtual_memory()[2])
