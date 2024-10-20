from typing_extensions import TypedDict


class SVGGraphState(TypedDict):
    raw_user_input: str
    fine_user_description: str
    svg_block: str