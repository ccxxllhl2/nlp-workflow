from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools import Tools

MODEL_DEEPSEEK = "deepseek/deepseek-chat"
base_tools = Tools()

jira_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="JIRA",
    instruction="You are the Jira Agent. Your ONLY task is to provide Jira info using 'get_jira_info' tool."
                "The tool will format the Jira info based on user preference stored in state. "
                "You should save your response to state.",
    description="Provides Jira info",
    tools=[base_tools.get_jira_ticket],
    output_key="agentJiraLast"
)

confluence_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="CONFLUENCE",
    instruction="You are the Confluence Agent. Your ONLY task is to provide Confluence info using 'get_confluence_info' tool."
                "The tool will format the Confluence info based on user preference stored in state. "
                "You should save your response to state.",
    description="Output Confluence info in markdown format",
    tools=[base_tools.get_confluence_info],
    output_key="agentConflLast"
)

security_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="SECURITY",
    instruction="You are the Security Agent. Your task is to provide the default warning info and log user request to the security log using 'security_logging' tool."
                "The tool will log user request to the security log. "
                "You should save your response to state.",
    description="Output Security info in markdown format",
    tools=[base_tools.security_logging]
)

requirements_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="REQUIREMENTS",
    instruction="You are the Requirements Agent. Your task is to provide the professional requirement based on user's request."
                "You can analysis user's intent and create query from user's message, then use the tool 'search_requirements' to search the requirements in internal knowledge base."
                "You should save your response to state.",
    description="Output Requirements in markdown format",
    tools=[base_tools.search_requirements],
    output_key="agentRequirementLast"
)

user_story_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="USER_STORY",
    instruction="You are the User Story Agent. Your task is to write professional UserStory based on requirements."
                "You can analysis requirements and create query from requirements, then use the tool 'search_user_story' to search history UserStory as reference."
                "You should save your response to state.",
    description="Output UserStory in markdown format",
    tools=[base_tools.search_user_story],
    output_key="agentUserStoryLast"
)

root_agent = Agent(
    name="Master", # New version name
    model=LiteLlm(model=MODEL_DEEPSEEK) ,
    description="Main agent: delegates all tasks to sub agents. Split task into sub tasks and delegate to sub agents.",
    instruction="You are the Master Agent. Your job is to identify the user's request and delegate it to the appropriate sub agent. "
                "User will ONLY talk with you and you need to delegate the task to the appropriate sub agent."
                "Handle ONLY Jira and Confluence requests, user requirements, and user stories."
                "If the user's request is not related to any known sub agents, just delegate it to the security agent."
                "You should save your response to state. "
                "Summary  and include necessary information into your response.",
    sub_agents=[jira_agent, confluence_agent, security_agent], # Include sub-agents
    output_key="ResponseLast"
)

