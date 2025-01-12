from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition
from langgraph.graph.message import add_messages
from memory_manager import manage_memory, retrieve_context, summarize_and_store_facts
from database import retrieve_facts
from typing import Annotated
from typing_extensions import TypedDict

# Initialize chatbot state graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot_logic(state: State, user_id: str):
    # Retrieve facts
    stored_facts = retrieve_facts(user_id)
    fact_string = "\n".join(f"- {fact}" for fact in stored_facts)

    # Retrieve vector-based memory
    user_query = state["messages"][-1]["content"]
    context_messages = retrieve_context(user_id, user_query)

    # Combine facts and context
    context = [
        {"role": "system", "content": f"The following facts are remembered:\n{fact_string}"}
    ]
    context.extend({"role": msg["role"], "content": msg["content"]} for msg in context_messages)

    # Pass updated context to the LLM
    state["messages"] = context + state["messages"]

    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot_logic)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

# Save summarized facts at intervals
def periodic_fact_storage(user_id: str, conversation: list[dict]):
    return summarize_and_store_facts(user_id, conversation)
