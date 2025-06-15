from pydantic import BaseModel

class UniversityOut(BaseModel):
    id: int
    name: str
    address: str | None = None
    phone: str | None = None
    email: str | None = None

