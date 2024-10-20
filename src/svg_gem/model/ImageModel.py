from pydantic import BaseModel


class ImageInputType(BaseModel):
    image_url: str


class GenerateSVGInputType(BaseModel):
    user_input: str