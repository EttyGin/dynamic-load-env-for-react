# Architecture Overview

## How "Build Once, Deploy Many" Works

### Traditional Approach (Requires Rebuild)

```
Environment: PRODUCTION          Environment: STAGING
┌─────────────────────┐         ┌─────────────────────┐
│ npm run build       │         │ npm run build       │
│ (with env vars)     │         │ (with env vars)     │
└──────────┬──────────┘         └──────────┬──────────┘
           │                              │
    Build 1: prod-api.com        Build 2: staging-api.com
           │                              │
           v                              v
    ┌────────────┐                ┌────────────┐
    │ React      │                │ React      │
    │ build #1   │                │ build #2   │
    │ (hardcoded)│                │ (hardcoded)│
    │ prod API   │                │ staging API│
    └────────────┘                └────────────┘

Problem: Two different builds for two environments
```

### This Example's Approach (Build Once, Deploy Many)

```
                   npm run build (ONCE)
                          │
                          v
                   ┌────────────────┐
                   │  React Build   │
                   │  (no hardcoded │
                   │   env values)  │
                   └────────┬───────┘
                            │
         ┌──────────────────┴──────────────────┐
         │                                    │
         v                                    v
┌─────────────────────────┐      ┌─────────────────────────┐
│ PRODUCTION Environment  │      │ STAGING Environment     │
│                         │      │                         │
│ Same React build        │      │ Same React build        │
│ + config.json:          │      │ + config.json:          │
│   BACKEND_URL:          │      │   BACKEND_URL:          │
│   prod-api.com          │      │   staging-api.com       │
│                         │      │                         │
│ ↓ (at runtime)          │      │ ↓ (at runtime)          │
│ Fetch /config.json      │      │ Fetch /config.json      │
│ Get prod URL            │      │ Get staging URL         │
└─────────────────────────┘      └─────────────────────────┘

Benefit: Same build, different environments, no rebuild
```

## File Serving Architecture

### Development Mode (npm run dev)

```
Browser Request              Vite Dev Server
    │                              │
    ├─ GET /                       │
    │  ───────────────────────────>│ Serves index.html
    │                              │
    ├─ GET /src/main.jsx           │
    │  ───────────────────────────>│ Serves transformed JSX
    │                              │
    ├─ GET /config.json            │
    │  ───────────────────────────>│ Serves from public/
    │                              │
    └─ GET /api/hello              │
       ───────────────────────────>│ Proxy to backend
                                   │ (or backend runs separately)
```

### Production Mode (npm run build + serve)

```
Browser Request              Static File Server
    │                              │
    ├─ GET /                       │
    │  ───────────────────────────>│ Serves index.html
    │                              │ from dist/
    │                              │
    ├─ GET /assets/main-[hash].js  │
    │  ───────────────────────────>│ Serves from dist/assets/
    │                              │
    ├─ GET /config.json            │
    │  ───────────────────────────>│ Serves from root or
    │                              │ public/ directory
    │                              │
    └─ GET /api/hello              │
       ───────────────────────────>│ Proxy to backend
                                   │ (configured in nginx/server)
```

## Runtime Config Loading Sequence

```
1. User opens http://localhost:5173
                       │
                       v
2. Browser downloads index.html
   <script type="module" src="/src/main.jsx"></script>
                       │
                       v
3. main.jsx starts
   await loadConfig()
                       │
                       v
4. config.js fetches /config.json
   Response: { "BACKEND_URL": "http://localhost:8000" }
                       │
                       v
5. Config stored in memory
                       │
                       v
6. ReactDOM.createRoot(document.getElementById('root')).render(<App />)
   App component can now call getConfig()
                       │
                       v
7. App.jsx calls getConfig() and fetches /api/hello
   fetch(`${config.BACKEND_URL}/api/hello`)
                       │
                       v
8. Display backend response in UI
```

## Key Insight: Where Build Ends, Runtime Begins

```
REACT BUILD (One Time)
├─ Compile JSX to JavaScript
├─ Bundle and minify
├─ Generate dist/ folder
├─ Include: Components, hooks, utilities
└─ DO NOT include: config.json ← Critical!

                    ↓ (Deploy dist/ folder)

RUNTIME (Every Time App Starts)
├─ Browser loads index.html
├─ JavaScript executes
├─ JavaScript fetches /config.json (HTTP request!)
├─ Configuration injected into React
└─ UI renders using runtime config
```

## Why process.env Doesn't Work

### With process.env (Build-time)

```javascript
// .env.production
REACT_APP_BACKEND_URL=prod-api.com

// In React component
const url = process.env.REACT_APP_BACKEND_URL;

// During build:
// process.env.REACT_APP_BACKEND_URL gets replaced with "prod-api.com"
// This substitution is permanent in the final JavaScript file
```

After build, the JavaScript contains:

```javascript
const url = "prod-api.com";  // Hardcoded!
```

You cannot change this without rebuilding.

### With Runtime Config (This Approach)

```javascript
// frontend/public/config.json
{
  "BACKEND_URL": "prod-api.com"
}

// In React component
const config = await fetch('/config.json').then(r => r.json());
const url = config.BACKEND_URL;  // Dynamic!
```

After build, the JavaScript contains:

```javascript
const config = await fetch('/config.json');
const url = config.BACKEND_URL;  // Fetched at runtime!
```

You CAN change config.json anytime without rebuilding.

## Deployment Scenarios

### Scenario 1: Change Backend URL

**Before:** `config.json` points to `http://staging-api.example.com`
**Action:** Edit `config.json` to `http://prod-api.example.com`
**Result:** Reload browser → Uses prod API
**Rebuild needed?** NO

### Scenario 2: Add New Config Value

**Add to config.json:**
```json
{
  "BACKEND_URL": "http://localhost:8000",
  "FEATURE_FLAGS": { "newUI": true }
}
```

**Update React to use it:**
```javascript
const config = getConfig();
if (config.FEATURE_FLAGS.newUI) {
  // Use new UI
}
```

**Rebuild needed?** YES (only because React code changed)

### Scenario 3: Scale to Multiple Regions

```
North America:               Europe:                 Asia:
┌──────────────────┐        ┌──────────────────┐    ┌──────────────────┐
│ Same React build │        │ Same React build │    │ Same React build │
│ + config.json:   │        │ + config.json:   │    │ + config.json:   │
│  na-api.example. │        │  eu-api.example. │    │  asia-api.       │
│  com             │        │  com             │    │  example.com     │
└──────────────────┘        └──────────────────┘    └──────────────────┘

One React build works globally, configured per region.
```

## Security Note

For this minimal example, we've kept it simple. In production:

- Don't put secrets in `config.json`
- If config contains sensitive values, serve it securely (HTTPS)
- Consider signing/validating config to prevent tampering
- Use environment variables on the backend (as shown in this example)

The key is: **Frontend uses runtime config for non-sensitive values**
**Backend uses environment variables for sensitive values**
