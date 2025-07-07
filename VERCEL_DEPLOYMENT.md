# Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Environment Variables**: Have your API keys ready

## Deployment Steps

### 1. Set Environment Variables in Vercel

Add these environment variables in your Vercel project dashboard or via CLI:

```bash
# Set environment variables
vercel env add PINECONE_API_KEY
vercel env add PINECONE_INDEX_NAME
vercel env add PINECONE_CLOUD
vercel env add PINECONE_REGION
vercel env add GROQ_API_KEY
```

**Values to use:**
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_INDEX_NAME`: `abc-assistant-index-384d` (or your index name)
- `PINECONE_CLOUD`: `aws`
- `PINECONE_REGION`: `us-east-1`
- `GROQ_API_KEY`: Your Groq API key

### 2. Deploy to Vercel

```bash
# Login to Vercel
vercel login

# Deploy the project
vercel

# For production deployment
vercel --prod
```

### 3. Alternative: GitHub Integration

1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Add environment variables in Vercel dashboard
4. Vercel will auto-deploy on every push

## Configuration Details

### vercel.json Configuration

The `vercel.json` file is configured with:

- **Build**: Uses `@vercel/python` for FastAPI
- **Memory**: 1024MB for AI operations
- **Timeout**: 30 seconds for API calls
- **Region**: US East (iad1) for better performance
- **Environment**: References to Vercel environment variables

### File Structure for Deployment

```
├── app.py                 # Vercel entry point (wrapper)
├── main.py                # Main FastAPI application
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── core/                  # Core modules
│   ├── agent.py
│   ├── embeddings.py
│   ├── llm_setup.py
│   ├── prompt_templates.py
│   └── vector_store.py
├── knowledge_base/        # Knowledge base
└── scripts/               # Utility scripts
```

## Important Notes

### Data Ingestion
- Run `python scripts/ingest_data.py` locally before deployment
- Vercel functions are stateless - data must be in Pinecone

### Cold Starts
- First request may take 10-15 seconds (cold start)
- Subsequent requests will be faster
- Consider using Vercel Pro for better performance

### Limitations
- 10-second timeout on Hobby plan (30s on Pro)
- 1024MB memory limit
- Serverless functions are stateless

### Monitoring
- Check Vercel dashboard for logs
- Monitor function performance
- Set up alerts for errors

## Testing Deployment

Once deployed, test your API:

```bash
# Replace YOUR_VERCEL_URL with your actual Vercel URL
curl -X POST "https://YOUR_VERCEL_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello, what services do you offer?",
    "session_id": "test-session"
  }'
```

## Troubleshooting

### Common Issues:

1. **Environment Variables**: Ensure all variables are set in Vercel
2. **Dependencies**: Check `requirements.txt` includes all packages
3. **Timeout**: Increase function timeout if needed
4. **Memory**: Increase memory allocation for large models
5. **Cold Starts**: Consider keeping function warm with scheduled requests

### Logs:
- Check Vercel function logs in dashboard
- Use `vercel logs` CLI command
- Monitor performance metrics

## Cost Optimization

- Use Pinecone Starter plan for development
- Monitor Vercel usage
- Consider caching strategies
- Optimize model loading

Your ABC Assistant chatbot will be available at your Vercel URL!
