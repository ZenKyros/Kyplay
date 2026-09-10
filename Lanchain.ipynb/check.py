import os 
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
from langchain.agents import create_agent

agent = create_agent(
    model="openrouter:nex-agi/nex-n2.5-mini:free"
)

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Explain quantum entanglement in simple terms."
        }
    ]
})

print(response["messages"][-1].content)