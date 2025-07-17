from google.genai import types
from agent import root_agent_stateful
from session import SessionController
from google.adk.runners import Runner

APP_NAME = "WORKFLOW_APP"
USER_ID = "USER001"
SESSION_ID = "SESSION001" 

async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    #print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found

    #print(f"<<< Agent Response: {final_response_text}")


class AgentRunner:
    def __init__(self, ):
        pass

    async def init_session(self, init_state):
        # Session Init
        session_controller = SessionController()
        await session_controller.create_session(APP_NAME, USER_ID, SESSION_ID, init_state)
        self.stored_session = session_controller.session_service_stateful.sessions[APP_NAME][USER_ID][SESSION_ID]
        print(f"State: {self.stored_session.state}")
        self.stored_session.state['WorkflowState'] = 'Running'
        print(f"State: {self.stored_session.state}")

        # Runner Init
        self.runner_root_stateful = Runner(
            agent=root_agent_stateful,
            app_name=APP_NAME,
            session_service=session_controller.session_service_stateful
        )

    async def call_agent_seq(self, query: str):
        await call_agent_async(
        query= query,
        runner=self.runner_root_stateful,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    async def run_stateful_conversation(self, query_list: list[str]): 
        for query in query_list:
            await self.call_agent_seq(query)
        self.stored_session.state['WorkflowState'] = 'Finished'
        print(f"State: {self.stored_session.state}")