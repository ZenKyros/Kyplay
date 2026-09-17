
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langchain.messages import SystemMessage

from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

# 1. Define your local LLM
# This automatically connects to http://localhost:11434 by default
local_llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

##Define tool 
@tool

def mutiply(a :int, b : int)-> int:
    """ Multiply 'a' with 'b'
    Args :
        a : First in
        b  : second int 

    
    """

    return a * b 

@tool

def add (a :int, b : int)-> int:
    """ Add 'a' with 'b'
    Args :
        a : First in
        b  : second int 

    
    """

    return a + b 


@tool

def divide (a :int, b : int)-> int:
    """ Divide 'a' with 'b'
    Args :
        a : First in
        b  : second int 

    
    """

    return a / b 


tools = [divide, add, mutiply]

tools_by_name = {tool.name : tool for tool in tools }

model_with_tools = local_llm.bind_tools(tools)\




class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

from langchain.messages import SystemMessage


def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

from langchain.messages import ToolMessage


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


from typing import Literal
from langgraph.graph import StateGraph, START, END


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END


# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Compile the agent
agent = agent_builder.compile()

# Show the agent

# Invoke
from langchain.messages import HumanMessage
messages = [HumanMessage(content="what is three and 4 add ")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()

