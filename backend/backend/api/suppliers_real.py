"""Real Supplier APIs for E-Battisseurs"""
import os
import httpx
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/suppliers", tags=["Real Suppliers"])

# API Keys from environment
ALIEXPRESS_API_KEY = os.environ.get("ALIEXPRESS_API_KEY")
ALIEXPRESS_API_SECRET = os.environ.get("ALIEXPRESS_API_SECRET")
CJ_API_KEY = os.environ.get("CJ_DROPSHIPPING_API_KEY")
ALIBABA_API_KEY = os.environ.get("ALIBABA_API_KEY")


async def fetch_aliexpress_products(keyword: str, page: int = 1) -> Dict[str, Any]:
    """Fetch products from AliExpress API"""
    if not ALIEXPRESS_API_KEY:
        # Return mock data if no API key
        return {
            "products": [
                {
                    "id": "ae-prod-001",
                    "title": f"AliExpress {keyword} - Premium Quality",
                    "price": 29.99,
                    "orders": 15000,
                    "rating": 4.5,
                    "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf33?w=400"
                },
                {
                    "id": "ae-prod-002", 
                    "title": f"AliExpress {keyword} - Best Seller",
                    "price": 19.99,
                    "orders": 8500,
                    "rating": 4.6,
                    "image": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400"
                }
            ],
            "source": "aliexpress",
            "page": page
        }
    
    # Real API call (example structure)
    url = "https://api.aliexpress.com/api/products/search"
    headers = {"Authorization": f"Bearer {ALIEXPRESS_API_KEY}"}
    params = {"keyword": keyword, "page": page}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            return {"error": str(e), "products": []}


async def fetch_cj_products(keyword: str) -> Dict[str, Any]:
    """Fetch products from CJ Dropshipping API"""
    if not CJ_API_KEY:
        return {
            "products": [
                {
                    "id": "cj-prod-001",
                    "title": f"CJ {keyword}",
                    "price": 15.99,
                    "shipping": "3-7 days",
                    "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf33?w=400"
                }
            ],
            "source": "cj"
        }
    
    url = "https://api.cjdropshipping.com/api/products"
    headers = {"Authorization": f"Bearer {CJ_API_KEY}"}
    params = {"keyword": keyword}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            return {"products": []}


# API Endpoints
@router.get("/aliexpress/search")
async def aliexpress_search(q: str, page: int = 1):
    """Search AliExpress products"""
    return await fetch_aliexpress_products(q, page)


@router.get("/cj/search")
async def cj_search(q: str):
    """Search CJ products"""
    return await fetch_cj_products(q)


@router.get("/compare")
async def compare_prices(q: str):
    """Compare prices across all suppliers"""
    ae = await fetch_aliexpress_products(q)
    cj = await fetch_cj_products(q)
    
    return {
        "query": q,
        "aliexpress": ae.get("products", []),
        "cj": cj.get("products", []),
        "best_price": min(
            [p.get("price", 999) for p in ae.get("products", []) + cj.get("products", [])],
            default=0
        )
    }


@router.get("/status")
async def supplier_status():
    """Check supplier API status"""
    return {
        "aliexpress": "configured" if ALIEXPRESS_API_KEY else "demo",
        "cj": "configured" if CJ_API_KEY else "demo",
        "alibaba": "configured" if ALIBABA_API_KEY else "demo"
    }