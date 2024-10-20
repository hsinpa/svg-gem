import re
from itertools import islice


def clamp(value: int, min_value: int, max_value: int):
    return max(min_value, min(value, max_value))

def chunk(lst: list, n: int):
    it = iter(lst)
    return iter(lambda: tuple(islice(it, n)), ())

def parse_block(code: str, raw_message: str) -> str:
    try:
        regex_sympy = r'```{code}(?:.|\n)*?```'
        regex_sympy = regex_sympy.replace('{code}', code)

        sympy_codes: list[str] = re.findall(regex_sympy, raw_message)

        raw_llm_msg: str = raw_message

        if len(sympy_codes) > 0:
            raw_llm_msg: str = sympy_codes[0]

        raw_llm_msg = raw_llm_msg.replace(f'```{code}', '')
        raw_llm_msg = raw_llm_msg.replace('```', '')

        return raw_llm_msg
    except Exception as e:
        print(e)

    return raw_message

def parse_xml(code: str, raw_message: str) -> str:
    try:
        regex_sympy = r'<{code}(?:.|\n)*?<\/{code}>'
        regex_sympy = regex_sympy.replace('{code}', code)

        sympy_codes: list[str] = re.findall(regex_sympy, raw_message)

        raw_llm_msg: str = raw_message

        if len(sympy_codes) > 0:
            raw_llm_msg: str = sympy_codes[0]

        raw_llm_msg = raw_llm_msg.replace(f'```{code}', '')
        raw_llm_msg = raw_llm_msg.replace('```', '')

        return raw_llm_msg
    except Exception as e:
        print(e)

    return raw_message