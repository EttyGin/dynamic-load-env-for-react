# Testing and Demo Guide

This guide walks through demonstrating the "Build Once, Deploy Many" pattern.

## Prerequisites

Run the setup script first:

```bash
bash setup.sh
```

## Demo 1: Basic Development Setup

### Terminal 1: Start Backend

```bash
cd backend
python main.py
```

Expected output:

```
Backend running on port 8000
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

Expected output:

```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Terminal 3: Test Backend Directly

```bash
curl http://localhost:8000/api/hello
```

Expected response:

```json
{"message":"hello from backend"}
```

### Open Browser

Visit `http://localhost:5173`

You should see:
- ✅ "Build Once, Deploy Many" heading
- ✅ Runtime Configuration section showing `http://localhost:8000`
- ✅ "hello from backend" message displayed

---

## Demo 2: Runtime Configuration Change (No Rebuild!)

With the app running in your browser:

### Step 1: Change config.json

Edit `frontend/public/config.json`:

**From:**
```json
{
  "BACKEND_URL": "http://localhost:8000"
}
```

**To:**
```json
{
  "BACKEND_URL": "http://localhost:9000"
}
```

### Step 2: Reload Browser

Refresh the page in your browser (F5 or Cmd+R).

### Expected Result

The app will now show:
- ✅ Backend URL: `http://localhost:9000`
- ❌ Error message (because backend isn't on 9000)

**Key observation:** We changed the backend URL WITHOUT rebuilding React!

### Step 3: Restore and Verify

Change `config.json` back to:
```json
{
  "BACKEND_URL": "http://localhost:8000"
}
```

Reload the browser. The message reappears. ✅

---

## Demo 3: Production Build

### Step 1: Build React (One Time)

```bash
cd frontend
npm run build
```

Expected output:

```
✓ 527 modules transformed.
dist/index.html                    0.46 kB │ gzip:  0.31 kB
dist/assets/main-[hash].js         X.XX kB │ gzip:  Y.YY kB

✓ built in XXXms
```

### Step 2: Verify config.json is NOT in the build

```bash
# Check what's in the built React bundle
ls -la frontend/dist/
```

You'll see:
- `index.html`
- `assets/` folder with JavaScript files
- **NO config.json** ← This is external!

### Step 3: Run Production Build

```bash
cd frontend
npm run preview
```

Expected output:

```
  ➜  Local:   http://localhost:4173/
```

### Step 4: Open and Verify

Visit `http://localhost:4173`

You should see the same working app. ✅

### Step 5: Demonstrate Config Change (Still No Rebuild!)

Edit `frontend/public/config.json` again and reload the browser. It works! ✅

**This proves:** The React build (`dist/`) doesn't contain the config. It's loaded separately at runtime.

---

## Demo 4: Backend on Different Port

### Change Backend Port

Stop the backend (Ctrl+C) and restart on a different port:

```bash
PORT=3000 python main.py
```

Output:

```
Backend running on port 3000
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

### Update Config

Edit `frontend/public/config.json`:

```json
{
  "BACKEND_URL": "http://localhost:3000"
}
```

### Reload App (Without Rebuilding)

Refresh your browser. It works with the new backend port! ✅

**No React rebuild needed** – just config change.

---

## Demo 5: Multiple Deployments with Same Build

### Simulate Production Setup

#### Build Once (for all environments)

```bash
cd frontend
npm run build
```

This produces a `dist/` folder that works for ANY backend URL.

#### Deployment 1: Staging Environment

1. Copy `dist/` to your staging server
2. Create `config.json` with:
   ```json
   {
     "BACKEND_URL": "http://staging-api.example.com"
   }
```
3. Serve both files

#### Deployment 2: Production Environment

1. Copy the same `dist/` to your production server
2. Create `config.json` with:
   ```json
   {
     "BACKEND_URL": "http://prod-api.example.com"
   }
```
3. Serve both files

**Result:** Same React build, different backends, no rebuild! ✅

---

## Demo 6: Add More Config Values

### Extend config.json

Edit `frontend/public/config.json`:

```json
{
  "BACKEND_URL": "http://localhost:8000",
  "API_TIMEOUT": 5000,
  "FEATURE_ENABLE_BETA": false,
  "LOG_LEVEL": "info"
}
```

### Check Browser Console

With the app running, open DevTools (F12) and check the console:

```javascript
// In DevTools console:
import { getConfig } from '/src/config.js'
getConfig()
// Returns: {BACKEND_URL: '...', API_TIMEOUT: 5000, FEATURE_ENABLE_BETA: false, LOG_LEVEL: 'info'}
```

---

## Troubleshooting

### App shows "Failed to load configuration"

**Cause:** `config.json` not found

**Fix:** Ensure `frontend/public/config.json` exists with valid JSON

### Backend returns "Connection refused"

**Cause:** Backend not running

**Fix:** Start backend with `python main.py` (or `PORT=X python main.py`)

### Frontend shows old config after editing

**Cause:** Browser cached the old config.json

**Fix:** 
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Open DevTools → Network → Disable cache

### CORS error

**Cause:** Backend and frontend on different origins

**Fix:** Backend already has CORS enabled. If error persists:
1. Check backend console for CORS middleware logs
2. Verify backend is actually running
3. Try accessing backend directly: `curl http://localhost:8000/api/hello`

---

## Summary of Key Concepts

| Aspect | Before (Traditional) | After (This Example) |
|--------|---------------------|----------------------|
| Build command | `npm run build` (per env) | `npm run build` (once) |
| Configuration | Baked into build | Loaded at runtime |
| Config file location | In source code | In public/ folder |
| Change config | Requires rebuild | Just edit file |
| Environment count | N builds | 1 build |
| Deployment | Build then deploy | Deploy once, config per env |

---

## Next Steps

1. Try changing config values in the browser console
2. Run the backend on a different port
3. Build for production and serve with different configs
4. Imagine deploying to 10 different environments – same build, different configs!

This is the essence of "Build Once, Deploy Many." 🚀
