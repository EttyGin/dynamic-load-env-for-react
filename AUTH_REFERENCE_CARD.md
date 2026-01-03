# HTTP Bearer Authentication - Reference Card

## Quick Command Reference

### Start Backend
```bash
cd backend
pip install -r requirements.txt
MASTER_API_KEY=super-secret-key python main.py
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### Test Authentication
```bash
# Option 1: Python script
python test_auth.py

# Option 2: cURL commands
curl http://localhost:8000/api/hello  # ❌ No token

curl -H "Authorization: Bearer wrong-token" \
  http://localhost:8000/api/hello  # ❌ Wrong token

curl -H "Authorization: Bearer super-secret-key" \
  http://localhost:8000/api/hello  # ✅ Success
```

---

## Code Snippets

### Backend: Protect an Endpoint
```python
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()
MASTER_API_KEY = os.environ.get("MASTER_API_KEY")

def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    token = credentials.credentials
    if token != MASTER_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/api/endpoint")
def endpoint(token: str = Depends(verify_token)):
    return {"data": "protected"}
```

### Frontend: Send Authorization Header
```typescript
const config = getConfig();

const response = await fetch('/api/hello', {
    headers: {
        'Authorization': `Bearer ${config.MASTER_API_KEY}`
    }
});

const data = await response.json();
```

### Frontend: Config Interface
```typescript
interface Config {
    BACKEND_URL: string;
    MASTER_API_KEY: string;
}
```

### Frontend: Runtime Config Loading
```typescript
export async function loadConfig(): Promise<Config> {
    const response = await fetch('/config.json');
    const config = await response.json();
    return config;
}
```

---

## Configuration Files

### `frontend/public/config.json`
```json
{
    "BACKEND_URL": "http://localhost:8000",
    "MASTER_API_KEY": "super-secret-key"
}
```

**Important:** NOT bundled into React build!

---

## Environment Variables

### Backend
```bash
# Required
MASTER_API_KEY=your-api-key

# Optional
PORT=8000  # defaults to 8000
```

**Never** hardcode these in code!

### Frontend
Uses runtime config from `config.json` **NOT** environment variables.

---

## API Response Codes

| Scenario | Status | Response |
|----------|--------|----------|
| Valid token | 200 | `{"message": "...", "authenticated": true}` |
| Missing token | 403 | `{"detail": "Not authenticated"}` |
| Invalid token | 401 | `{"detail": "Invalid or expired token"}` |
| Server error | 500 | `{"detail": "Server not properly configured..."}` |

---

## HTTP Headers

### Request with Valid Token
```http
GET /api/hello HTTP/1.1
Host: localhost:8000
Authorization: Bearer super-secret-key
```

### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{"message": "hello from backend", "authenticated": true}
```

---

## Deployment Checklist

- [ ] Set `MASTER_API_KEY` environment variable on backend
- [ ] Update `config.json` with production backend URL
- [ ] Update `config.json` with production API key
- [ ] Verify API calls include `Authorization` header
- [ ] Test with cURL or test script
- [ ] Use HTTPS in production (not HTTP)
- [ ] Never commit sensitive keys to git

---

## Troubleshooting

### Error: "Backend error: 401 Unauthorized"
**Cause:** API key mismatch or missing token
**Solution:** 
- Check `MASTER_API_KEY` environment variable
- Verify `config.json` has correct key
- Ensure Authorization header is sent

### Error: "Server not properly configured"
**Cause:** `MASTER_API_KEY` not set in environment
**Solution:**
```bash
export MASTER_API_KEY=your-key
python main.py
```

### Frontend can't load config.json
**Cause:** File not in public folder or CORS issue
**Solution:**
- Place `config.json` in `frontend/public/`
- Verify file path: `/config.json`
- Check browser console for errors

### "Invalid or expired token" on all requests
**Cause:** Token in config doesn't match environment variable
**Solution:**
```bash
# Set environment variable
MASTER_API_KEY=super-secret-key python main.py

# Ensure config.json has same key
# "MASTER_API_KEY": "super-secret-key"
```

---

## Security Best Practices

✅ **DO:**
- Store API keys in environment variables (backend)
- Load API keys from runtime config (frontend)
- Use HTTPS in production
- Use complex, random API keys
- Rotate keys regularly
- Log authentication failures
- Monitor for suspicious activity

❌ **DON'T:**
- Hardcode API keys in source code
- Commit keys to version control
- Share keys via email or chat
- Use simple keys like "secret" or "password"
- Expose keys in error messages
- Log full tokens/keys
- Use HTTP in production

---

## File Reference

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI with HTTPBearer auth |
| `frontend/src/config.ts` | Config loading & type definitions |
| `frontend/src/App.tsx` | Frontend with Authorization header |
| `frontend/public/config.json` | Runtime configuration |
| `test_auth.py` | Authentication testing script |
| `AUTH_IMPLEMENTATION.md` | Complete technical docs |
| `QUICK_AUTH_START.md` | Quick start guide |
| `AUTH_FLOW_DIAGRAMS.md` | Visual diagrams |
| `CHANGES_SUMMARY.md` | Before/after comparison |

---

## Additional Resources

### FastAPI Security
- [HTTPBearer Documentation](https://fastapi.tiangolo.com/advanced/security/http-bearer/)
- [OAuth2 with Password](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)
- [FastAPI Security Module](https://fastapi.tiangolo.com/tutorial/security/)

### React Configuration
- [React at Runtime Configuration](https://12factor.net/config)
- [Environment Variables in Vite](https://vitejs.dev/guide/env-and-mode.html)

### Best Practices
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Bearer Token Usage](https://tools.ietf.org/html/rfc6750)
- [API Key Management](https://cheatsheetseries.owasp.org/cheatsheets/API_Key_Lifecycle_Cheat_Sheet.html)

---

## Summary

This implementation demonstrates:

✅ **Backend:**
- HTTPBearer authentication
- Environment-based secrets
- Protected endpoints with dependency injection

✅ **Frontend:**
- Runtime configuration loading
- TypeScript interfaces
- Authorization headers in API calls

✅ **Deployment:**
- "Build Once, Deploy Many" pattern
- Environment-specific configuration
- No hardcoded secrets

This is **educational demonstration**, suitable for learning the patterns but should be enhanced for production:
- Replace with JWT tokens
- Add refresh token mechanism
- Implement user management
- Add role-based access control
- Use OAuth2 or OpenID Connect
