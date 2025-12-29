"""
PMM Deep Agent Factory.

Creates configurable PMM agents with different capability modes.
"""

from typing import Literal

# from langchain_anthropic import ChatAnthropic (Removed)
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from .prompts import (
    MAIN_SYSTEM_PROMPT,
    COMPETITIVE_ANALYST_PROMPT,
    MESSAGING_SPECIALIST_PROMPT,
    LAUNCH_COORDINATOR_PROMPT,
)
from .tools import (
    INTAKE_TOOLS,
    RESEARCH_TOOLS,
    PLANNING_TOOLS,
    RISK_TOOLS,
    ALL_TOOLS,
    HUMAN_APPROVAL_TOOLS,
)


AgentMode = Literal["full", "intake", "research", "planning", "risk"]

# Define the model once so we can reuse it easily
def get_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

def create_pmm_agent(
    mode: AgentMode = "full",
    model_name: str = "gemini-2.5-flash",
    with_subagents: bool = True,
):
    """
    Create a PMM agent with the specified capabilities.
    """
    # Select tools based on mode
    tools = []
    if mode == "full":
        tools = ALL_TOOLS
    elif mode == "intake":
        tools = INTAKE_TOOLS
    elif mode == "research":
        tools = RESEARCH_TOOLS + INTAKE_TOOLS 
    elif mode == "planning":
        tools = PLANNING_TOOLS + INTAKE_TOOLS
    elif mode == "risk":
        tools = RISK_TOOLS + RESEARCH_TOOLS

    # Initialize model (Using Google)
    llm = get_model()
    
    # Create base agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        # CHANGED: messages_modifier -> prompt
        prompt=MAIN_SYSTEM_PROMPT,
    )

    return agent


def create_competitive_analyst():
    """Create a specialist agent for competitive intelligence."""
    llm = get_model()
    return create_react_agent(
        model=llm,
        tools=RESEARCH_TOOLS,
        # CHANGED: messages_modifier -> prompt
        prompt=COMPETITIVE_ANALYST_PROMPT,
    )


def create_messaging_specialist():
    """Create a specialist agent for messaging work."""
    llm = get_model()
    return create_react_agent(
        model=llm,
        tools=PLANNING_TOOLS,
        # CHANGED: messages_modifier -> prompt
        prompt=MESSAGING_SPECIALIST_PROMPT,
    )


def create_launch_coordinator():
    """Create a specialist agent for launch planning."""
    llm = get_model()
    return create_react_agent(
        model=llm,
        tools=PLANNING_TOOLS + RISK_TOOLS,
        # CHANGED: messages_modifier -> prompt
        prompt=LAUNCH_COORDINATOR_PROMPT,
    )


# Convenience exports
agent = create_pmm_agent()