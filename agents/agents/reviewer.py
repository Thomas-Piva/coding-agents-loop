import os
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from rich.console import Console
from tools.filesystem import read_file, list_files
from tools.shell import run_command

console = Console()

LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "sk-changeme")

reviewer = Agent(
    name="Reviewer",
    model=OpenAILike(
        id="reviewer",
        base_url=LITELLM_BASE_URL,
        api_key=LITELLM_API_KEY,
    ),
    instructions=(
        "Communicate with other agents in English. All internal reasoning "
        "and inter-agent messages must be in English.\n"
        "When producing the final APPROVED message or the list of issues to fix, "
        "write it in Italian for the end user.\n\n"
        "You are the Reviewer agent. Your responsibilities:\n"
        "1. Review all files in /workspace produced by the Coder.\n"
        "2. Run linting and basic tests using the shell tool if applicable.\n"
        "3. If everything is correct, respond with exactly: 'APPROVATO'\n"
        "4. If there are issues, respond with a numbered list in Italian "
        "describing each problem clearly, so the Coder can fix them."
    ),
    tools=[read_file, list_files, run_command],
    show_tool_calls=True,
    markdown=True,
)


def log(message: str) -> None:
    console.print(f"[bold yellow][REVIEWER][/bold yellow] {message}")
