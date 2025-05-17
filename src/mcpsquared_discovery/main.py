"""
Main application module for MCP Squared Discovery Service.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from mcpsquared_discovery.api.routes import router
# from mcpsquared_discovery.core.config import settings

app = FastAPI(
    title="MCP Squared Discovery Service",
    description="A service to recommend MCP Servers based on project context",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
# app.include_router(router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
