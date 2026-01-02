# ✅ Verification Checklist

Use this checklist to verify that everything is set up correctly and working.

## Prerequisites Check

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Node.js 16+ installed: `node --version`
- [ ] npm installed: `npm --version`
- [ ] Project cloned/extracted to: `/home/etty/try-dynamic-react`

## Setup Phase

- [ ] Run setup script: `bash setup.sh`
- [ ] Setup completed without errors
- [ ] Backend dependencies installed: `pip list | grep fastapi`
- [ ] Frontend dependencies installed: `ls frontend/node_modules | wc -l` (should be ~100+)

## Project Structure

- [ ] Backend folder exists: `ls backend/`
  - [ ] `main.py` exists
  - [ ] `requirements.txt` exists
- [ ] Frontend folder exists: `ls frontend/`
  - [ ] `src/` folder exists
  - [ ] `public/` folder exists
  - [ ] `package.json` exists
  - [ ] `index.html` exists
- [ ] Documentation exists:
  - [ ] `README.md`
  - [ ] `ARCHITECTURE.md`
  - [ ] `TESTING.md`
  - [ ] `QUICK_REFERENCE.md`
  - [ ] `DEPLOYMENT_EXAMPLES.md`
  - [ ] `DIAGRAMS.md`
  - [ ] `INDEX.md`

## Backend Verification

### Terminal 1: Start Backend

```bash
cd backend
python main.py
```

- [ ] Backend starts without errors
- [ ] Shows: "Backend running on port 8000"
- [ ] Shows: "Uvicorn running on http://0.0.0.0:8000"

### Terminal 3: Test Backend API

```bash
curl http://localhost:8000/api/hello
```

- [ ] Returns: `{"message":"hello from backend"}`
- [ ] Status code: 200

### Backend with Different Port

```bash
PORT=3000 python main.py
```

- [ ] Backend starts on port 3000
- [ ] Test API: `curl http://localhost:3000/api/hello`
- [ ] Returns correct response

## Frontend Development

### Terminal 2: Start Frontend Dev Server

```bash
cd frontend
npm run dev
```

- [ ] Frontend starts without errors
- [ ] Shows: "VITE v5.0.8 ready in XXX ms"
- [ ] Shows: "➜ Local: http://localhost:5173/"

### Browser Test

Open `http://localhost:5173/`

- [ ] Page loads
- [ ] Title shows: "Dynamic React Config Example"
- [ ] Heading shows: "Build Once, Deploy Many 🚀"
- [ ] Backend URL displayed: `http://localhost:8000`
- [ ] Message displayed: "hello from backend"
- [ ] No console errors (check with F12)

## Runtime Configuration Test

### Change config.json

Edit `frontend/public/config.json`:

```json
{
  "BACKEND_URL": "http://localhost:9999"
}
```

- [ ] File saved successfully

### Reload Browser

Press F5 or Cmd+R to refresh

- [ ] Backend URL shows: `http://localhost:9999`
- [ ] Error message displayed (backend not on 9999)
- [ ] **Key verification:** No React rebuild happened!

### Restore config.json

Change back to:

```json
{
  "BACKEND_URL": "http://localhost:8000"
}
```

- [ ] File saved

### Reload Browser

- [ ] Backend URL shows: `http://localhost:8000`
- [ ] Message displays: "hello from backend"
- [ ] App works again

## Production Build Test

### Build React

```bash
cd frontend
npm run build
```

- [ ] Build completes successfully
- [ ] Creates `dist/` folder
- [ ] Shows output summary with file sizes

### Verify config.json is NOT bundled

```bash
ls -la frontend/dist/
```

- [ ] No `config.json` in `dist/` folder
- [ ] Only contains: `index.html`, `assets/`

### Start Production Preview

```bash
cd frontend
npm run preview
```

- [ ] Shows: "➜ Local: http://localhost:4173/"

### Test Production Build

Open `http://localhost:4173/`

- [ ] Page loads
- [ ] Shows backend message
- [ ] Works exactly like dev build

### Change Config in Production Build

Edit `frontend/public/config.json` again to different backend

- [ ] Change file

### Reload Production Build

Visit `http://localhost:4173/` and refresh

- [ ] Uses new config
- [ ] No rebuild happened
- [ ] **This proves:** Same build serves different configs

## File Content Verification

### Check [src/config.js](frontend/src/config.js)

- [ ] Contains `loadConfig()` function
- [ ] Contains `getConfig()` function
- [ ] Uses `fetch('/config.json')`
- [ ] No hardcoded URLs
- [ ] No `process.env` usage

### Check [src/main.jsx](frontend/src/main.jsx)

- [ ] Contains `await loadConfig()` call
- [ ] Waits before rendering React
- [ ] Calls `ReactDOM.createRoot(...).render(<App />)`

### Check [src/App.jsx](frontend/src/App.jsx)

- [ ] Uses `getConfig()` to fetch config
- [ ] Fetches from `${config.BACKEND_URL}/api/hello`
- [ ] Displays backend response
- [ ] Shows backend URL used

### Check [public/config.json](frontend/public/config.json)

- [ ] Contains valid JSON
- [ ] Has `BACKEND_URL` key
- [ ] Value is `http://localhost:8000`

### Check [backend/main.py](backend/main.py)

- [ ] FastAPI app defined
- [ ] GET `/api/hello` endpoint exists
- [ ] Returns `{"message": "hello from backend"}`
- [ ] Reads `PORT` from `os.environ.get("PORT", 8000)`
- [ ] CORS enabled

## Documentation Verification

- [ ] [README.md](README.md) - Has setup instructions ✓
- [ ] [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - One-page summary ✓
- [ ] [ARCHITECTURE.md](ARCHITECTURE.md) - Technical deep dive ✓
- [ ] [TESTING.md](TESTING.md) - Demo scenarios ✓
- [ ] [DEPLOYMENT_EXAMPLES.md](DEPLOYMENT_EXAMPLES.md) - Real-world configs ✓
- [ ] [DIAGRAMS.md](DIAGRAMS.md) - Visual workflow ✓
- [ ] [INDEX.md](INDEX.md) - Documentation index ✓

## Edge Cases

### Backend Offline

Stop backend (Ctrl+C)

- [ ] Reload frontend
- [ ] Shows error message
- [ ] Gracefully handles connection error
- [ ] No crashes

### config.json Missing

Rename `frontend/public/config.json` temporarily

- [ ] Reload frontend
- [ ] Falls back to default `http://localhost:8000`
- [ ] Gracefully handles missing config
- [ ] Shows fallback error or warning

### Invalid JSON in config.json

Edit `frontend/public/config.json` with invalid JSON:

```
{broken json}
```

- [ ] Reload frontend
- [ ] Shows error message
- [ ] Doesn't crash React

## Performance Check

### Development Build Size

```bash
cd frontend && npm run build
ls -lh dist/assets/
```

- [ ] Main JS file is reasonable size (~50-150KB)
- [ ] No huge bundle size (would indicate config was bundled)

### Network Requests

With app running, open DevTools (F12) → Network tab

- [ ] See `config.json` request
- [ ] It's a separate HTTP request (not bundled)
- [ ] Size should be tiny (< 1KB)

## Success Criteria

### All of the following must pass:

- [ ] Backend starts and serves `/api/hello`
- [ ] Frontend dev server starts and loads
- [ ] App displays backend response in browser
- [ ] Changing `config.json` changes behavior
- [ ] No rebuild required for config changes
- [ ] Production build works (`npm run build` + preview)
- [ ] `config.json` is separate from React bundle
- [ ] Documentation is clear and complete

## If Anything Fails

### Check Logs

1. **Backend error?** Look for Python traceback in terminal
2. **Frontend error?** Look for JavaScript error in browser console (F12)
3. **Network error?** Check DevTools Network tab for failed requests

### Common Issues

- **"Cannot find config.json"** → Verify `frontend/public/config.json` exists
- **CORS error** → Backend CORS is enabled, should work
- **Port already in use** → Stop other services or use `PORT=XXXX`
- **npm install failed** → Try `npm install --legacy-peer-deps`

### Ask for Help

With the above checklist, you have verified:
- ✅ Project structure is correct
- ✅ Backend works
- ✅ Frontend works
- ✅ Runtime config loads
- ✅ Pattern works as intended
- ✅ Documentation is complete

You're ready to use this pattern! 🚀

---

## Quick Sanity Check

Run this to verify everything works (from project root):

```bash
# In 30 seconds, you'll know if everything works:

echo "1. Starting backend..."
(cd backend && timeout 5 python main.py &)
sleep 2

echo "2. Testing API..."
curl -s http://localhost:8000/api/hello | grep -q "hello from backend" && echo "✅ Backend works" || echo "❌ Backend failed"

echo "3. Checking frontend structure..."
[ -f "frontend/src/config.js" ] && echo "✅ config.js exists" || echo "❌ Missing config.js"
[ -f "frontend/public/config.json" ] && echo "✅ config.json exists" || echo "❌ Missing config.json"
[ -f "frontend/node_modules" ] && echo "✅ Dependencies installed" || echo "❌ Dependencies missing"

echo ""
echo "4. Ready to start:"
echo "   Terminal 1: cd backend && python main.py"
echo "   Terminal 2: cd frontend && npm run dev"
echo "   Browser: http://localhost:5173"
```

---

**When all checkboxes are marked, you're done!** ✅🎉
