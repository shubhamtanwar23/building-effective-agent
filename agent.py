import json

from utils import call_llm

# Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "multiply",
        "description": "Multiply two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number to multiply.",
                },
                "b": {
                    "type": "number",
                    "description": "The second number to multiply.",
                },
            },
            "required": ["a", "b"],
        },
    },
    {
        "type": "function",
        "name": "add",
        "description": "Add two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number to add.",
                },
                "b": {
                    "type": "number",
                    "description": "The second number to add.",
                },
            },
            "required": ["a", "b"],
        },
    },
    {
        "type": "function",
        "name": "divide",
        "description": "Divide two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The numerator.",
                },
                "b": {
                    "type": "number",
                    "description": "The denominator.",
                },
            },
            "required": ["a", "b"],
        },
    },
]


def multiply(a: int, b: int) -> int:
    """Multiply `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a * b


def add(a: int, b: int) -> int:
    """Adds `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a + b


def divide(a: int, b: int) -> float:
    """Divide `a` and `b`.

    Args:
        a: First int
        b: Second int
    """
    return a / b


tools_by_name = {tool.__name__: tool for tool in [add, multiply, divide]}


def run_agent(input: str):
    """Run the agent example"""

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can perform basic math "
            "operations. You have access to the following tools: add, multiply, "
            "divide. Use these tools to answer the user's question. "
            "Always use the tools when performing calculations and show your work.",
        },
        {"role": "user", "content": input},
    ]
    while True:
        response = call_llm(
            prompt=messages,
            model="gpt-5.4",
            tools=tools,
        )

        messages.extend(response)
        for message in response:
            if message.type == "function_call":
                tool_name = message.name
                tool_args = json.loads(message.arguments)
                tool = tools_by_name.get(tool_name)
                if tool:
                    tool_response = tool(**tool_args)
                    print(
                        f"\nCalled tool {tool_name} with args {tool_args}, "
                        f"got response {tool_response}"
                    )
                    messages.append(
                        {
                            "type": "function_call_output",
                            "call_id": message.call_id,
                            "output": str(tool_response),
                        }
                    )
                else:
                    print(f"Tool {tool_name} not found.")
            elif message.type == "message":
                print("\nAgent:", message.content[0].text)
                if message.phase == "final_answer":
                    return


if __name__ == "__main__":
    run_agent("What is (2 + 3) * 4?")
