from pydantic import BaseModel

from svg_gem.model.general_model import StreamingInputType


class ImageInputType(BaseModel):
    image_url: str


class GenerateSVGInputType(StreamingInputType):
    user_input: str