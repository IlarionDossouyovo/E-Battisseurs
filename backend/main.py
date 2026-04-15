"""
GLOBALSHIP PRO - Main FastAPI Application
E-Commerce Dropshipping Platform
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api import suppliers, orders, products, payments, logistics, analytics, marketing, crm, compliance, affiliate, orchestrator
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    print("🚀 E-Battisseurs - Démarrage...")
    print(f"📦 Modules chargés: M-01 à M-12")
    print(f"🌍 Mode: {settings.ENVIRONMENT}")
    yield
    # Shutdown
    print("📴 E-Battisseurs - Arrêt...")

app = FastAPI(
    title="E-Battisseurs API",
    description="API Plateforme Dropshipping Internationale",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc), "type": "error"},
    )

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "E-Battisseurs by ELECTRON",
        "version": "1.0.0",
        "modules": {
            "M-01": "Vitrine",
            "M-02": "Sourcing IA",
            "M-03": "Commandes",
            "M-04": "Logistique",
            "M-05": "Paiements",
            "M-06": "Marketing",
            "M-07": "CRM",
            "M-08": "Fournisseurs",
            "M-09": "Analytics",
            "M-10": "Conformité",
            "M-11": "Affiliation",
            "M-12": "Orchestrateur IA",
        }
    }

# API Routes
app.include_router(suppliers.router, prefix="/api/v1", tags=["M-08 Fournisseurs"])
app.include_router(products.router, prefix="/api/v1", tags=["M-01 Vitrine"])
app.include_router(orders.router, prefix="/api/v1", tags=["M-03 Commandes"])
app.include_router(payments.router, prefix="/api/v1", tags=["M-05 Paiements"])
app.include_router(logistics.router, prefix="/api/v1", tags=["M-04 Logistique"])
app.include_router(analytics.router, prefix="/api/v1", tags=["M-09 Analytics"])
app.include_router(marketing.router, prefix="/api/v1", tags=["M-06 Marketing"])
app.include_router(crm.router, prefix="/api/v1", tags=["M-07 CRM"])
app.include_router(compliance.router, prefix="/api/v1", tags=["M-10 Compliance"])
app.include_router(affiliate.router, prefix="/api/v1", tags=["M-11 Affiliation"])
app.include_router(orchestrator.router, prefix="/api/v1", tags=["M-12 IA"])

# M-06 Marketing (placeholder)
# M-07 CRM (placeholder)
# M-10 Conformité (placeholder)
# M-11 Affiliation (placeholder)
# M-12 Orchestrateur IA (placeholder)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)