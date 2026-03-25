import os
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from rich.console import Console

console = Console()

LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "sk-changeme")

orchestrator = Agent(
    name="Orchestrator",
    model=OpenAILike(
        id="orchestrator",
        base_url=LITELLM_BASE_URL,
        api_key=LITELLM_API_KEY,
    ),
    instructions=(
        "Communicate with other agents in English. All internal reasoning "
        "and inter-agent messages must be in English. "
        "Final output and summaries to the end user must be in Italian.\n\n"
        "You are the Orchestrator agent. Your responsibilities:\n"
        "1. Decompose the user task into clear subtasks.\n"
        "2. Assign the subtasks to the Coder agent with explicit instructions.\n"
        "3. Forward the Coder's output to the Reviewer agent for review.\n"
        "4. If the Reviewer returns a list of issues, re-assign the task to "
        "the Coder including the issue list as context. Repeat until the "
        "Reviewer responds with 'APPROVATO' or until MAX_REVIEW_ITERATIONS.\n"
        "5. When approved, present the final result to the user in Italian."
    ),
)


def log(message: str) -> None:
    console.print(f"[bold blue][ORCHESTRATOR][/bold blue] {message}")
