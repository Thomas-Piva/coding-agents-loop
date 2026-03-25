import os
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from rich.console import Console
from tools.filesystem import read_file, write_file, list_files, delete_file
from tools.shell import run_command
from tools.git_tools import git_init, git_add, git_commit, git_diff, git_log

console = Console()

LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "sk-changeme")

coder = Agent(
    name="Coder",
    model=OpenAILike(
        id="coder",
        base_url=LITELLM_BASE_URL,
        api_key=LITELLM_API_KEY,
    ),
    instructions=(
        "Communicate with other agents in English. All internal reasoning "
        "and inter-agent messages must be in English.\n\n"
        "You are the Coder agent. Your responsibilities:\n"
        "1. Implement the code as requested by the Orchestrator.\n"
        "2. If you receive a list of issues from the Reviewer, fix them all.\n"
        "3. Write all files to /workspace using the filesystem tools.\n"
        "4. After completing your work, always produce a summary listing "
        "every file you created or modified, with a brief description."
    ),
    tools=[read_file, write_file, list_files, delete_file,
           run_command, git_init, git_add, git_commit, git_diff, git_log],
    show_tool_calls=True,
    markdown=True,
)


def log(message: str) -> None:
    console.print(f"[bold green][CODER][/bold green] {message}")
