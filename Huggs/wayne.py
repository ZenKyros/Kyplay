import os
from huggingface_hub import login
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool
from huggingface_hub import list_repo_files

login()  #

HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY") 
agent = agent.from_hub.from_hub(
    "codewithkyros/Kyagen",
    repo_type="space",           # or "model"
    trust_remote_code=True,      # required to load pushed tools
    model=InferenceClientModel(
        model_id="moonshotai/Kimi-K2.5",
        token=HF_TOKEN,
    ),
)


kyagen = agent.from_hub('codewithkyros/Kyagen', trust_remote_code=True)

kyagen.run("Give me the best playlist for a party at Wayne's mansion. The party idea is a 'villain masquerade' theme")  
