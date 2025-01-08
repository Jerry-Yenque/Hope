from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.data.model.Category import Category

@dataclass
class Feature:
    id: int
    name: str = None
    created_at: datetime = None
    updated_at: datetime = None
    category_id: int = None
    pos: int = None
    category: Category = None
    deleted_at: Optional[datetime] = None

    def __hash__(self):
        return hash((self.id, self.name, self.created_at, self.updated_at, 
                     self.category_id, self.pos, self.category, self.deleted_at))
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
