"""M-01 Vitrine - Product Catalog API"""
from fastapi import APIRouter, Query
from typing import Optional, List, Literal
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class Product(BaseModel):
    id: str
    supplier_id: str
    supplier_product_id: str
    title: str
    description: str
    price: float
    compare_at_price: Optional[float] = None
    currency: str = "USD"
    category: str
    subcategory: Optional[str] = None
    images: List[str] = []
    options: List[dict] = []
    variants: List[dict] = []
    inventory: int = 1000
    weight: Optional[float] = None
    dimensions: Optional[dict] = None
    tags: List[str] = []
    status: Literal["active", "draft", "archived"] = "active"
    created_at: str
    updated_at: str

class ProductListResponse(BaseModel):
    products: List[Product]
    total: int
    page: int
    per_page: int
    total_pages: int

class Category(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    product_count: int = 0

# Mock product catalog
MOCK_CATALOG: List[dict] = [
    {
        "id": "prod-001",
        "supplier_id": "aliexpress",
        "supplier_product_id": "1005001955385632",
        "title": "Smart Watch Fitness Tracker - Noir",
        "description": "Montre connectée avec suivi cardiaque, podomètre et GPS. Écran AMOLED 1.3\". Batterie 7 jours.",
        "price": 29.99,
        "compare_at_price": 49.99,
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Wearables",
        "images": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf33?w=800",
            "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800",
        ],
        "options": [
            {"name": "Color", "values": ["Noir", "Blanc", "Rose Gold"]},
            {"name": "Size", "values": ["Standard", "Large"]},
        ],
        "variants": [
            {"id": "v1", "options": ["Noir", "Standard"], "price": 29.99, "inventory": 500},
            {"id": "v2", "options": ["Blanc", "Standard"], "price": 29.99, "inventory": 300},
            {"id": "v3", "options": ["Rose Gold", "Large"], "price": 34.99, "inventory": 200},
        ],
        "inventory": 1000,
        "weight": 0.05,
        "dimensions": {"length": 5, "width": 5, "height": 2},
        "tags": ["smartwatch", "fitness", "tracker"],
        "status": "active",
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z",
    },
    {
        "id": "prod-002",
        "supplier_id": "aliexpress",
        "supplier_product_id": "1005001955385633",
        "title": "Wireless Earbuds Pro",
        "description": "Ecouteurs sans fil avec réduction de bruit active. 30h d'autonomie avec étui de charge.",
        "price": 39.99,
        "compare_at_price": 59.99,
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Audio",
        "images": [
            "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800",
        ],
        "options": [{"name": "Color", "values": ["Noir", "Blanc"]}],
        "variants": [
            {"id": "v1", "options": ["Noir"], "price": 39.99, "inventory": 1000},
            {"id": "v2", "options": ["Blanc"], "price": 39.99, "inventory": 800},
        ],
        "inventory": 1800,
        "weight": 0.12,
        "tags": ["earbuds", "wireless", "bluetooth"],
        "status": "active",
        "created_at": "2024-01-16T10:00:00Z",
        "updated_at": "2024-01-16T10:00:00Z",
    },
    {
        "id": "prod-003",
        "supplier_id": "cj",
        "supplier_product_id": "CJP-2024-001",
        "title": "Lampe de Bureau LED USB",
        "description": "Lampe LED moderne avec port USB intégré. 3 niveaux de luminosité. Design minimaliste.",
        "price": 15.99,
        "compare_at_price": 24.99,
        "currency": "USD",
        "category": "Home",
        "subcategory": "Lighting",
        "images": [
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800",
        ],
        "options": [{"name": "Color", "values": ["Noir", "Blanc", "Gris"]}],
        "variants": [
            {"id": "v1", "options": ["Noir"], "price": 15.99, "inventory": 500},
            {"id": "v2", "options": ["Blanc"], "price": 15.99, "inventory": 400},
            {"id": "v3", "options": ["Gris"], "price": 17.99, "inventory": 300},
        ],
        "inventory": 1200,
        "weight": 0.8,
        "tags": ["lamp", "led", "desk"],
        "status": "active",
        "created_at": "2024-01-17T10:00:00Z",
        "updated_at": "2024-01-17T10:00:00Z",
    },
]

CATEGORIES = [
    {"id": "electronics", "name": "Electronics", "product_count": 15000},
    {"id": "electronics-wearables", "name": "Wearables", "parent_id": "electronics", "product_count": 2500},
    {"id": "electronics-audio", "name": "Audio", "parent_id": "electronics", "product_count": 3000},
    {"id": "home", "name": "Home", "product_count": 12000},
    {"id": "home-lighting", "name": "Lighting", "parent_id": "home", "product_count": 1500},
    {"id": "fashion", "name": "Fashion", "product_count": 20000},
    {"id": "beauty", "name": "Beauty", "product_count": 8000},
]

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    supplier_id: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    search: Optional[str] = None,
):
    """List products in the catalog"""
    products = MOCK_CATALOG.copy()
    
    if category:
        products = [p for p in products if p.get("category", "").lower() == category.lower()]
    if supplier_id:
        products = [p for p in products if p.get("supplier_id") == supplier_id]
    if status:
        products = [p for p in products if p.get("status") == status]
    if search:
        products = [p for p in products if search.lower() in p.get("title", "").lower()]
    
    # Sort
    if sort == "price_asc":
        products = sorted(products, key=lambda x: x.get("price", 0))
    elif sort == "price_desc":
        products = sorted(products, key=lambda x: x.get("price", 0), reverse=True)
    elif sort == "newest":
        products = sorted(products, key=lambda x: x.get("created_at", ""), reverse=True)
    
    total = len(products)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    
    return ProductListResponse(
        products=[Product(**p) for p in products[start:end]],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get product details"""
    product = next((p for p in MOCK_CATALOG if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found", "product_id": product_id}
    return Product(**product)

@router.get("/categories", response_model=List[Category])
async def list_categories(parent: Optional[str] = None):
    """List product categories"""
    if parent:
        cats = [c for c in CATEGORIES if c.get("parent_id") == parent]
    else:
        cats = [c for c in CATEGORIES if c.get("parent_id") is None]
    return [Category(**c) for c in cats]

@router.get("/featured")
async def get_featured_products():
    """Get featured products"""
    featured = [p for p in MOCK_CATALOG if p.get("status") == "active"][:6]
    return {"products": [Product(**p) for p in featured]}