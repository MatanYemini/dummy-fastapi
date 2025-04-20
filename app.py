from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
import httpx
from typing import Optional
import asyncio

app = FastAPI(
    title="Email Availability Checker",
    description="API to check if a Gmail username is already taken",
    version="1.0.0"
)

class EmailRequest(BaseModel):
    """Request model for checking email availability."""
    domain: str = Field(..., description="Domain to check as a Gmail username")
    
    @property
    def email(self) -> str:
        """Construct the full email address."""
        return f"{self.domain}@gmail.com"

async def get_http_client():
    """Dependency to provide an HTTP client."""
    async with httpx.AsyncClient() as client:
        yield client

async def is_email_registered(as_client: httpx.AsyncClient, email: str) -> bool:
    """
        Abuse the gxlu endpoint to check if any email address
        is registered on Google. (not only gmail accounts)
    """
    req = await as_client.get(f"https://mail.google.com/mail/gxlu", params={"email": email})
    return "Set-Cookie" in req.headers

@app.post("/check-email", response_model=dict)
async def check_email_availability(
    request: EmailRequest,
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """Check if a Gmail username is already taken."""
    try:
        email = request.email
        is_registered = await is_email_registered(client, email)
        
        return {
            "email": email,
            "is_available": not is_registered,
            "is_registered": is_registered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check email: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 