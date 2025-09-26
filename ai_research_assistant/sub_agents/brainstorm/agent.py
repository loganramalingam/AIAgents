"""BrainstormAgent for brainstorming research topics."""
from google.adk import Agent
from google.adk.tools import google_search
from . import prompt

MODEL = "gemini-2.5-pro"

brainstorm_agent = Agent(
    model=MODEL,
    name="BrainstormAgent",
    instruction=prompt.BRAINSTORM_AGENT_PROMPT,
    tools=[google_search],
)