import os
from collections.abc import Iterable

from dotenv import load_dotenv
from openai import Omit, OpenAI
from openai.types.responses import ResponseInputParam
from openai.types.responses.tool_param import ParseableToolParam
from pydantic import BaseModel

load_dotenv()
omit = Omit()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def call_llm(
    prompt: str | ResponseInputParam,
    system_prompt: str = "",
    model="gpt-5.4",
    output_structure: BaseModel | Omit = omit,
    tools: Iterable[ParseableToolParam] | Omit = omit,
    temperature: float = 0.9,
) -> str:
    response = client.responses.parse(
        model=model,
        input=prompt,
        instructions=system_prompt,
        text_format=output_structure,
        tools=tools,
        temperature=temperature,
    )
    if tools:
        return response.output
    if output_structure:
        return response.output_parsed
    return response.output_text
