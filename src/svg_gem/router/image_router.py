from fastapi import APIRouter, HTTPException, BackgroundTasks

from svg_gem.feature.image_visualization.img_visual_chain import ImgVisualChain
from svg_gem.feature.svg.svg_manager import SVGManager
from svg_gem.model.Image_model import ImageInputType, GenerateSVGInputType
from utility.websocket.websocket_manager import get_websocket

router = APIRouter(prefix="/api/v1/image", tags=["Image"])

@router.post("/read_image")
async def read_image(image_input: ImageInputType):
    chain = ImgVisualChain(reference_img_url=image_input.image_url)
    return await chain.execute_chain()

@router.post("/generate_svg")
async def generate_svg(image_input: GenerateSVGInputType):
    websocket_manager = get_websocket()
    svg_manager = SVGManager(image_input, websocket_manager)
    return await svg_manager.execute_pipeline()

@router.post("/background_generate_svg")
def background_generate_svg(image_input: GenerateSVGInputType, background_tasks: BackgroundTasks):

    background_tasks.add_task(generate_svg, image_input=image_input)

    return {'session_id': image_input.session_id}