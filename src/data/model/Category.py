from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from src.data.model.Division import Division  

@dataclass
class Category:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    division_id: int
    division: Division
    deleted_at: Optional[datetime] = None