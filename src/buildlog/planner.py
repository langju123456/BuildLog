"""Story planning stage."""

from __future__ import annotations

from buildlog.config import Settings
from buildlog.llm_client import LLMClient
from buildlog.models import Iteration, StoryPlan
from buildlog.prompt_loader import load_prompt


def create_plan(iteration: Iteration, client: LLMClient, settings: Settings) -> StoryPlan:
    """Create a validated story plan for one iteration."""
    prompt = load_prompt(settings.prompts_dir, "planner_v1.md").format(
        iteration_json=iteration.model_dump_json(indent=2)
    )
    return client.complete_json(prompt, StoryPlan)
