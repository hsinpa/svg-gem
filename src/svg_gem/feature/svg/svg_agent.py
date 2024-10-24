from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import END
from langgraph.graph import StateGraph

from svg_gem.feature.agent_interface import GraphAgent
from svg_gem.feature.svg.svg_prompt import USER_INPUT_GRAMMAR_SYSTEM_PROMPT, SVG_RENDER_SYSTEM_PROMPT, \
    SVG_RENDER_HUMAN_PROMPT, USER_INPUT_GRAMMAR_HUMAN_PROMPT
from svg_gem.feature.svg.svg_type import SVGGraphState
from svg_gem.model.Image_model import GenerateSVGInputType
from utility.langchain_helper.simple_factory_type import SocketEvent
from utility.langchain_helper.simple_prompt_factory import SimplePromptFactory
from utility.langchain_helper.simple_prompt_streamer import SimplePromptStreamer
from utility.llm_model import get_together_model, LLAMA_3_1_8B, get_antropic_model, LLAMA_3_2_3B
from utility.utility_func import parse_xml
from utility.websocket.websocket_manager import WebSocketManager


class SVGAgent(GraphAgent):

    def __init__(self, user_input: GenerateSVGInputType, websocket_manager: WebSocketManager):
        self._user_input = user_input
        self._websocket_manager = websocket_manager

    async def _fine_tune_user_input_chain(self, state: SVGGraphState):
        prompt_factory = SimplePromptFactory(llm_model=get_together_model(model_name=LLAMA_3_1_8B))

        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=USER_INPUT_GRAMMAR_SYSTEM_PROMPT,
            human_prompt_text=USER_INPUT_GRAMMAR_HUMAN_PROMPT,
            partial_variables={'user_input': state['raw_user_input']}
        ).with_config({"run_name": 'Rewrite user input'})

        r = await chain.ainvoke({})

        return {'fine_user_description': r}


    async def _output_svg_chain(self, state: SVGGraphState):
        prompt_factory = SimplePromptFactory(
            # llm_model=get_antropic_model()
            llm_model=get_together_model(model_name=LLAMA_3_2_3B)
        )

        chain = prompt_factory.create_chain(
            output_parser=StrOutputParser(),
            system_prompt_text=SVG_RENDER_SYSTEM_PROMPT,
            human_prompt_text=SVG_RENDER_HUMAN_PROMPT,
            partial_variables={'description': state['fine_user_description']}
        ).with_config({"run_name": 'output svg chain'})

        simple_streamer = SimplePromptStreamer(websocket_manager=self._websocket_manager, session_id=self._user_input.session_id,
                                               socket_id=self._user_input.socket_id, event_tag=SocketEvent.bot)

        result = await simple_streamer.execute(chain=chain)

        result = result.replace('\\n', '')
        result = result.replace('\\', '')
        result = parse_xml('svg', result)

        return {'svg_block': result}

    def create_graph(self):
        g_workflow = StateGraph(SVGGraphState)

        g_workflow.add_node('find_tune_user_input_chain', self._fine_tune_user_input_chain)
        g_workflow.add_node('output_svg_chain', self._output_svg_chain)

        g_workflow.set_entry_point('find_tune_user_input_chain')
        g_workflow.add_edge('find_tune_user_input_chain', 'output_svg_chain')
        g_workflow.add_edge('output_svg_chain', END)

        return g_workflow.compile()
