IMAGE_TO_TEXT_SYSTEM_PROMPT = """\
Give me concise description best describe the image.
It is for education purpose, so reason about the logic behind.
If number or color is mention, it should be accurate, and do not use vague word such as some etc...
If text is mention, list out it's content and rough position

The description will be used as prompt for image generation, 
the shape of object need to transform into simple primitive shape, only capture the overall look, detail can be omit.\
"""
