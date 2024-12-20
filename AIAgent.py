from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('api_key')

model = GeminiModel('gemini-1.5-flash', api_key=api_key)
agent = Agent(  
    model = model,
    system_prompt='Be concise, reply with one sentence.',  
)

result = agent.run_sync('How are you?')  
print(result.data)
