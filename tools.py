from google.adk.tools.tool_context import ToolContext
from typing import Optional
from collections import defaultdict
import time

class Tools:
    def __init__(self):
        self.history_cache = defaultdict(list)

    def get_jira_ticket(self, tickets: list, tool_context: ToolContext) -> str:
        """Retrieves markdown message from Jira system for demo test, directly return mock data."""

        # --- Read preference from state ---
        state = tool_context.state.get('Nodes')
        state['JIRA']['status'] = 'running'
        tool_context.state['Nodes'] = state
        
        # TODO: Jira Markdown API call to get ticket details

        # Mock Data
        result = '# Jira Demo Ticket\n * Hi\n *Jira Content\n.'
        state['JIRA']['message'] = result['markdown']
        state['JIRA']['status'] = 'finished'
        tool_context.state['Nodes'] = state
        self.history_cache['JIRA'].append(
            {
                "date": time.time(),
                "content": result['markdown']
            }
        )
        return result

    def get_confluence_info(self, ticket_url: str, tool_context: ToolContext, name: Optional[str] = None) -> str: # MODIFIED SIGNATURE
        """Retrieves markdown message from Confluence system for demo test, directly return mock data."""
        state = tool_context.state.get('Nodes')
        state['CONFLUENCE']['status'] = 'running'
        tool_context.state['Nodes'] = state

        result = "Mock Confluence Info"
        state['CONFLUENCE']['message'] = result

        # TODO: Confluence API call

        state['CONFLUENCE']['status'] = 'finished'
        tool_context.state['Nodes'] = state
        self.history_cache['CONFLUENCE'].append(
            {
                "date": time.time(),
                "content": result
            }
        )

        return result

    def security_logging(self, useless_info: str, tool_context: ToolContext) -> str:
        """Warning and log user if user's request is relevent from security perspective or not about work."""
        state = tool_context.state.get('Nodes')
        state['SECURITY']['status'] = 'running'
        tool_context.state['Nodes'] = state

        result = "This is not about our organization. And AI will not response for it. \nYour illegal message: " + useless_info

        state['SECURITY']['message'] = result
        state['SECURITY']['status'] = 'finished'
        tool_context.state['Nodes'] = state

        self.history_cache['SECURITY'].append(
            {
                "date": time.time(),
                "content": result
            }
        )

        return result
    
    def search_requirements(self, query: str, tool_context: ToolContext) -> str:
        """Search requirements in internal knowledge base based on query."""
        state = tool_context.state.get('Nodes')
        state['REQUIREMENTS']['status'] = 'running'
        tool_context.state['Nodes'] = state

        # TODO: Search requirements in internal knowledge base
        result = "Mock Requirements Info"

        state['REQUIREMENTS']['message'] = result
        state['REQUIREMENTS']['status'] = 'finished'
        tool_context.state['Nodes'] = state

        self.history_cache['REQUIREMENTS'].append(
            {
                "date": time.time(),
                "content": result
            }
        )
        return result
    
    def search_user_story(self, query: str, tool_context: ToolContext) -> str:
        """Search user story in internal knowledge base based on query."""
        state = tool_context.state.get('Nodes')
        state['USER STORY']['status'] = 'running'
        tool_context.state['Nodes'] = state

        # TODO: Search user story in internal knowledge base
        result = "Mock User Story Info"

        state['USER STORY']['message'] = result
        state['USER STORY']['status'] = 'finished'
        tool_context.state['Nodes'] = state

        self.history_cache['USER STORY'].append(
            {
                "date": time.time(),
                "content": result
            }
        )
        return result