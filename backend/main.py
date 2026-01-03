"""
FastAPI backend demonstrating:
1. Runtime configuration via environment variables
2. HTTP Bearer token authentication
This server reads PORT and MASTER_API_KEY from environment variables.
"""

import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security setup
security = HTTPBearer()

# Read MASTER_API_KEY from environment variable
MASTER_API_KEY = os.environ.get("MASTER_API_KEY")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to verify Bearer token authentication.
    
    Raises:
        HTTPException: 401 Unauthorized if token is missing, invalid, or doesn't match MASTER_API_KEY
    """
    if not MASTER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not properly configured: MASTER_API_KEY environment variable not set"
        )
    
    token = credentials.credentials
    if token != MASTER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token


@app.get("/api/hello")
def hello(token: str = Depends(verify_token)):
    """
    Protected endpoint that returns a greeting.
    Requires valid Bearer token in Authorization header.
    
    Example:
        curl -H "Authorization: Bearer <MASTER_API_KEY>" http://localhost:8000/api/hello
    """
    return {"message": "hello from backend", "authenticated": True}


if __name__ == "__main__":
    import uvicorn
    
    # Read port from environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Backend running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
