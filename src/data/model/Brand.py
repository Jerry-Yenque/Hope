class Brand:
    def __init__(self, id, name, created_at, updated_at, deleted_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return f"Brand(id={self.id}, name={self.name}, created_at={self.created_at}, updated_at={self.updated_at}, deleted_at={self.deleted_at})"