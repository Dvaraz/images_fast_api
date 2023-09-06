from pydantic import BaseModel


class Image(BaseModel):
    name: str
    base64_image: str


class GetImages(BaseModel):
    id: int
    image_name: str
    image_size: str
    last_edit_at: str

    class Config:
        from_attributes = True
