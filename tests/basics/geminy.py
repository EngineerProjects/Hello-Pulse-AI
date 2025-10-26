from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
import random

import os
from dotenv import load_dotenv
load_dotenv()

provider = GoogleProvider(api_key=os.getenv('GOOGLE_API_KEY'))


roulette_agent = Agent(
    GoogleModel('gemini-2.5-flash', provider=provider), 
    deps_type=int,
    output_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'

# Run agent
success_number = 18 # random.randint(1, 10)
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.output)

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.output)