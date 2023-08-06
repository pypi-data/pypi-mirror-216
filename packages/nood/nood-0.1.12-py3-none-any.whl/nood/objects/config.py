from pydantic import BaseModel


class MonitorConfig(BaseModel):
    monitor_id: int
