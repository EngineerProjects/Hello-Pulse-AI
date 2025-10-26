from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
import httpx
import random

# Create a custom HTTP client with longer timeout for slow computers
custom_client = httpx.AsyncClient(timeout=300)

ollama_model = OpenAIChatModel(
    model_name='mistral',
    provider=OllamaProvider(
        base_url='http://localhost:11434/v1',
        http_client=custom_client
    )
)

roulette_agent = Agent(
    ollama_model, 
    deps_type=int,
    output_type=str,
    retries=2,
    system_prompt=(
        'You must check if a roulette bet wins. '
        'Call the roulette_wheel function with the number the customer chose. '
        'Return EXACTLY what the function returns: either "winner" or "loser". '
        'Do not add any other text or explanation.'
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