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


# Push the agent that actually has the tool and ran
agent.push_to_hub('codewithkyros/Kyagen')

kyagen = agent.from_hub('codewithkyros/Kyagen', trust_remote_code=True)

kyagen.run("Give me the best playlist for a party at Wayne's mansion. The party idea is a 'villain masquerade' theme")  
