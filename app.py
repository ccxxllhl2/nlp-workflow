import asyncio
from agent import root_agent_stateful
from session import SessionController
from google.adk.runners import Runner
from google.genai import types

APP_NAME = "WORKFLOW_APP"
USER_ID = "USER001"
SESSION_ID = "SESSION001" 

async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")

async def run_stateful_conversation():
    # Session Init
    session_controller = SessionController()
    await session_controller.create_session(APP_NAME, USER_ID, SESSION_ID)

    #init_session_state = await session_controller.get_session(APP_NAME, USER_ID, SESSION_ID)
    #print(f"Session state: {init_session_state.state['WorkflowState']}")
    stored_session = session_controller.session_service_stateful.sessions[APP_NAME][USER_ID][SESSION_ID]
    stored_session.state['WorkflowState'] = 'Running'
    print(f"|Init State: {stored_session.state}")

    # Create Runner
    runner_root_stateful = Runner(
        agent=root_agent_stateful,
        app_name=APP_NAME,
        session_service=session_controller.session_service_stateful
    )
    
    # Running Start Node
    await call_agent_async(
        query= "Hi!",
        runner=runner_root_stateful,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"|Start State: {stored_session.state}")

    # Running Jira Node
    await call_agent_async(
        query= "What's the markdown info from Jira?",
        runner=runner_root_stateful,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"|Jira State: {stored_session.state}")

    # Running End Node
    await call_agent_async(query= "Bye!",
        runner=runner_root_stateful,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    stored_session.state['WorkflowState'] = 'Finished'
    print(f"|End State: {stored_session.state}")

if __name__ == "__main__":
    asyncio.run(run_stateful_conversation())

