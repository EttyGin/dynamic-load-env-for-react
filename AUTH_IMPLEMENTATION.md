# HTTP Bearer Authentication Implementation

## Overview

This project demonstrates how to implement HTTP Bearer token authentication in a production-like scenario where:
- The API key is read from **environment variables** (never hardcoded)
- The frontend reads the key from **runtime configuration** (not build-time)
- All API requests are **authenticated** with Bearer tokens

## Architecture

### Backend (FastAPI)

```
┌─────────────────────────────────────────┐
│ Environment Variable: MASTER_API_KEY    │
│ (set at runtime, not in code)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ FastAPI with HTTPBearer security        │
│ - verify_token() dependency             │
│ - Checks Authorization header           │
│ - Compares token to MASTER_API_KEY      │
│ - Returns 401 if invalid                │
└────────────────┬────────────────────────┘
                 │
                 ▼
        Protected /api/* endpoints
```

### Frontend (React + TypeScript)

```
┌─────────────────────────────────────────┐
│ Runtime config (config.json)            │
│ - BACKEND_URL                           │
│ - MASTER_API_KEY                        │
│ (loaded at app startup, not bundled)    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ React App (App.tsx)                     │
│ - Fetches config.json at runtime        │
│ - Includes Authorization header:        │
│   Authorization: Bearer <MASTER_API_KEY>│
└────────────────┬────────────────────────┘
                 │
                 ▼
        API requests to protected endpoints
```

## Setup & Running

### 1. Start the Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with MASTER_API_KEY environment variable
MASTER_API_KEY=super-secret-key python main.py
```

The server will start on `http://localhost:8000`

### 2. Start the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The app will start on `http://localhost:5173`

### 3. Test the Authentication

```bash
python test_auth.py
```

This script demonstrates:
- ❌ Request without token → 401 Unauthorized
- ❌ Request with wrong token → 401 Unauthorized
- ✅ Request with correct token → 200 Success

## Implementation Details

### Backend: `backend/main.py`

**Key Components:**

1. **Read API Key from Environment**
```python
MASTER_API_KEY = os.environ.get("MASTER_API_KEY")
```

2. **HTTPBearer Security**
```python
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()
```

3. **Token Verification Dependency**
```python
def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    if not MASTER_API_KEY:
        raise HTTPException(status_code=500, detail="...")
    
    token = credentials.credentials
    if token != MASTER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token
```

4. **Protected Endpoint**
```python
@app.get("/api/hello")
def hello(token: str = Depends(verify_token)):
    return {"message": "hello from backend", "authenticated": True}
```

### Frontend: Configuration

**`frontend/public/config.json`**
```json
{
    "BACKEND_URL": "http://localhost:8000",
    "MASTER_API_KEY": "super-secret-key"
}
```

**Key Points:**
- NOT bundled into the React build
- Loaded at runtime before app renders
- Can be changed without rebuilding

### Frontend: `frontend/src/config.ts`

```typescript
interface Config {
    BACKEND_URL: string;
    MASTER_API_KEY: string;
}

export async function loadConfig(): Promise<Config> {
    const response = await fetch('/config.json');
    config = await response.json();
    return config;
}

export function getConfig(): Config {
    if (!config) throw new Error('Config not loaded yet.');
    return config;
}
```

### Frontend: `frontend/src/App.tsx`

**API call with Authorization header:**
```typescript
const config = getConfig();

const response = await fetch(`${config.BACKEND_URL}/api/hello`, {
    headers: {
        'Authorization': `Bearer ${config.MASTER_API_KEY}`
    }
});
```

## Testing Without Frontend

### Using cURL

**Without token (fails):**
```bash
curl http://localhost:8000/api/hello
# Response: 403 Forbidden (or 401 depending on implementation)
```

**With correct token:**
```bash
curl -H "Authorization: Bearer super-secret-key" http://localhost:8000/api/hello
# Response: {"message": "hello from backend", "authenticated": true}
```

**With wrong token (fails):**
```bash
curl -H "Authorization: Bearer wrong-token" http://localhost:8000/api/hello
# Response: 401 Unauthorized
```

## Important Notes

### Security (Development Only)

This is a **technical demonstration**, NOT a production authentication system:

✅ **What this shows:**
- Reading secrets from environment variables
- Using runtime configuration for API keys
- Bearer token authentication pattern
- Keeping secrets out of frontend builds

❌ **What this is NOT:**
- Production-grade authentication
- Suitable for real applications without additional security measures
- A replacement for OAuth2, JWT, or proper session management

### Environment Variable Management

**Backend:** Must receive `MASTER_API_KEY` at runtime
```bash
# Good: Pass via environment
MASTER_API_KEY=secret python backend/main.py

# Bad: Never hardcode
MASTER_API_KEY = "secret"  # in code
```

**Frontend:** Reads from `config.json` (never from build-time environment)
```javascript
// Good: Load from runtime config
const key = config.MASTER_API_KEY;

// Bad: Never use build-time env vars
const key = process.env.REACT_APP_API_KEY;  // ❌ Gets bundled!
```

## Deployment Considerations

### Docker Example

```dockerfile
FROM node:18 AS frontend
WORKDIR /app
COPY frontend .
RUN npm install && npm run build

FROM python:3.11
WORKDIR /app
COPY backend .
RUN pip install -r requirements.txt
COPY --from=frontend /app/dist public/
ENV MASTER_API_KEY=production-secret-key
CMD ["python", "main.py"]
```

**The key advantage:** Change `config.json` per environment without rebuilding the frontend!

```json
# staging/config.json
{"BACKEND_URL": "https://staging-api.example.com", "MASTER_API_KEY": "staging-key"}

# production/config.json  
{"BACKEND_URL": "https://api.example.com", "MASTER_API_KEY": "prod-key"}
```

## Files Modified/Created

- `backend/main.py` - Added HTTPBearer authentication
- `frontend/src/config.ts` - Added MASTER_API_KEY to Config interface
- `frontend/src/App.tsx` - Added Authorization header to API calls
- `frontend/public/config.json` - Added MASTER_API_KEY
- `test_auth.py` - Demonstration script for testing authentication

## Summary

This implementation demonstrates the principle of **"Build Once, Deploy Many"** with authentication:

1. ✅ Backend reads secrets from **environment variables only**
2. ✅ Frontend reads secrets from **runtime configuration only**
3. ✅ All API calls include **Bearer token authentication**
4. ✅ Same build works with **different backends and API keys**
5. ✅ No secrets hardcoded anywhere in the code
