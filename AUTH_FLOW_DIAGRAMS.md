# HTTP Bearer Authentication - Visual Guide

## Request Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND (React TypeScript)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  1. Load Runtime Config                                                      │
│     ┌─────────────────────┐                                                  │
│     │ config.json (public)|                                                  │
│     │ - BACKEND_URL       │                                                  │
│     │ - MASTER_API_KEY    │                                                  │
│     └──────────┬──────────┘                                                  │
│                │ (loaded at startup)                                         │
│                ▼                                                              │
│     ┌─────────────────────────────────────┐                                 │
│     │ config.ts                           │                                 │
│     │ - loadConfig()                      │                                 │
│     │ - getConfig()                       │                                 │
│     │ - Config interface with MASTER_API_KEY │                              │
│     └──────────┬──────────────────────────┘                                 │
│                │                                                              │
│                ▼                                                              │
│     ┌──────────────────────────────────────────────┐                       │
│     │ App.tsx                                      │                       │
│     │ const config = getConfig()                   │                       │
│     │ fetch('/api/hello', {                        │                       │
│     │   headers: {                                 │                       │
│     │     'Authorization':                         │                       │
│     │       `Bearer ${config.MASTER_API_KEY}`      │                       │
│     │   }                                          │                       │
│     │ })                                           │                       │
│     └──────────┬───────────────────────────────────┘                       │
│                │                                                              │
│                │ HTTP Request with Bearer Token                             │
│                │ Authorization: Bearer super-secret-key                     │
│                ▼                                                              │
└────────────────┼──────────────────────────────────────────────────────────────┘
                 │
                 │ (Internet / Network)
                 │
┌────────────────┼──────────────────────────────────────────────────────────────┐
│                ▼                                                              │
│           ┌─────────────────────────────────────────┐                       │
│           │ FastAPI Backend (main.py)               │                       │
│           │                                         │                       │
│           │ HTTPBearer Security                     │                       │
│           │ - security = HTTPBearer()               │                       │
│           └────────────┬────────────────────────────┘                       │
│                        │                                                     │
│                        ▼                                                     │
│          ┌──────────────────────────────────┐                              │
│          │ verify_token() Dependency        │                              │
│          │                                  │                              │
│          │ 1. Extract token from header     │                              │
│          │ 2. Compare to MASTER_API_KEY     │                              │
│          │    (from environment variable)   │                              │
│          │ 3. Return token or raise 401     │                              │
│          └────────────┬─────────────────────┘                              │
│                       │                                                      │
│        ┌──────────────┴──────────────┐                                      │
│        │                             │                                      │
│        ▼                             ▼                                      │
│   ✅ VALID TOKEN            ❌ INVALID/MISSING                            │
│   │                          │                                             │
│   ▼                          ▼                                             │
│  ┌─────────────────────┐  ┌──────────────────────┐                       │
│  │ @app.get("/api/")   │  │ HTTPException(401)   │                       │
│  │ def hello(token):   │  │ "Invalid token"      │                       │
│  │   return {          │  │                      │                       │
│  │     "message": ..., │  │ Response to client:  │                       │
│  │     "authenticated" │  │ HTTP 401 Unauthorized│                       │
│  │   }                 │  │                      │                       │
│  └─────────────────────┘  └──────────────────────┘                       │
│        │                          │                                       │
│        └──────────┬───────────────┘                                       │
│                   │                                                        │
│                   │ HTTP Response                                         │
│                   ▼                                                        │
└────────────────┼──────────────────────────────────────────────────────────────┘
                 │
                 │ (Internet / Network)
                 │
┌────────────────┼──────────────────────────────────────────────────────────────┐
│                ▼                                                              │
│          ┌──────────────────────────────────┐                              │
│          │ Frontend receives response       │                              │
│          │ - 200 OK + message               │                              │
│          │ - 401 Unauthorized (error)       │                              │
│          └──────────────┬───────────────────┘                              │
│                         │                                                   │
│                         ▼                                                   │
│          ┌─────────────────────────────────────┐                          │
│          │ Display to user                     │                          │
│          │ ✅ Message from backend: ...        │                          │
│          │ or                                  │                          │
│          │ ❌ Error: Invalid or expired token  │                          │
│          └─────────────────────────────────────┘                          │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow: Secrets Management

```
Environment Setup (Development/Production):
┌──────────────────────────────────┐
│ $ export MASTER_API_KEY=secret   │
│ $ python backend/main.py         │
└──────────────┬───────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ backend/main.py                     │
│ MASTER_API_KEY = os.environ.get(...) │  ← Read from environment only
└──────────────┬──────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ FastAPI verify_token() dependency       │
│ Compares incoming token to MASTER_API_KEY│
└──────────────────────────────────────────┘

Frontend Configuration:
┌──────────────────────────────────────────┐
│ frontend/public/config.json              │
│ {                                        │
│   "MASTER_API_KEY": "super-secret-key"  │
│ }                                        │
│                                          │
│ ✅ Loaded at runtime                    │
│ ✅ NOT bundled in build                 │
│ ✅ Can change without rebuild           │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│ App.tsx                                  │
│ config = getConfig()                     │
│ fetch(url, {                             │
│   headers: {                             │
│     Authorization: Bearer <API_KEY>      │
│   }                                      │
│ })                                       │
└──────────────────────────────────────────┘
```

## Testing Scenarios

### Scenario 1: No Authorization Header

```
Request:
GET /api/hello HTTP/1.1
Host: localhost:8000

Response:
HTTP/1.1 403 Forbidden
Content-Type: application/json

{"detail":"Not authenticated"}
```

### Scenario 2: Invalid Token

```
Request:
GET /api/hello HTTP/1.1
Host: localhost:8000
Authorization: Bearer wrong-token

Response:
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"detail":"Invalid or expired token"}
```

### Scenario 3: Valid Token

```
Request:
GET /api/hello HTTP/1.1
Host: localhost:8000
Authorization: Bearer super-secret-key

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{"message":"hello from backend","authenticated":true}
```

## Security Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Layer 1: Environment Variables (Backend Only)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ MASTER_API_KEY is NEVER in code or config files    │  │
│  │ Backend reads: os.environ.get("MASTER_API_KEY")    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  Layer 2: Runtime Configuration (Frontend)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ config.json is loaded at app startup               │  │
│  │ NOT bundled into React build                       │  │
│  │ Can be changed per environment                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  Layer 3: Bearer Token Authentication                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ All /api/* endpoints protected                     │  │
│  │ Requires: Authorization: Bearer <TOKEN>           │  │
│  │ Invalid token → 401 Unauthorized                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  Layer 4: HTTPS in Production                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ All communication should be encrypted               │  │
│  │ Protects token from network interception           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Pattern

```
Development:
  Environment: MASTER_API_KEY=dev-key
  config.json: BACKEND_URL=http://localhost:8000
  
Staging:
  Environment: MASTER_API_KEY=staging-key
  config.json: BACKEND_URL=https://staging-api.example.com
  
Production:
  Environment: MASTER_API_KEY=prod-key
  config.json: BACKEND_URL=https://api.example.com

⭐ KEY ADVANTAGE: Same React build for all environments!
   Only change the environment variable and config.json
   No need to rebuild React
```
