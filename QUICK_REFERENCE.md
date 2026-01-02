# Build Once, Deploy Many - Quick Reference

## What Is This?

A minimal, production-ready pattern for deploying React apps to multiple environments **without rebuilding**.

Traditional approach: Build per environment
```
Build (prod) → Deploy (prod)
Build (staging) → Deploy (staging)
Build (dev) → Deploy (dev)
```

This approach: Build once, deploy everywhere
```
Build (once) → Deploy (prod)
             → Deploy (staging)
             → Deploy (dev)
```

## Core Principle

```
❌ DON'T:  const API = process.env.REACT_APP_API  // Build-time injection
✅ DO:     const API = (await fetch('/config.json')).BACKEND_URL  // Runtime fetch
```

## Project Structure

```
try-dynamic-react/
│
├── backend/
│   ├── main.py               ← FastAPI server (reads PORT from env)
│   └── requirements.txt       ← Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── config.js         ← ⭐ Runtime config loader
│   │   ├── App.jsx           ← React component using config
│   │   ├── main.jsx          ← Bootstrap (load config first)
│   │   └── index.css         ← Styles
│   │
│   ├── public/
│   │   └── config.json       ← ⭐ NOT bundled with React build
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── README.md                 ← Setup and usage
├── ARCHITECTURE.md           ← Deep dive on how it works
├── TESTING.md                ← Demo scenarios
└── setup.sh                  ← One-command setup
```

## The Magic: config.js

```javascript
// ⭐ Load config from /config.json (NOT from build)
export async function loadConfig() {
  const response = await fetch('/config.json');
  return await response.json();  // { BACKEND_URL: "..." }
}

// Use it anywhere in React
export function getConfig() {
  return config;
}
```

## The Flow

```
1. Browser opens app
   ↓
2. index.html loads
   <script src="/src/main.jsx"></script>
   ↓
3. main.jsx runs:
   await loadConfig()  // ← Fetch /config.json from server
   ReactDOM.render(<App />)
   ↓
4. App component gets config:
   const config = getConfig()
   fetch(`${config.BACKEND_URL}/api/hello`)
   ↓
5. Display response
```

## Quick Start

```bash
# One-time setup
bash setup.sh

# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Test
curl http://localhost:8000/api/hello

# Browser
http://localhost:5173
```

## Demonstrating "Build Once, Deploy Many"

### Scenario 1: Change Backend URL

**Without rebuilding:**

```bash
# Change frontend/public/config.json
{
  "BACKEND_URL": "http://new-api.example.com"  # Change this
}

# Reload browser
# ✅ App now uses new backend
```

### Scenario 2: Production Build for 3 Environments

```bash
# Build once
cd frontend && npm run build

# Deploy to Staging
copy dist/ → staging-server/
create config.json with staging-api-url

# Deploy to Production  
copy dist/ → production-server/
create config.json with prod-api-url

# Deploy to Development
copy dist/ → dev-server/
create config.json with dev-api-url

# All use the same React build! ✅
```

### Scenario 3: Extend with More Values

```json
{
  "BACKEND_URL": "http://localhost:8000",
  "FEATURE_FLAGS": { "betaUI": true },
  "API_TIMEOUT": 5000,
  "LOG_LEVEL": "debug"
}
```

## File Storage

### React Build (`dist/`)
```
dist/
├── index.html
├── assets/
│   └── main-abc123.js  (NO environment values)
```

### Deployment Folder
```
/var/www/app/
├── dist/               (React build)
├── config.json         (Runtime config)  ← Changed per environment
└── server.conf         (Web server config)
```

## Backend (for reference)

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
def hello():
    return {"message": "hello from backend"}

# Read port from environment
port = int(os.environ.get("PORT", 8000))
# Usage: PORT=3000 python main.py
```

## Why Not process.env?

### Problem with process.env (Build-time)

```javascript
// .env
REACT_APP_API=https://prod-api.com

// After build, JavaScript contains:
const API = "https://prod-api.com";  // Hardcoded! Cannot change!
```

To use different API for staging:
```bash
REACT_APP_API=https://staging-api.com npm run build  # Build again! ❌
```

### Solution with Runtime Config

```javascript
// config.json
{ "BACKEND_URL": "https://prod-api.com" }

// After build, JavaScript contains:
const config = await fetch('/config.json');
const API = config.BACKEND_URL;  // Loaded at runtime ✅
```

To use different API for staging:
```bash
# Just change config.json
{ "BACKEND_URL": "https://staging-api.com" }
# No rebuild! ✅
```

## Key Insights

| Item | Details |
|------|---------|
| **Build Time** | React compiled once, no env values baked in |
| **Runtime** | App fetches config.json and uses it |
| **Deployment** | Copy same React build to multiple servers |
| **Configuration** | Each server has its own config.json |
| **Rebuild** | Only needed when React code changes |
| **Config** | Can be changed anytime without rebuild |

## Next Steps

1. Read [README.md](README.md) for full setup
2. Check [TESTING.md](TESTING.md) for demo scenarios
3. Review [ARCHITECTURE.md](ARCHITECTURE.md) for deep dive
4. Modify `frontend/public/config.json` and reload to see it work
5. Build with `npm run build` and serve to test production setup

## Extending This Pattern

For production use, consider:

- **Validation:** Validate config.json schema at runtime
- **Caching:** Cache config in localStorage with TTL
- **Versioning:** Version your config.json
- **Secrets:** Keep secrets in backend environment, not config.json
- **Rollback:** Revert by restoring old config.json
- **Monitoring:** Log config changes in observability tools

## No Secrets Here! 🔒

This example uses non-sensitive config only. For secrets:
- Keep them on the backend
- Backend reads from environment variables
- Frontend calls backend API, backend uses secrets
- Frontend never sees secrets directly

This example demonstrates the pattern with public, non-sensitive data.

---

**Status:** Ready to run! Just follow "Quick Start" above.

**Remember:** Build once (React), deploy many (config per environment). 🚀
