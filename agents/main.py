import os
import sys
import yaml
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from team.dev_team import dev_team

console = Console()

# Agent communication: English between agents, Italian for final user output
LANGUAGE_INSTRUCTION = (
    "Agent communication language: English. "
    "Final output to the user must be in Italian (lingua italiana)."
)


def load_template(name: str) -> str:
    """Load orchestrator_prompt from tasks/{name}.yaml."""
    task_path = Path(__file__).parent / "tasks" / f"{name}.yaml"
    if not task_path.exists():
        console.print(f"[bold red][SYSTEM][/bold red] Template '{name}' not found at {task_path}")
        sys.exit(1)
    with open(task_path) as f:
        data = yaml.safe_load(f)
    return data["orchestrator_prompt"]


def print_banner(task: str) -> None:
    litellm_url = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
    max_iter = os.getenv("MAX_REVIEW_ITERATIONS", "5")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_row("[cyan]LiteLLM URL[/cyan]", litellm_url)
    table.add_row("[cyan]Max iterations[/cyan]", max_iter)
    table.add_row("[cyan]Orchestrator[/cyan]", "orchestrator \u2192 Gemini 2.5 Pro")
    table.add_row("[cyan]Coder[/cyan]",        "coder        \u2192 OpenAI Codex")
    table.add_row("[cyan]Reviewer[/cyan]",      "reviewer     \u2192 Claude Sonnet 4")
    table.add_row("[cyan]Task[/cyan]",          task[:120] + ("\u2026" if len(task) > 120 else ""))

    console.print(Panel(table, title="[bold magenta]coding-agents-loop[/bold magenta]", expand=False))


def main() -> None:
    # Resolve task: CLI arg \u2192 stdin
    if len(sys.argv) > 1:
        raw_task = " ".join(sys.argv[1:])
    else:
        console.print("[bold magenta][SYSTEM][/bold magenta] Enter task (Ctrl+D to submit):")
        raw_task = sys.stdin.read().strip()

    # Template shortcut: "template:webapp" \u2192 loads tasks/webapp.yaml
    if raw_task.startswith("template:"):
        template_name = raw_task.split(":", 1)[1].strip()
        console.print(f"[bold magenta][SYSTEM][/bold magenta] Loading template: {template_name}")
        task = load_template(template_name)
    else:
        task = raw_task

    print_banner(task)

    console.print("[bold magenta][SYSTEM][/bold magenta] Starting DevTeam\u2026")
    result = dev_team.run(task + "\n\n" + LANGUAGE_INSTRUCTION)

    console.print(Panel(
        str(result),
        title="[bold white]Risultato finale[/bold white]",
        border_style="white",
    ))


if __name__ == "__main__":
    main()
