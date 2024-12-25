import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv()

# Set up API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# Define the state type
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize memory
memory = MemorySaver()

# Configure tools
tool = TavilySearchResults(max_results=2, search_depth="advanced")
tools = [tool]

# Initialize LLM
llm = ChatGroq(model_name="llama-3.1-70b-versatile")
llm_with_tools = llm.bind_tools(tools)

# Build the state graph
graph_builder = StateGraph(State)

def chatbot(state: State):
    """Core chatbot function."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Add nodes
graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# Define edges
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Compile the graph
graph = graph_builder.compile(checkpointer=memory)

# Define constant config for single-user use
config = {"configurable": {"thread_id": "local_user"}}

# Load system prompt
with open("prompt.txt", "r") as file:
    prompt = file.read()

system_prompt = {
    "role": "system",
    "content": prompt
}

# Export objects for the app
__all__ = ["graph", "config", "system_prompt"]
