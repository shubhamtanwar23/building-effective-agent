import os

from dotenv import load_dotenv
from openai import Omit, OpenAI
from pydantic import BaseModel

load_dotenv()
omit = Omit()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def call_llm(
    prompt: str,
    system_prompt: str = "",
    model="gpt-5.4",
    output_structure: BaseModel | Omit = omit,
    temperature: float = 0.9,
) -> str:
    response = client.responses.parse(
        model=model,
        input=prompt,
        instructions=system_prompt,
        text_format=output_structure,
        temperature=temperature,
    )

    if output_structure:
        return response.output_parsed
    return response.output_text
