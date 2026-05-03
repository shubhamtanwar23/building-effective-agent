from utils import call_llm


def generate_joke(topic: str):
    """First LLM call to generate initial joke"""

    return call_llm(f"Write a short joke about {topic}")


def check_punchline(joke: str):
    """Gate function to check if the joke has a punchline"""

    # Simple check - does the joke contain "?" or "!"
    if "?" in joke or "!" in "joke":
        return "Pass"
    return "Fail"


def improve_joke(joke: str):
    """Second LLM call to improve the joke"""

    return call_llm(f"Make this joke funnier by adding wordplay: {joke}")


def polish_joke(joke: str):
    """Third LLM call for final polish"""
    return call_llm(f"Add a surprising twist to this joke: {joke}")


def run_chaining(topic: str):
    """Run the full chaining example"""

    joke = generate_joke(topic)
    print("Initial joke:", joke)
    if check_punchline(joke) == "Pass":
        print("Joke has a punchline, done generating joke...")
        return joke
    else:
        print("Joke is missing a punchline, improving it...")
        improved_joke = improve_joke(joke)
        print("Improved joke:", improved_joke)
        print("Polishing joke...")
        polished_joke = polish_joke(improved_joke)
        print("Polished joke:", polished_joke)
        return polished_joke


if __name__ == "__main__":
    run_chaining("cats")
