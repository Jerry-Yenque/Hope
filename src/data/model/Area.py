from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Area:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None