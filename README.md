# Build Once, Deploy Many 🚀

A minimal end-to-end example demonstrating runtime configuration for a React frontend with a FastAPI backend.

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (with npm)

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start the Backend

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000` by default.

To use a different port:

```bash
PORT=3000 python main.py
```

### 4. Start the Frontend (Development)

In a new terminal:

```bash
cd frontend
npm run dev
```

Open your browser to `http://localhost:5173`. You should see the backend message displayed.

## Project Structure

```
try-dynamic-react/
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt      # Python dependencies
│
└── frontend/
    ├── public/
    │   └── config.json      # RUNTIME config (NOT bundled)
    ├── src/
    │   ├── config.js        # Runtime config loader
    │   ├── App.jsx          # React component
    │   ├── main.jsx         # App bootstrap
    │   └── index.css        # Styles
    ├── package.json         # React dependencies
    ├── vite.config.js       # Vite configuration
    └── index.html           # HTML entry point
```

## Understanding Build vs Runtime

### Build Time (npm run build)

When you run `npm run build` in the frontend:

- React code is bundled into optimized JavaScript files
- Static assets are processed
- **`config.json` is NOT included in the build** ← Key point
- Output: A `dist/` folder ready for deployment

### Runtime

When the app loads in the browser:

1. Browser downloads `index.html` and JavaScript from `dist/`
2. JavaScript executes and fetches `/config.json` as a separate HTTP request
3. Configuration is loaded into memory
4. React renders using the loaded config

### Why No Rebuild?

```
Deploy to Environment A:     Deploy to Environment B:
├── dist/ (same React build) ├── dist/ (same React build)
└── config.json              └── config.json
    BACKEND_URL:                 BACKEND_URL:
    prod-api.example.com         staging-api.example.com
    ↓                            ↓
    React builds once,           React builds once,
    config loaded at runtime     config loaded at runtime
```

**The same React build works with different backend URLs by simply changing `config.json`.**

## Demonstration: Change Backend at Runtime

### Start Backend on Port 8000

```bash
cd backend
python main.py
# Backend runs on http://localhost:8000
```

### Build React

```bash
cd frontend
npm run build
# Creates dist/ folder with production build
```

### Serve Built Frontend

```bash
cd frontend
npm run preview
# Serves dist/ on http://localhost:4173
```

The app displays the backend URL from `config.json`.

### Change Backend URL WITHOUT Rebuilding

Edit `frontend/public/config.json`:

```json
{
  "BACKEND_URL": "http://api.example.com"
}
```

When serving the built app, the config is re-fetched and displays the new URL.

**Note:** In development (`npm run dev`), Vite serves from the source `public/` folder. In production, you'd serve both `dist/` and `config.json` from the same HTTP server or path.

## Key Files Explained

### [backend/main.py](backend/main.py)

- FastAPI server with CORS enabled
- Reads `PORT` from environment: `PORT=3000 python main.py`
- Exposes `GET /api/hello` endpoint

### [frontend/src/config.js](frontend/src/config.js)

**The critical piece for "build once, deploy many":**

- `loadConfig()`: Fetches `/config.json` at runtime (NOT build-time)
- `getConfig()`: Returns the loaded config for use in components
- No hardcoded URLs anywhere

### [frontend/src/main.jsx](frontend/src/main.jsx)

- Bootstrap sequence:
  1. Load config from `config.json`
  2. Then render React app
  3. Ensures config is ready before components render

### [frontend/public/config.json](frontend/public/config.json)

- Static file served from the web server
- **NOT bundled into React build**
- Can be replaced on any deployed environment

## How It's Different from process.env

### ❌ Traditional build-time env vars (process.env)

```javascript
// In React component
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
// ↑ Baked into the build at build time
// ↑ To change it, must rebuild React
```

Build 1: `REACT_APP_BACKEND_URL=prod npm run build`
Build 2: `REACT_APP_BACKEND_URL=staging npm run build`

**Result: 2 different builds, 2 deployments**

### ✅ Runtime config (this example)

```javascript
// In config.js
const config = await fetch('/config.json').then(r => r.json());
// ↑ Loaded at runtime
// ↑ No rebuild needed
```

Build 1: `npm run build` (once, for all environments)
Deploy 1: Point to `prod` by using prod's `config.json`
Deploy 2: Point to `staging` by using staging's `config.json`

**Result: 1 build, many deployments**

## Production Deployment Example

### Local Development

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

Visit `http://localhost:5173`

### Production-like Setup

```bash
# Build frontend once
cd frontend && npm run build

# Copy dist/ and config.json to your server
# /app/
# ├── dist/           (React build)
# └── config.json     (Runtime config)

# Serve with any static file server
cd frontend && npm run preview
```

Visit `http://localhost:4173`, confirm it loads the backend response.

### Change Configuration Without Rebuilding

Edit `frontend/public/config.json`:

```json
{
  "BACKEND_URL": "http://production-api.example.com"
}
```

Restart your web server (or just replace the file on disk). The app immediately uses the new config.

## Key Takeaways

1. **Build Once:** React is compiled once with `npm run build`
2. **Deploy Many:** The same build works with any backend by changing `config.json`
3. **No process.env:** No build-time environment variables
4. **Runtime Loading:** Configuration loaded when the app starts
5. **Static File:** `config.json` is served as a static file, not bundled

## Extending This Example

To add more configuration values:

### Update [frontend/public/config.json](frontend/public/config.json)

```json
{
  "BACKEND_URL": "http://localhost:8000",
  "API_KEY": "abc123",
  "FEATURE_FLAG": true
}
```

### Use in [frontend/src/App.jsx](frontend/src/App.jsx)

```javascript
const config = getConfig();
const backendUrl = config.BACKEND_URL;
const apiKey = config.API_KEY;
const featureEnabled = config.FEATURE_FLAG;
```

## Files Not Included (By Design)

- No authentication/secrets
- No advanced error handling
- No state management (Redux, Zustand, etc.)
- No deployment orchestration (Docker, Kubernetes, etc.)

This is a minimal, focused example to demonstrate the pattern clearly.
