from database import store_memory, search_memory, store_fact, retrieve_facts
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize LLM for summarization
llm = ChatGroq(model_name="llama-3.3-70b-specdec", temperature=0.7, max_tokens=400)

# Function to store user messages and bot responses
def manage_memory(user_id: str, role: str, content: str):
    store_memory(user_id, role, content)

# Function to retrieve context
def retrieve_context(user_id: str, query: str, top_k: int = 5):
    return search_memory(user_id, query, top_k)

# Summarization-based fact storage
def summarize_and_store_facts(user_id: str, messages: list[dict]):
    prompt_template = """
    Given the following conversation, summarize any essential facts that should be remembered permanently:
    {messages}
    """
    prompt = PromptTemplate(input_variables=["messages"], template=prompt_template)
    chain = llm | prompt

    conversation_text = "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)
    summary = chain.run(messages=conversation_text)

    store_fact(user_id, summary)
    return summary
