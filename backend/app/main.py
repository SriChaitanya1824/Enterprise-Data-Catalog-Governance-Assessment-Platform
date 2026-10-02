"""
Enterprise Data Catalog Backend - Fast API Application
Main entry point for the application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Enterprise Data Catalog & Governance Assessment Platform",
    version="1.0.0",
    description="A comprehensive platform for data catalog, metadata management, and governance assessment",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Enterprise Data Catalog",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
