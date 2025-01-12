import os
from supabase import create_client
from openai.embeddings_utils import get_embedding
import openai

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to embed text
def embed_text(text: str) -> list[float]:
    return get_embedding(text, model="text-embedding-ada-002")

# Store memory in the database
def store_memory(user_id: str, role: str, content: str):
    embedding = embed_text(content)
    response = supabase.table("memory").insert({
        "user_id": user_id,
        "role": role,
        "content": content,
        "embedding": embedding
    }).execute()
    return response

# Search memory using pgvector
def search_memory(user_id: str, query: str, top_k: int = 5):
    query_embedding = embed_text(query)
    sql_query = """
        SELECT content, role
        FROM memory
        WHERE user_id = %s
        ORDER BY embedding <=> %s
        LIMIT %s;
    """
    response = supabase.rpc("sql", {"query": sql_query, "params": [user_id, query_embedding, top_k]}).execute()
    return response.data

# Store summarized facts
def store_fact(user_id: str, fact: str):
    response = supabase.table("facts").insert({
        "user_id": user_id,
        "fact": fact
    }).execute()
    return response

# Retrieve stored facts
def retrieve_facts(user_id: str):
    response = supabase.table("facts").select("*").eq("user_id", user_id).execute()
    return [fact["fact"] for fact in response.data]
