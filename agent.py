from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tools import BaseTools

MODEL_DEEPSEEK = "deepseek/deepseek-chat"
base_tools = BaseTools(jira_token="123", jira_source="w")

greeting_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="START",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[base_tools.say_hello],
    #output_key="greeting_message"
)
print(f"Agent: [{greeting_agent.name}] ready.")

farewell_agent = Agent(
    model=LiteLlm(model=MODEL_DEEPSEEK),
    name="END",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[base_tools.say_goodbye],
    #output_key="farewell_message"
)
print(f"Agent: [{farewell_agent.name}] ready.")

root_agent_stateful = Agent(
    name="JIRA", # New version name
    model=LiteLlm(model=MODEL_DEEPSEEK) ,
    description="Main agent: Provides Jira info, delegates greetings/farewells, saves message to state.",
    instruction="You are the BusinessManager. Your job is to provide Jira info using 'get_jira_info'. "
                "The tool will format the Jira info based on user preference stored in state. "
                "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                "Handle only Jira requests, greetings, and farewells.",
    tools=[base_tools.get_jira_ticket], # Use the state-aware tool
    sub_agents=[greeting_agent, farewell_agent], # Include sub-agents
    #output_key="Jira_markdown" # <<< Auto-save agent's final response
)
print(f"Agent: [{root_agent_stateful.name}] ready.")

