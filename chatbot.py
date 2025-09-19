import requests
import redis
import json
from config import OPENROUTER_API_KEY, MODEL_NAME, REDIS_HOST, REDIS_PORT, REDIS_DB
from retriever import retrieve_relevant_docs
from sanitizer import sanitize_input

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
MAX_CACHE_SIZE = 1000

def get_chatbot_response(user_query):
    sanitized_query = sanitize_input(user_query)
    cache_key = f"query:{sanitized_query}"
    cached_response = redis_client.get(cache_key)
    if cached_response:
        print(f"Cache hit for query: {sanitized_query}")
        return json.loads(cached_response)
    
    relevant_docs = retrieve_relevant_docs(sanitized_query, top_k=2)
    context = '\n'.join(relevant_docs)[:200] if relevant_docs else "No relevant information found."
    print(f"Context for query '{sanitized_query}': {context}")
    if not relevant_docs:
        response = "Sorry, I couldn't find relevant information. Please try rephrasing your question."
        redis_client.setex(cache_key, 3600, json.dumps(response))
        return response
    
    prompt = f"Context: {context}\nUser: {sanitized_query}\nAssistant:"
    print(f"Prompt sent to API: {prompt}")
    print(f"Using API Key: {OPENROUTER_API_KEY}")
    messages = [{"role": "user", "content": prompt}]
    response = get_api_response(messages)
    
    if redis_client.dbsize() < MAX_CACHE_SIZE:
        redis_client.setex(cache_key, 3600, json.dumps(response))
    else:
        print("Cache full, skipping cache for this response.")
    return response

def get_api_response(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.7,
    }
    print(f"Sending request to API with data: {data}")
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error in API request: {e}"