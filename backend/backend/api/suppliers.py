"""M-08 Fournisseur APIs - AliExpress, CJ, Alibaba, Amazon"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Models
class ProductSource(BaseModel):
    id: str
    supplier: str
    product_id: str
    title: str
    price: float
    currency: str = "USD"
    category: str
    rating: float = 0.0
    orders: int = 0
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    
class SupplierProduct(BaseModel):
    source: ProductSource
    quality_score: float = 0.0
    price_score: float = 0.0
    reliability_score: float = 0.0
    
class SearchResult(BaseModel):
    products: List[SupplierProduct]
    total: int
    page: int
    per_page: int

# Mock supplier data (would connect to real APIs in production)
MOCK_PRODUCTS = [
    {
        "id": "ae-001",
        "supplier": "AliExpress",
        "product_id": "1005001955385632",
        "title": "Smart Watch Fitness Tracker",
        "price": 29.99,
        "category": "Electronics",
        "rating": 4.5,
        "orders": 15000,
        "image_url": "https://ae01.alicdn.com/kf/H8f7e7f6c0c6d4f5e9b2c1a0d5e6f7g8h.jpg",
    },
    {
        "id": "ae-002",
        "supplier": "AliExpress", 
        "product_id": "1005001955385633",
        "title": "Wireless Earbuds Pro",
        "price": 39.99,
        "category": "Electronics",
        "rating": 4.7,
        "orders": 25000,
        "image_url": "https://ae01.alicdn.com/kf/H9g8f7f6c0c6d4f5e9b2c1a0d5e6f7g8h.jpg",
    },
    {
        "id": "cj-001",
        "supplier": "CJ Dropshipping",
        "product_id": "CJP-2024-001",
        "title": "LED Desk Lamp USB",
        "price": 15.99,
        "category": "Home",
        "rating": 4.3,
        "orders": 8000,
        "image_url": "https://cdn.cjdropshipping.com/images/001.jpg",
    },
    {
        "id": "alibaba-001",
        "supplier": "Alibaba",
        "product_id": "ALB-16001234",
        "title": "Bulk Wireless Mouse",
        "price": 8.50,
        "category": "Electronics",
        "rating": 4.6,
        "orders": 50000,
        "image_url": "https://img.alibaba.com/images/p1.jpg",
    },
    {
        "id": "amazon-001",
        "supplier": "Amazon",
        "product_id": "B08N5WRWNW",
        "title": "Premium Charging Cable",
        "price": 12.99,
        "category": "Electronics",
        "rating": 4.8,
        "orders": 100000,
        "image_url": "https://images-na.ssl-images-amazon.com/images/I/81.jpg",
    },
]

def calculate_scores(product: dict) -> dict:
    """Calculate quality, price, and reliability scores"""
    rating = product.get("rating", 0)
    orders = product.get("orders", 0)
    
    quality_score = min(rating / 5.0 * 100, 100)
    price_score = max(100 - (product.get("price", 0) * 2), 20)
    reliability_score = min(orders / 1000 * 100, 100) if orders > 0 else 50
    
    return {
        "quality_score": round(quality_score, 1),
        "price_score": round(price_score, 1),
        "reliability_score": round(reliability_score, 1),
    }

@router.get("/suppliers", response_model=List[dict])
async def get_suppliers():
    """List all available suppliers"""
    return [
        {"id": "aliexpress", "name": "AliExpress", "products": 50000000, "rating": 4.5},
        {"id": "cj", "name": "CJ Dropshipping", "products": 100000, "rating": 4.6},
        {"id": "alibaba", "name": "Alibaba", "products": 20000000, "rating": 4.4},
        {"id": "amazon", "name": "Amazon", "products": 100000000, "rating": 4.7},
    ]

@router.get("/suppliers/{supplier_id}/products", response_model=SearchResult)
async def get_supplier_products(
    supplier_id: str,
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    """Get products from a specific supplier"""
    filtered = [p for p in MOCK_PRODUCTS if p["supplier"].lower() == supplier_id.lower()]
    
    if category:
        filtered = [p for p in filtered if p.get("category", "").lower() == category.lower()]
    if min_price:
        filtered = [p for p in filtered if p.get("price", 0) >= min_price]
    if max_price:
        filtered = [p for p in filtered if p.get("price", 0) <= max_price]
    
    total = len(filtered)
    start = (page - 1) * per_page
    end = start + per_page
    items = filtered[start:end]
    
    products = [
        SupplierProduct(
            source=ProductSource(**p),
            **calculate_scores(p)
        )
        for p in items
    ]
    
    return SearchResult(
        products=products,
        total=total,
        page=page,
        per_page=per_page,
    )

@router.get("/search", response_model=SearchResult)
async def search_products(
    q: str = Query(..., min_length=1),
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    """Search products across all suppliers"""
    query_lower = q.lower()
    filtered = [
        p for p in MOCK_PRODUCTS
        if query_lower in p.get("title", "").lower()
    ]
    
    if category:
        filtered = [p for p in filtered if p.get("category", "").lower() == category.lower()]
    
    total = len(filtered)
    start = (page - 1) * per_page
    end = start + per_page
    items = filtered[start:end]
    
    products = [
        SupplierProduct(
            source=ProductSource(**p),
            **calculate_scores(p)
        )
        for p in items
    ]
    
    return SearchResult(
        products=products,
        total=total,
        page=page,
        per_page=per_page,
    )

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get product details by ID"""
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    scores = calculate_scores(product)
    return {
        "product": ProductSource(**product),
        "scores": scores,
        "updated_at": datetime.utcnow().isoformat(),
    }