"""Main FastAPI application"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db
from .routes import (
    auth,
    organizations,
    respondents,
    questionnaires,
    responses,
    campaigns,
    reports,
    analytics,
    admin,
    lgpd,
    demo,
    campaign_analytics
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management - startup and shutdown"""
    # Startup
    print("🚀 Starting SIMDCCO...")
    init_db()
    print("✅ SIMDCCO ready!")
    yield
    # Shutdown
    print("👋 Shutting down SIMDCCO...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema de Diagnóstico de Saúde Mental, Clima e Cultura Organizacional",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "trace": str(exc)},
        )

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Proxy headers - ensures redirects use the correct host
from fastapi.middleware.proxy_headers import ProxyHeadersMiddleware
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])

# Security headers
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure properly in production
    )

# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(organizations.router, prefix="/api/organizations", tags=["Organizations"])
app.include_router(respondents.router, prefix="/api/respondents", tags=["Respondents"])
app.include_router(questionnaires.router, prefix="/api/questionnaires", tags=["Questionnaires"])
app.include_router(responses.router, prefix="/api/responses", tags=["Responses"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(lgpd.router, prefix="/api/lgpd", tags=["LGPD"])
app.include_router(demo.router, prefix="/api/demo", tags=["Demo"])
app.include_router(campaign_analytics.router, prefix="/api/campaigns/analytics", tags=["Campaign Analytics"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/api/docs" if settings.DEBUG else "Contact admin for access"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
