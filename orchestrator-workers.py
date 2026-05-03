from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field

from utils import call_llm


class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )


class Sections(BaseModel):
    sections: list[Section] = Field(
        description="Sections of the report.",
    )


def orchestrator(topic: str) -> Sections:
    """Orchestrator that generates a plan for the report"""

    # Generate queries
    return call_llm(
        prompt=f"Generate a plan for the report on the topic: {topic}",
        system_prompt="You are a report planner. Generate a structured plan for the report.",
        output_structure=Sections,
    )


def worker(section: Section) -> str:
    """Worker writes a section of the report"""

    # Generate section
    return call_llm(
        prompt=f"Here is the section name: {section.name} and description: {section.description}",
        system_prompt="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting.",
    )


def run_workers(sections: list[Section]) -> list[str]:
    """Assign a worker to each section in the plan"""

    # Kick off section writing in parallel via Send() API
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(worker, section) for section in sections]
        return [future.result() for future in futures]


def synthesizer(completed_sections: list[str]) -> str:
    """Synthesize full report from sections"""
    # Format completed section to str to use as context for final sections
    return "\n\n---\n\n".join(completed_sections)


def run_orchestrator_workers(topic: str):
    """Run the full orchestrator-workers example"""

    # Step 1: Orchestrator generates plan for report
    plan = orchestrator(topic)
    print("\n\nGenerated plan:", plan, "\n\n")

    # Step 2: Workers write sections of the report in parallel
    completed_sections = run_workers(plan.sections)

    # Step 3: Synthesize final report from completed sections
    final_report = synthesizer(completed_sections)
    print("\n\nFinal report:\n", final_report)


if __name__ == "__main__":
    run_orchestrator_workers("The impact of climate change on global agriculture")
