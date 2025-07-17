from google.adk.tools.tool_context import ToolContext
from typing import Optional

class BaseTools:
    def __init__(self, jira_token: str, jira_source: str):
        self.jira_url = "https://w" if jira_source == 'w' else jira_source == 'a'

    def get_jira_ticket(self, ticket_key: str, tool_context: ToolContext) -> dict:
        """Retrieves markdown message from Jira system for demo test, directly return mock data."""

        # --- Read preference from state ---
        state = tool_context.state.get('Agents')
        state['JIRA']['status'] = 'running'
        tool_context.state['Agents'] = state
        
        # mock
        print(f"STATE: {tool_context.state.get('Agents')}")
        
        # TODO: Jira Markdown API call to get ticket details

        # Mock Data
        result = {'markdown': '# Jira Demo Ticket\n * Hi\n *Jira Content\n.'}
        state['JIRA']['message'] = result['markdown']
        state['JIRA']['status'] = 'finished'
        tool_context.state['Agents'] = state
        print(f"STATE: {tool_context.state.get('Agents')}")
        return result

    def say_hello(self, tool_context: ToolContext, name: Optional[str] = None) -> str: # MODIFIED SIGNATURE
        """Provides a simple greeting. If a name is provided, it will be used."""
        state = tool_context.state.get('Agents')
        state['START']['status'] = 'running'
        tool_context.state['Agents'] = state
        print(f"STATE: {tool_context.state.get('Agents')}")
        if name:
            greeting = f"Hello, {name}!"
        else:
            greeting = "Hello there!" # Default greeting if name is None or not explicitly passed
        state['START']['message'] = greeting
        state['START']['status'] = 'finished'
        tool_context.state['Agents'] = state

        print(f"STATE: {tool_context.state.get('Agents')}")
        return greeting

    def say_goodbye(self, tool_context: ToolContext) -> str:
        """Provides a simple farewell message to conclude the conversation."""
        state = tool_context.state.get('Agents')
        state['END']['status'] = 'running'
        tool_context.state['Agents'] = state
        print(f"STATE: {tool_context.state.get('Agents')}")

        goodbye = "Goodbye! Have a great day."
        state['END']['message'] = goodbye
        state['END']['status'] = 'finished'
        tool_context.state['Agents'] = state

        print(f"STATE: {tool_context.state.get('Agents')}")
        return "Goodbye! Have a great day."