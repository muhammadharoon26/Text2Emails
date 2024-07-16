from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
from typing import List

app = FastAPI()

class EmailOutput(BaseModel):
    emails: List[str]
    count: int

def extract_emails(text: str) -> List[str]:
    email_regex = r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)'
    return list(set(re.findall(email_regex, text)))

@app.post("/extract_emails", response_model=EmailOutput)
async def extract_and_format_emails(text: str):
    emails = extract_emails(text)
    if not emails:
        raise HTTPException(status_code=404, detail="No email addresses found")
    
    return EmailOutput(
        emails=emails,
        count=len(emails)
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Email Extractor API"}
