from pydantic import BaseModel
from typing import Optional

class VolunteerSummaryOut(BaseModel):
    user_id: int
    full_name: str
    image: Optional[str]
    total_points: int

    class Config:
        orm_mode = True
