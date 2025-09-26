"""DeepDiveAgent for analyzing specific research papers."""
from google.adk import Agent
from google.adk.tools import google_search
from ai_research_assistant.tools import url_reader
from . import prompt

MODEL = "gemini-2.5-pro"


deep_dive_agent = Agent(
    model=MODEL,
    name="DeepDiveAgent",
    instruction=prompt.DEEP_DIVE_AGENT_PROMPT,
    tools=[google_search],
)