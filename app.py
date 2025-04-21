from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API Key securely from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file!")

@app.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text:
        return JSONResponse({"summary": "No input text provided."})

    # Create the prompt for summarization
    prompt = f"Summarize the following transcription into a clear, concise summary:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",  # Model used for summarization
        "messages": [
            {"role": "system", "content": "You are a helpful summarization assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the status code is 4xx/5xx

            result = response.json()

            # Log the response for debugging purposes
            logger.info(f"API Response: {result}")

            # Extract summary from response
            summary_text = result.get('choices', [{}])[0].get('message', {}).get('content', None)

            if not summary_text:
                raise ValueError("No summary content found in the response.")

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        return JSONResponse({"summary": "Failed to get a valid response from the summarization service."})
    except httpx.RequestError as e:
        logger.error(f"Error with request: {e}")
        return JSONResponse({"summary": "Failed to connect to the summarization service."})
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return JSONResponse({"summary": f"An error occurred: {str(e)}"})

    return JSONResponse({"summary": summary_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
