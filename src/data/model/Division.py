from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.data.model.Area import Area

@dataclass
class Division:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    area_id: int
    area: Area
    deleted_at: Optional[datetime] = None