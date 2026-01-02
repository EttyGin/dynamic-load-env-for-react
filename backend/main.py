"""
FastAPI backend demonstrating runtime configuration via environment variables.
This server reads PORT from the environment and exposes a simple API endpoint.
"""

import os
from fastapi import FastAPI
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


@app.get("/api/hello")
def hello():
    """
    Simple endpoint that returns a greeting.
    Demonstrates that the backend is running and accessible.
    """
    return {"message": "hello from backend"}


if __name__ == "__main__":
    import uvicorn
    
    # Read port from environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Backend running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
