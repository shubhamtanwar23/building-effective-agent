# Graph state
from typing import Literal

from pydantic import BaseModel, Field

from utils import call_llm


# Schema for structured output to use in evaluation
class Feedback(BaseModel):
    grade: Literal["funny", "not funny"] = Field(
        description="Decide if the joke is funny or not.",
    )
    feedback: str = Field(
        description="If the joke is not funny, provide feedback on how to improve it.",
    )


def generator(topic: str, feedback: str | None) -> str:
    """LLM generates a joke"""

    if feedback:
        msg = call_llm(
            f"Write a joke about {topic} but take into account the feedback: {feedback}"
        )
    else:
        msg = call_llm(f"Write a joke about {topic}")
    return msg


def evaluator(joke: str) -> Feedback:
    """LLM evaluates the joke"""

    return call_llm(f"Grade the joke: {joke}", output_structure=Feedback)


def run_evaluator_optimizer(topic: str):
    """Run the full evaluator-optimizer example"""

    feedback = None
    while True:
        joke = generator(topic, feedback)
        print("Generated joke:", joke)
        feedback = evaluator(joke)
        print("\n\nEvaluator feedback:", feedback)
        if feedback.grade == "funny":
            print("\nJoke accepted!")
            return joke
        elif feedback.grade == "not funny":
            print("\nJoke rejected, regenerating with feedback...")


if __name__ == "__main__":
    joke = run_evaluator_optimizer("Cats")
