from svg_gem.feature.svg.svg_agent import SVGAgent
from langfuse.callback import CallbackHandler

from svg_gem.model.ImageModel import GenerateSVGInputType
from utility.websocket.websocket_manager import WebSocketManager


class SVGManager:
    def __init__(self, user_input: GenerateSVGInputType, websocket_manager: WebSocketManager):
        self._user_input = user_input
        self._websocket_manager = websocket_manager

    async def execute_pipeline(self):
        agent = SVGAgent(self._websocket_manager)
        compile_graph = agent.create_graph()

        r = await compile_graph.ainvoke({'raw_user_input': self._user_input.user_input},
                                    config={"run_name": 'SVG Graph', "callbacks": [CallbackHandler(user_id='hsinpa')]})

        return r