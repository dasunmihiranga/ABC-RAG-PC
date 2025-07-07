# app.py
# Vercel deployment wrapper for the FastAPI application

from main import app

# This file is required for Vercel deployment
# It simply imports the FastAPI app from main.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
