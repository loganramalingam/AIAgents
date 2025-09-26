"""CoreAgent: The primary user interface and dispatcher."""
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt
from .sub_agents.brainstorm import brainstorm_agent
from .sub_agents.deep_dive import deep_dive_agent

MODEL = "gemini-2.5-pro"

# This is the root agent that the user interacts with.
# It uses the other agents as tools to accomplish its tasks.
root_agent = LlmAgent(
    name="ai_research_assistant",
    model=MODEL,
    output_key="answer",
    description=(
        "A multi-agent AI research assistant."
        "that can brainstorm on a specific topic or "
        "provide deep dive on specifc research paper"),
    instruction=prompt.CORE_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=deep_dive_agent),
        AgentTool(agent=brainstorm_agent),
    ],
)