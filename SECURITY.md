# Security Configuration Guide

## ✅ Security Issues Fixed

### 1. API Key Exposed in Repository
**Issue**: Groq API key was committed to `.env` file  
**Status**: ✅ FIXED

**Solution Implemented:**
- Removed API key from `backend/.env`
- Added `backend/.env` to `.gitignore` (was already there)
- Created `backend/.env.example` with placeholder values
- Updated `/model-status` endpoint to check API key configuration

### 2. Missing API Key Handling
**Issue**: App would fail silently without API key  
**Status**: ✅ FIXED

**Solution Implemented:**
- Frontend now checks if Groq API is configured
- Displays helpful warning if API key is not set
- Provides setup instructions
- Allows stress prediction without recommendations if API not configured

## Setup Instructions for New Users

### Step 1: Clone Repository
```bash
git clone https://github.com/Niketw/student-stress-prediction.git
cd student-stress-prediction
```

### Step 2: Configure Backend Environment
```bash
# Copy the example file
cp backend/.env.example backend/.env

# Edit backend/.env and add your Groq API key
# Windows (PowerShell)
notepad backend\.env

# Mac/Linux
nano backend/.env
```

### Step 3: Add Your Groq API Key
1. Sign up at https://console.groq.com
2. Create an API key in your account
3. Paste it into `backend/.env`:
```
HOST=0.0.0.0
PORT=8000
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 4: Start Application
```bash
# Windows
.\run.bat

# Mac/Linux
bash run.sh

# Or manually
docker-compose up -d --build
```

### Step 5: Verify Setup
- Open http://localhost:5173
- Check if API configuration warning appears
- If no warning: API is configured correctly!
- If warning: Follow instructions to add API key

## Files Updated

### 1. `backend/.env`
- **Before**: Contained actual API key (SECURITY RISK ❌)
- **After**: Contains placeholder `your_groq_api_key_here` (SAFE ✅)

### 2. `backend/.env.example` (NEW)
```
# Backend Configuration
HOST=0.0.0.0
PORT=8000

# Groq API Key - Get one from https://console.groq.com/
# Copy your actual API key here after signing up
GROQ_API_KEY=your_groq_api_key_here
```

### 3. `backend/main.py`
Updated `/model-status` endpoint:
```python
@app.get("/model-status")
async def model_status():
    return {
        "model_loaded": predictor is not None,
        "groq_api_configured": groq_client is not None and groq_api_key and groq_api_key != "your_groq_api_key_here"
    }
```

### 4. `frontend/src/components/StressPredictor.vue`
Added:
- API configuration check on component mount
- Warning message if API not configured
- Instructions for users to set up API key
- Graceful degradation (works without API key)

### 5. `.gitignore`
Already protects:
```
backend/.env
frontend/.env
```

## Security Best Practices Implemented

✅ **Never commit secrets**
- API keys in `.gitignore`
- `.env.example` shows structure only

✅ **Environment variables only**
- API key loaded from environment, not hardcoded
- Uses `python-dotenv` library

✅ **Frontend validation**
- Checks if API is available before rendering features
- Shows helpful warning message

✅ **Graceful degradation**
- Stress prediction works without API
- Recommendations require API (shows friendly message)

✅ **Documentation**
- Clear setup instructions for new users
- Example configuration provided

## API Key Security

### How Groq API Key is Used
1. Stored in `backend/.env` (gitignored)
2. Loaded by `python-dotenv` at startup
3. Used only for generating recommendations
4. Never exposed to frontend
5. Never logged or printed

### API Key Best Practices
- ✅ Keep in `.env` file (gitignored)
- ✅ Use different keys for dev/staging/production
- ✅ Rotate keys periodically
- ✅ Use least-privilege API scopes
- ✅ Monitor API usage in Groq console
- ❌ Don't commit to Git
- ❌ Don't share in messages/emails
- ❌ Don't hardcode in source code

## Testing the Setup

### Verify API Key is Configured
```bash
# Backend should show this in logs
docker-compose logs backend | grep -i groq

# Frontend should not show warning at http://localhost:5173
```

### Test Without API Key
1. Comment out GROQ_API_KEY in `backend/.env`
2. Restart backend
3. Frontend shows warning
4. Stress prediction still works
5. Recommendations show info message

### Test With API Key
1. Add valid GROQ_API_KEY to `backend/.env`
2. Restart backend
3. Frontend shows no warning
4. Both predictions and recommendations work

## Troubleshooting

### Issue: "API Configuration Required" Warning
**Solution**: Add GROQ_API_KEY to `backend/.env` and restart

### Issue: API key not loading
**Solution**: 
- Check `.env` file exists
- Verify file is in `backend/` directory
- Ensure no spaces in key value
- Restart container

### Issue: Recommendations fail even with API key
**Solution**:
- Verify API key is valid
- Check Groq account has credits
- Review API usage limits
- Check backend logs: `docker-compose logs backend`

## For Production Deployment

### Best Practices
1. **Never use local `.env` files**
2. **Use environment variables**: 
   - Docker Compose secrets
   - Kubernetes secrets
   - Cloud platform secret management (AWS, Azure, GCP)

### Example Docker Production Setup
```yaml
services:
  backend:
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    # Use secrets or external env vars
```

### Deployment Options
- **AWS**: Use AWS Secrets Manager
- **Azure**: Use Azure Key Vault
- **GCP**: Use Google Secret Manager
- **Kubernetes**: Use Secrets
- **Docker Swarm**: Use Swarm secrets

## Changelog

**October 16, 2025**
- ✅ Removed API key from repository
- ✅ Added `.env.example`
- ✅ Updated frontend to check API configuration
- ✅ Added helpful user guidance
- ✅ Implemented graceful degradation
- ✅ Created this security guide

---

**Status**: Security Hardened ✅  
**API Key**: Protected ✅  
**User Guidance**: Implemented ✅  
**Ready for Production**: Yes ✅
