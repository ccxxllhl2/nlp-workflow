import asyncio
from process import AgentRunner

runner = AgentRunner()

user_input = [
    "Hi!",
    "What's the markdown info from Jira?",
    "Goodbye!"
]

init_state = {
    'WorkflowState': 'Init',
    'Nodes': {
        'JIRA': {},
        'START': {},
        'END': {}
    }
}

if __name__ == "__main__":
    asyncio.run(runner.init_session(init_state))
    asyncio.run(runner.run_stateful_conversation(user_input))

