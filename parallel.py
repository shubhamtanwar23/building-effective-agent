from concurrent.futures import ThreadPoolExecutor

from utils import call_llm


def generate_joke(topic: str):
    """First LLM call to generate initial joke"""

    print(f"Generating joke about {topic}...")
    return call_llm(f"Write a short joke about {topic}")


def generate_story(topic: str):
    """Second LLM call to generate story"""

    print(f"Generating story about {topic}...")
    return call_llm(f"Write a short story about {topic}")


def generate_poem(topic: str):
    """Third LLM call to generate poem"""

    print(f"Generating poem about {topic}...")
    return call_llm(f"Write a short poem about {topic}")


def aggregator(topic, joke, story, poem):
    """Combine the joke, story and poem into a single output"""

    combined = f"Here's a story, joke, and poem about {topic}!\n\n"
    combined += f"STORY:\n{story}\n\n"
    combined += f"JOKE:\n{joke}\n\n"
    combined += f"POEM:\n{poem}"
    return combined


def run_parallel(topic: str):
    """Run the parallel example"""

    with ThreadPoolExecutor() as executor:
        joke_future = executor.submit(generate_joke, topic)
        story_future = executor.submit(generate_story, topic)
        poem_future = executor.submit(generate_poem, topic)

        joke = joke_future.result()
        story = story_future.result()
        poem = poem_future.result()

        combined_output = aggregator(topic, joke, story, poem)
        print("\n\n", combined_output)


if __name__ == "__main__":
    run_parallel("dogs")
