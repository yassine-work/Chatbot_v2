from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from chatbot import get_chatbot_response
from dotenv import load_dotenv
import os

load_dotenv()
print(f"API Key in backend.py: {os.getenv('OPENROUTER_API_KEY')}")
print(f"Redis Config: {os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}, DB {os.getenv('REDIS_DB')}")
print(f"ChromaDB Path: {os.getenv('CHROMA_PATH')}")

app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "http://localhost:5173"],  # Include frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.options("/chat")
async def options_chat(request: Request):
    print(f"OPTIONS request received. Headers: {request.headers}")
    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.post("/chat")
async def chat(request: Request):
    print(f"POST request received. Headers: {request.headers}")
    try:
        data = await request.json()
        print(f"POST request body: {data}")
        user_query = data.get("query", "")
        response = get_chatbot_response(user_query)
        return JSONResponse(content={"response": response})
    except Exception as e:
        print(f"Error in POST /chat: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)