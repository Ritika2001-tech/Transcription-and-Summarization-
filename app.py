from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, specify allowed origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Key securely
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file!")

@app.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text:
        return JSONResponse({"summary": "No input text provided."})

    prompt = f"Summarize the following transcription into a clear, concise summary:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",  # free + powerful
        "messages": [
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        result = response.json()

    summary_text = result.get('choices', [{}])[0].get('message', {}).get('content', 'No summary available.')

    return JSONResponse({"summary": summary_text})

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
