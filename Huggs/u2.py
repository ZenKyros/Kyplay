import os
from huggingface_hub import login

login()

from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=InferenceClientModel(
        model_id="moonshotai/Kimi-K2.5",
        token=HF_TOKEN,
    ),
)

# agent.run("What is the current suitation of Nepal Flood.")


#=====================================================================================================================


from smolagents import CodeAgent , tool, InferenceClientModel

@tool 

def suggest_menu(occasion : str )->str:
    """Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """

    if occasion == "casual":
            return "Pizza, snacks, and drinks."
    elif occasion == "formal":
            return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
            return "Buffet with high-energy and healthy food."
    else:
            return "Custom menu for the butler."
agent2 = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=InferenceClientModel(
        model_id="moonshotai/Kimi-K2.5",
        token=HF_TOKEN,
    ),
)

agent2.run("Prepare a formal menu for the party")