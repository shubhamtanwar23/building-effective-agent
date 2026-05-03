from typing import Literal

from pydantic import BaseModel, Field

from utils import call_llm


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(
        None, description="The next step in the routing process"
    )


# State
class State(BaseModel):
    input: str
    decision: str
    output: str


# Nodes
def generate_story(user_input: str):
    """Write a story"""

    return call_llm(user_input)


def generate_joke(user_input: str):
    """Write a joke"""

    return call_llm(user_input)


def generate_poem(user_input: str):
    """Write a poem"""

    return call_llm(user_input)


def llm_call_router(user_input: str) -> Route:
    """Route the input to the appropriate node"""

    # Run the augmented LLM with structured output to serve as routing logic
    return call_llm(
        prompt=user_input,
        system_prompt="You are a router that routes user input to the appropriate node based on whether they want a story, joke, or poem. Output only the next step in the routing process as either 'story', 'joke', or 'poem'.",
        output_structure=Route,
    )


def run_routing(user_input: str):
    """Run the routing example"""

    route = llm_call_router(user_input)
    if route.step == "story":
        print("generating story...")
        output = generate_story(user_input)
    elif route.step == "joke":
        print("generating joke...")
        output = generate_joke(user_input)
    elif route.step == "poem":
        print("generating poem...")
        output = generate_poem(user_input)
    else:
        output = (
            "Sorry, I didn't understand that. Please enter 'story', 'joke', or 'poem'."
        )

    print(output)


if __name__ == "__main__":
    run_routing("Write me a joke about cats")
