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
) -> str:
    response = client.responses.parse(
        model=model,
        input=prompt,
        instructions=system_prompt,
        text_format=output_structure,
        temperature=0.7,
    )
    #   ParsedResponse[~TextFormatT](id='resp_0fb2498e17a1d61f0069f7296d78c48194bf71d89fb058a5e1', created_at=1777805677.0, error=None, incomplete_details=None, instructions=None, metadata={}, model='gpt-5.4-2026-03-05', object='response', output=[ParsedResponseOutputMessage[~TextFormatT](id='msg_0fb2498e17a1d61f0069f7296e27b08194affd5766df08310f', content=[ParsedResponseOutputText[~TextFormatT](annotations=[], text='Hello! How can I help you today?', type='output_text', logprobs=[], parsed=None)], role='assistant', status='completed', type='message', phase='final_answer')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[], top_p=0.98, background=False, completed_at=1777805678.0, conversation=None, max_output_tokens=None, max_tool_calls=None, previous_response_id=None, prompt=None, prompt_cache_key=None, prompt_cache_retention='in_memory', reasoning=Reasoning(effort='none', generate_summary=None, summary=None), safety_identifier=None, service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text'), verbosity='medium'), top_logprobs=0, truncation='disabled', usage=ResponseUsage(input_tokens=7, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=13, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=20), user=None, billing={'payer': 'developer'}, frequency_penalty=0.0, moderation=None, presence_penalty=0.0, store=True)
    if output_structure:
        return response.output_parsed
    return response.output_text
