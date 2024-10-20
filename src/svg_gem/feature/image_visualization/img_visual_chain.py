from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from svg_gem.feature.image_visualization.img_visual_prompt import IMAGE_TO_TEXT_SYSTEM_PROMPT
from utility.langchain_helper.simple_prompt_factory import SimplePromptFactory
from utility.llm_model import get_together_model, LLAMA_3_2_11B


class ImgVisualChain:
    def __init__(self, reference_img_url: str):
        self._reference_img_url = reference_img_url

    def _get_chain(self):
        past_messages = [
            SystemMessage(IMAGE_TO_TEXT_SYSTEM_PROMPT),
            HumanMessage(content=[{'type': 'image_url', 'image_url': {"url": self._reference_img_url}, }])]

        prompt_template = ChatPromptTemplate.from_messages(past_messages)

        chain = (prompt_template | get_together_model(LLAMA_3_2_11B) | StrOutputParser()).with_config({"run_name": 'Image visual'})

        return chain

    async def execute_chain(self):
        return await self._get_chain().ainvoke({})