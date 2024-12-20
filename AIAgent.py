from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

model = GeminiModel('gemini-1.5-flash', api_key='AIzaSyB2AvYTlbs_9nY-_MF-3xL3PLDA0IMxY3o')
agent = Agent(  
    model = model,
    system_prompt='Be concise, reply with one sentence.',  
)

result = agent.run_sync('How are you?')  
print(result.data)
