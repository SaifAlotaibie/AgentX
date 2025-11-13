# Setting Up Your OpenAI API Key

## Quick Setup (3 Steps)

### Step 1: Create `.env` file

In the `/backend/Agents/` directory, create a file named `.env`:

```bash
cd backend/Agents
touch .env
```

### Step 2: Copy this template into `.env`

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Backend API Configuration
BACKEND_API_URL=http://localhost:3000/api
BACKEND_API_KEY=

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Model Configuration
MODEL_NAME=gpt-4o-mini
MODEL_TEMPERATURE=0

# Logging Configuration
LOG_DIRECTORY=logs

# Feature Flags
USE_LOCAL_LLM=false
```

### Step 3: Replace with your actual OpenAI API key

Replace `sk-your-actual-api-key-here` with your actual OpenAI API key.

**Example**:
```env
OPENAI_API_KEY=sk-proj-abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx1234
```

## Getting Your OpenAI API Key

If you don't have an OpenAI API key yet:

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key immediately (you won't be able to see it again)
5. Paste it into your `.env` file

## Verify Your Setup

After creating the `.env` file:

```bash
# Test without actual LLM calls (uses mocked LLM)
python3 test_agent.py

# Start the server (will use your OpenAI API key)
uvicorn app:app --reload
```

## Using the Agent with OpenAI

Once your API key is set up, the agent will:

1. ✅ Use GPT-4o-mini for intelligent responses
2. ✅ Log all LLM calls with token usage
3. ✅ Track latency for each API call
4. ✅ Work with both Arabic and English naturally

## Model Configuration

You can change the model in `.env`:

```env
# Use GPT-4 (more capable but more expensive)
MODEL_NAME=gpt-4

# Use GPT-3.5-turbo (faster and cheaper)
MODEL_NAME=gpt-3.5-turbo

# Use GPT-4o-mini (recommended - balanced performance/cost)
MODEL_NAME=gpt-4o-mini
```

## Temperature Setting

Control response randomness:

```env
# More deterministic (recommended for customer service)
MODEL_TEMPERATURE=0

# More creative
MODEL_TEMPERATURE=0.7

# Very creative
MODEL_TEMPERATURE=1.0
```

## Important Notes

⚠️ **Security**:
- Never commit `.env` to git (it's already in `.gitignore`)
- Keep your API key private
- Rotate keys regularly

💰 **Costs**:
- GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Monitor usage at [https://platform.openai.com/usage](https://platform.openai.com/usage)

🔒 **Rate Limits**:
- New accounts have lower limits
- Request limit increases if needed

## Testing Without OpenAI (Optional)

The system can run tests without an API key:

```bash
# Tests use mocked LLM responses
python3 test_agent.py
```

But for actual agent conversations, you need a valid API key.

## Troubleshooting

### "API key not found"
- Check that `.env` exists in `/backend/Agents/`
- Verify no extra spaces around `OPENAI_API_KEY=`
- Ensure key starts with `sk-`

### "Rate limit exceeded"
- Wait a few minutes and try again
- Check your usage limits on OpenAI dashboard
- Consider upgrading your account

### "Invalid API key"
- Verify you copied the full key
- Generate a new key if needed
- Check for any hidden characters

## Example .env File (Complete)

```env
# OpenAI Configuration - REPLACE WITH YOUR KEY
OPENAI_API_KEY=sk-proj-1234567890abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmnop

# Backend API Configuration - Update when backend is ready
BACKEND_API_URL=http://localhost:3000/api
BACKEND_API_KEY=

# Server Configuration - Default ports
HOST=0.0.0.0
PORT=8000

# Model Configuration - Optimized for customer service
MODEL_NAME=gpt-4o-mini
MODEL_TEMPERATURE=0

# Logging Configuration - Default log directory
LOG_DIRECTORY=logs

# Feature Flags - Set to false to use OpenAI
USE_LOCAL_LLM=false
```

## Ready to Start!

Once your `.env` is set up:

```bash
# Start the agent server
uvicorn app:app --reload

# In another terminal, test it
curl -X POST http://localhost:8000/agent/message \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "S123",
    "userId": "U123",
    "userRole": "employee",
    "message": "What is Qiwa?"
  }'
```

Or open `sample_client.html` in your browser and start chatting!

---

Need help? Check `README.md` or `QUICKSTART.md` for more details.

