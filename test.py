from session import SessionController
import asyncio

async def test():
    session_controller = SessionController()
    await session_controller.create_session(
        app_name = 'WORKFLOW_APP',
        user_id = 'USER001',
        session_id = 'SESSION001'    
    )
    retrieved_session = await session_controller.get_session(
        app_name = 'WORKFLOW_APP',
        user_id = 'USER001',
        session_id = 'SESSION001'
    )
    print(retrieved_session.state)


if __name__ == '__main__':
    asyncio.run(test())