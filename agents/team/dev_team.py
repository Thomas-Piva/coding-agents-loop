import os
from agno.team import Team
from agents.orchestrator import orchestrator
from agents.coder import coder
from agents.reviewer import reviewer

dev_team = Team(
    name="DevTeam",
    mode="coordinate",
    leader=orchestrator,
    members=[coder, reviewer],
    max_iterations=int(os.getenv("MAX_REVIEW_ITERATIONS", 5)),
)
