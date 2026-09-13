import os
from huggingface_hub import login
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool

login()  # token must have WRITE access for push_to_hub

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")  # optional; login() already cached it

@tool
def suggest_menu(occasion: str) -> str:
    """Suggests a menu based on the occasion.

    Args:
        occasion (str): One of "casual", "formal", "superhero", or "custom".
    """
    menus = {
        "casual": "Pizza, snacks, and drinks.",
        "formal": "3-course dinner with wine and dessert.",
        "superhero": "Buffet with high-energy and healthy food.",
    }
    return menus.get(occasion, "Custom menu for the butler.")

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), suggest_menu],
    model=InferenceClientModel(
        model_id="moonshotai/Kimi-K2.5",
        token=HF_TOKEN,
    ),
    additional_authorized_imports=["datetime"],
)

agent.run("""
    Alfred needs to prepare for the party. Here are the tasks:
    1. Prepare the drinks - 30 minutes
    2. Decorate the mansion - 60 minutes
    3. Set up the menu - 45 minutes
    4. Prepare the music and playlist - 45 minutes

    If we start right now, at what time will the party be ready?
""")

# Push the agent that actually has the tool and ran
agent.push_to_hub('codewithkyros/Kyagen')