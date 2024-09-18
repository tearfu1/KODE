from pydantic import BaseModel, Field, ConfigDict


class SNote(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str = Field(..., min_length=1, description="Название")
    content: str = Field(..., min_length=1, description="Содержание")


class SNoteAdd(BaseModel):
    title: str = Field(..., min_length=1, description="Название")
    content: str = Field(..., min_length=1, description="Содержание")


class SNoteUpdate(BaseModel):
    title: str = Field(..., min_length=1, description="Название")
    content: str = Field(..., min_length=1, description="Содержание")
