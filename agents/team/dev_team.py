import os
from agno.team import Team
from agno.models.openai.like import OpenAILike
from agents.coder import coder
from agents.reviewer import reviewer

LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "sk-changeme")

dev_team = Team(
    name="DevTeam",
    mode="coordinate",
    model=OpenAILike(
        id="orchestrator",
        base_url=LITELLM_BASE_URL,
        api_key=LITELLM_API_KEY,
    ),
    members=[coder, reviewer],
    instructions=(
        "Communicate with other agents in English. All internal reasoning "
        "and inter-agent messages must be in English. "
        "Final output and summaries to the end user must be in Italian.\n\n"
        "You are the Orchestrator. Decompose the task, assign to Coder, "
        "send output to Reviewer. If Reviewer returns issues, re-assign to "
        "Coder with the issue list as context. Repeat until 'APPROVATO'."
    ),
    max_iterations=int(os.getenv("MAX_REVIEW_ITERATIONS", 5)),
)
