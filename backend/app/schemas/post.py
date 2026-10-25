from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field

class PostCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    content: str = Field(min_length=1, max_length=280)
    image_url: str | None = None

class PostOut(BaseModel):
    id: int
    anon_id: str
    content: str
    image_url: str | None
    created_at: datetime
