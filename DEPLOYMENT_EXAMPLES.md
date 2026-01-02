# Example: Deployment Configurations

This folder would typically contain environment-specific config.json files
ready for deployment. This is just for reference.

## Example 1: Development Environment

**File: `config.development.json`**

```json
{
  "BACKEND_URL": "http://localhost:8000",
  "LOG_LEVEL": "debug",
  "FEATURE_FLAGS": {
    "betaUI": true,
    "analytics": false
  }
}
```

Copy to deployment:
```bash
cp config.development.json <dev-server>/config.json
```

## Example 2: Staging Environment

**File: `config.staging.json`**

```json
{
  "BACKEND_URL": "https://api-staging.example.com",
  "LOG_LEVEL": "info",
  "FEATURE_FLAGS": {
    "betaUI": true,
    "analytics": true
  }
}
```

Copy to deployment:
```bash
cp config.staging.json <staging-server>/config.json
```

## Example 3: Production Environment

**File: `config.production.json`**

```json
{
  "BACKEND_URL": "https://api.example.com",
  "LOG_LEVEL": "error",
  "FEATURE_FLAGS": {
    "betaUI": false,
    "analytics": true
  }
}
```

Copy to deployment:
```bash
cp config.production.json <prod-server>/config.json
```

## Deployment Process

### Step 1: Build React Once

```bash
cd frontend
npm run build
# Creates dist/ folder
```

### Step 2: Deploy to Each Environment

```bash
# Development
cp -r frontend/dist/* /var/www/dev/
cp config.development.json /var/www/dev/config.json

# Staging
cp -r frontend/dist/* /var/www/staging/
cp config.staging.json /var/www/staging/config.json

# Production
cp -r frontend/dist/* /var/www/prod/
cp config.production.json /var/www/prod/config.json
```

### Result

Same React build, different configs, different backend URLs. ✅

## Key Point

The React build (`dist/` folder) is **identical** across all environments.
Only `config.json` differs per environment.

If you rebuilt React for each environment, you'd have this:

```
React Build 1: prod environment
React Build 2: staging environment  
React Build 3: dev environment

← These are all the same! Wasteful. ❌
```

With runtime config:

```
React Build 1: (all environments)
  + config.json (dev)
  + config.json (staging)
  + config.json (prod)

← One build, deployed three ways. Efficient! ✅
```

## Scaling

Once you have this pattern, scaling to 10 environments is trivial:

```bash
npm run build  # Once!

for env in dev staging qa uat prod eu-prod ap-prod ...; do
  cp -r frontend/dist/* /var/www/$env/
  cp config.$env.json /var/www/$env/config.json
done
```

Same build serves all. 🚀
