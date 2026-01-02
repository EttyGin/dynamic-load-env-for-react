# Visual Workflow Diagram

## End-to-End Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER OPENS BROWSER                           │
│                 http://localhost:5173                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             v
                ┌────────────────────────────┐
                │  Browser Downloads HTML    │
                │  <script>main.jsx</script> │
                └────────────────┬───────────┘
                                 │
                                 v
        ┌────────────────────────────────────────────┐
        │ main.jsx starts:                           │
        │ 1. Calls loadConfig()                      │
        │ 2. Fetches /config.json from server        │
        └────────────────────┬───────────────────────┘
                             │
                ┌────────────v──────────────┐
                │ /config.json (Response)   │
                │ {                         │
                │  "BACKEND_URL":           │
                │  "http://localhost:8000"  │
                │ }                         │
                └────────────┬──────────────┘
                             │
        ┌────────────────────v─────────────────────┐
        │ Config Stored in Memory                  │
        │ ReactDOM.render(<App />)                 │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────v─────────────────────┐
        │ App Component Renders                    │
        │ const config = getConfig()               │
        │ fetch(                                   │
        │   `${config.BACKEND_URL}/api/hello`     │
        │ )                                        │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────v──────────────────────────┐
        │ GET http://localhost:8000/api/hello          │
        │ (Request to FastAPI Backend)                 │
        └────────────────────┬──────────────────────────┘
                             │
        ┌────────────────────v──────────────────────────┐
        │ Backend Response:                             │
        │ {                                            │
        │   "message": "hello from backend"            │
        │ }                                            │
        └────────────────────┬──────────────────────────┘
                             │
        ┌────────────────────v──────────────────────────┐
        │ App Renders:                                 │
        │ ✅ Message from backend: hello from backend  │
        │ Backend URL: http://localhost:8000           │
        └──────────────────────────────────────────────┘
```

## Build Time vs Runtime

```
┌──────────────────────────────────────────────────────────────────┐
│                         DEVELOPMENT                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  npm run dev                                                     │
│       │                                                          │
│       ├─ Vite Dev Server on :5173                               │
│       │   ├─ Serves index.html                                  │
│       │   ├─ Transforms JSX on-the-fly                          │
│       │   └─ Serves public/config.json as-is                    │
│       │                                                          │
│       └─ Fast reload on code change (HMR)                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      PRODUCTION BUILD                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  npm run build                                                   │
│       │                                                          │
│       v                                                          │
│  ┌──────────────────────┐                                       │
│  │ Vite Build Process   │                                       │
│  ├──────────────────────┤                                       │
│  │ ✅ Compile JSX       │                                       │
│  │ ✅ Bundle code       │                                       │
│  │ ✅ Minify JS/CSS     │                                       │
│  │ ✅ Optimize assets   │                                       │
│  │ ❌ DON'T include     │                                       │
│  │    config.json       │ ← KEY!                                │
│  └──────────────────────┘                                       │
│       │                                                          │
│       v                                                          │
│  ┌──────────────────────┐                                       │
│  │ Output: dist/        │                                       │
│  ├──────────────────────┤                                       │
│  │ index.html           │                                       │
│  │ assets/              │                                       │
│  │  └─ main-[hash].js   │ (NO environment values)              │
│  │ (NO config.json)     │                                       │
│  └──────────────────────┘                                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                       DEPLOYMENT                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Copy to Server:                                                │
│                                                                  │
│  /var/www/app/                                                  │
│  ├─ dist/              (from build output)                      │
│  │  ├─ index.html                                              │
│  │  └─ assets/main-[hash].js                                   │
│  │                                                              │
│  └─ config.json        (created/updated per environment)        │
│     { "BACKEND_URL": "..." }                                    │
│                                                                  │
│  Serve both with web server (nginx, apache, etc)               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Runtime Configuration Handling

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEFORE APP STARTS                            │
│                    (Application Loading)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  index.html loads → main.jsx starts → loadConfig() executes    │
│                                                                 │
│  While this happens, React rendering is BLOCKED               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                FETCH /config.json                               │
│                                                                 │
│  const response = await fetch('/config.json')                  │
│  const config = await response.json()                          │
│                                                                 │
│  ← This is an HTTP request to the web server                   │
│  ← NOT read from the JavaScript bundle                         │
│  ← Can be updated without rebuilding React                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│              STORE CONFIG IN MEMORY                             │
│                                                                 │
│  Global variable `config` now contains:                        │
│  {                                                              │
│    BACKEND_URL: "http://localhost:8000",                       │
│    ... other values ...                                        │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│           RENDER REACT APP                                      │
│                                                                 │
│  Now React components can call getConfig()                     │
│  and access BACKEND_URL                                        │
│                                                                 │
│  ReactDOM.createRoot().render(<App />)                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Comparison: Traditional vs Runtime Config

```
TRADITIONAL (process.env - Build-time Injection)
═══════════════════════════════════════════════

Build #1: REACT_APP_API=prod npm run build
          ↓
          JavaScript contains: const API = "prod-api.com"
          ↓
          Deploy to Production

Build #2: REACT_APP_API=staging npm run build
          ↓
          JavaScript contains: const API = "staging-api.com"
          ↓
          Deploy to Staging

Problem: Need separate builds for each environment
Result: N environments = N builds = N deployments


RUNTIME CONFIG (This Example)
════════════════════════════

npm run build (ONCE)
          ↓
          JavaScript contains: const API = await fetch('/config.json')
          ↓
          ┌──────────────────────┬──────────────────────┐
          │                      │                      │
          v                      v                      v
      Deploy to             Deploy to             Deploy to
      Production            Staging               Dev
      
      +                     +                     +
      
      config.json:          config.json:          config.json:
      prod-api.com          staging-api.com       localhost:8000

Benefit: Single build serves all environments
Result: 1 build = ∞ deployments with different configs
```

## Configuration Lifecycle

```
TIME AXIS ➜

User Opens Browser
│
├─ T0: Download HTML/JS (no config yet)
│
├─ T1: JavaScript starts executing
│       └─ loadConfig() begins
│
├─ T2: fetch('/config.json') in flight
│
├─ T3: config.json arrives
│       └─ Store in memory
│       └─ config variable is now populated
│
├─ T4: React rendering unblocked
│       └─ Components can now call getConfig()
│
└─ T5: User sees UI with data from config.BACKEND_URL
        └─ If config changes, just reload browser
        └─ No rebuild needed!

     ↑
     └─── ALL OF THIS HAPPENS DYNAMICALLY AT RUNTIME
         NO BUILD STEP INVOLVED
```

## Code Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ Browser opens http://localhost:5173                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────v────────────────┐
        │ HTML <script src="/src/main.jsx">│
        │ loads and starts                 │
        └─────────────────┬────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ main.jsx (src/main.jsx) executes:       │
        │                                          │
        │ async function startApp() {             │
        │   await loadConfig()  ← WAITS HERE     │
        │   ReactDOM.render(<App />)  ← THEN    │
        │ }                                        │
        │                                          │
        │ startApp()                               │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ config.js loadConfig() function:        │
        │                                          │
        │ export async function loadConfig() {    │
        │   const response = await              │
        │     fetch('/config.json')              │
        │   config = await response.json()       │
        │   return config                        │
        │ }                                        │
        │                                          │
        │ Fetches: /config.json                   │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ Web Server Response:                    │
        │                                          │
        │ Content-Type: application/json          │
        │ {                                        │
        │   "BACKEND_URL":                        │
        │   "http://localhost:8000"               │
        │ }                                        │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ Back in startApp():                     │
        │                                          │
        │ Config is loaded ✓                      │
        │ Now render React                        │
        │ ReactDOM.render(<App />)               │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ App.jsx Component renders:              │
        │                                          │
        │ function App() {                        │
        │   const config = getConfig()  ✓        │
        │   const url = config.BACKEND_URL       │
        │   fetch(`${url}/api/hello`)            │
        │   return <div>...</div>                │
        │ }                                        │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ Backend Request:                        │
        │ GET /api/hello                          │
        │ Host: localhost:8000                    │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ Backend Response:                       │
        │ {                                        │
        │   "message": "hello from backend"       │
        │ }                                        │
        └─────────────────┬───────────────────────┘
                          │
        ┌─────────────────v───────────────────────┐
        │ UI Rendered:                            │
        │ ✅ Hello from backend                   │
        │ Backend URL: http://localhost:8000      │
        └──────────────────────────────────────────┘
```

## Deployment Architecture

```
    ┌─────────────────────────────────────────────────────────┐
    │              SINGLE BUILD ARTIFACT                      │
    ├─────────────────────────────────────────────────────────┤
    │ dist/                                                   │
    │ ├─ index.html                                          │
    │ └─ assets/main-abc123def456.js                         │
    │                                                         │
    │ (Created once: npm run build)                          │
    │ (No environment-specific values baked in)              │
    └─────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         v               v               v

    PRODUCTION      STAGING         DEVELOPMENT
    ┌──────────┐   ┌──────────┐    ┌──────────┐
    │  dist/   │   │  dist/   │    │  dist/   │
    │(same)    │   │(same)    │    │(same)    │
    ├──────────┤   ├──────────┤    ├──────────┤
    │config.json   │config.json   │config.json
    │BACKEND_URL:  │BACKEND_URL:  │BACKEND_URL:
    │prod-api.com  │staging-api   │localhost:
    │              │.example.com  │8000
    └──────────┘   └──────────┘    └──────────┘
         │               │               │
         └───────────────┴───────────────┘
                    ↓
            Same React build
            Different configs
            Different backends
```

---

**Key Takeaway:** React is built once and deployed everywhere.
Configuration is loaded at runtime from a static file, not bundled.
