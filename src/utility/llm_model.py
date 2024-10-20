import asyncio
from enum import Enum
from typing import Dict, Any
from google.cloud.aiplatform_v1beta1 import HarmCategory, SafetySetting
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI
from openai import OpenAI

TEXT_EMBEDDING_SIZE = 256
OpenAI_Model_4o = 'gpt-4o'
OpenAI_Model_3_5 = 'gpt-3.5-turbo'
OpenAI_Model_4o_mini = 'gpt-4o-mini'
Gemini_Model_1_5 = 'gemini-1.5-flash-002'
LLAMA_3_2_11B = 'meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo'
LLAMA_3_1_8B = 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo'
CLAUDE_3_5 = 'claude-3-5-sonnet-20240620'

def get_gpt_model(model_name: str = OpenAI_Model_4o_mini, temperature: float = 0.75,
                  json_mode: bool = False, **kwargs):
    arguments = {'model': model_name, 'temperature': temperature, **kwargs}

    if json_mode is True:
        arguments['response_format'] = {"type": "json_object"}

    return ChatOpenAI(
        **arguments
    )


def get_gemini_model(model_name: str = Gemini_Model_1_5, temperature: float = 0.75,
                     json_schema: Dict[str, Any] = None, **kwargs):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_UNSPECIFIED: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
    }

    arguments = {'model_name': model_name, 'temperature': temperature, 'safety_settings': safety_settings,
                 **kwargs}

    if json_schema is not None:
        arguments['response_mime_type'] = "application/json"
        arguments['response_schema'] = json_schema

    return ChatVertexAI(
        **arguments
    )

def get_together_model(model_name: str, temperature: float = 0.75,
                     json_schema: Dict[str, Any] = None, **kwargs):

    arguments = {'model': model_name, 'temperature': temperature, **kwargs}

    if json_schema is not None:
        arguments['response_format'] = {"type": "json_object", "schema": json_schema }

    return ChatTogether(**arguments)

def get_antropic_model(model_name: str = CLAUDE_3_5, temperature: float = 0.75, **kwargs):

    arguments = {'model': model_name, 'temperature': temperature, **kwargs}

    return ChatAnthropic(**arguments)

def text_embedding(corpus: list[str]):
    client = OpenAI()
    return client.embeddings.create(input=corpus, model="text-embedding-3-small", dimensions=TEXT_EMBEDDING_SIZE).data

async def atext_embedding(corpus: list[str]):
    return await asyncio.to_thread(text_embedding, corpus)
