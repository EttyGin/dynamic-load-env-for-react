# Quick Start: HTTP Bearer Authentication

## 30 Second Setup

### Terminal 1: Backend
```bash
cd backend
pip install -r requirements.txt
MASTER_API_KEY=super-secret-key python main.py
```

### Terminal 2: Frontend
```bash
cd frontend
npm install
npm run dev
```

### Terminal 3: Test (optional)
```bash
pip install requests
python test_auth.py
```

## What Changed?

### Backend (`backend/main.py`)
- ✅ Reads `MASTER_API_KEY` from environment variable
- ✅ Uses `HTTPBearer` from FastAPI security
- ✅ `verify_token()` dependency protects `/api/*` endpoints
- ✅ Returns 401 if token missing or invalid

### Frontend (`frontend/src/`)
- ✅ `config.ts`: Added `MASTER_API_KEY` to Config interface
- ✅ `App.tsx`: Sends `Authorization: Bearer <KEY>` header
- ✅ `config.json`: Contains the API key (loaded at runtime)

## Testing

### With cURL
```bash
# Fails - no token
curl http://localhost:8000/api/hello

# Fails - wrong token  
curl -H "Authorization: Bearer wrong" http://localhost:8000/api/hello

# Works - correct token
curl -H "Authorization: Bearer super-secret-key" http://localhost:8000/api/hello
```

### With Python Script
```bash
python test_auth.py
```

## Key Principles

1. **Never Hardcode Secrets**
   - Backend: Read from `os.environ`
   - Frontend: Read from `config.json`

2. **Runtime Configuration**
   - `config.json` is NOT bundled
   - Loaded at app startup
   - Can change without rebuild

3. **Bearer Authentication**
   - Include: `Authorization: Bearer <token>`
   - All `/api/*` endpoints protected
   - Returns 401 if invalid

## Production Deployment

Change `config.json` per environment:

```bash
# Development
MASTER_API_KEY=dev-secret-key python backend/main.py

# Staging
MASTER_API_KEY=staging-secret-key python backend/main.py

# Production  
MASTER_API_KEY=production-secret-key python backend/main.py
```

Then update `config.json` on the frontend:
```json
{
    "BACKEND_URL": "https://api.prod.example.com",
    "MASTER_API_KEY": "production-secret-key"
}
```

**Same React build, different backends & API keys!**

---

See `AUTH_IMPLEMENTATION.md` for detailed documentation.
