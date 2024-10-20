from fastapi import APIRouter

from svg_gem.feature.image_visualization.img_visual_chain import ImgVisualChain
from svg_gem.feature.svg.svg_manager import SVGManager
from svg_gem.model.ImageModel import ImageInputType, GenerateSVGInputType
from utility.websocket.websocket_manager import get_websocket

router = APIRouter(prefix="/api/v1/image", tags=["Image"])

@router.post("/read_image")
async def read_image(image_input: ImageInputType):
    chain = ImgVisualChain(reference_img_url=image_input.image_url)
    return await chain.execute_chain()

@router.post("/generate_image")
async def read_image(image_input: GenerateSVGInputType):
    websocket_manager = get_websocket()
    svg_manager = SVGManager(image_input, websocket_manager)
    return await svg_manager.execute_pipeline()