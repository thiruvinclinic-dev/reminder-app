import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# Use environment variable or fallback to your key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

class CommandRequest(BaseModel):
    command: str

@app.post("/parse")
def parse_command(req: CommandRequest):
    prompt = f"""
    You are a personal secretary. Parse the following request into a strict JSON object with these keys:
    - "action": "call", "message", "calendar", or "reminder"
    - "title": string (summary or title)
    - "target": string (contact name, phone number, or details)
    - "time": string (ISO format or descriptive time like "tomorrow at 10 AM")

    Request: "{req.command}"
    """
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))