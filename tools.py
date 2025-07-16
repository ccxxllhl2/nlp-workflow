from google.adk.tools.tool_context import ToolContext
from typing import Optional

class JiraTools:
    def __init__(self, jira_token: str, jira_source: str):
        self.jira_url = "https://w" if jira_source == 'w' else jira_source == 'a'

    def get_jira_ticket(self, ticket_key: str, tool_context: ToolContext) -> dict:
        """Retrieves markdown message from Jira system for demo test, directly return mock data."""
        print(f"--- Tool: get_jira_ticket called for {ticket_key} ---")

        # --- Read preference from state ---
        state_for_now = tool_context.state.get("tool_get_jira_ticket_used")
        
        # TODO: Jira Markdown API call to get ticket details

        # Mock Data
        result = {'status': 'success', 'markdown': '# Jira Demo Ticket\n * Hi.'}
        tool_context.state["tool_get_jira_ticket_used"] = True
        return result

def say_hello(tool_context: ToolContext, name: Optional[str] = None) -> str: # MODIFIED SIGNATURE
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    # MODIFICATION START
    tool_context.state['start_node'] = 'finished'
    if name:
        greeting = f"Hello, {name}!"
    else:
        greeting = "Hello there!" # Default greeting if name is None or not explicitly passed
    return greeting

def say_goodbye(tool_context: ToolContext) -> str:
    """Provides a simple farewell message to conclude the conversation."""
    tool_context.state['end_node'] = 'finished'
    return "Goodbye! Have a great day."