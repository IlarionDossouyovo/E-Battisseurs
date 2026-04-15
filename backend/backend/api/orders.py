"""M-03 Commandes - Order Management"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class OrderItem(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    title: str
    quantity: int
    price: float
    image_url: Optional[str] = None

class ShippingAddress(BaseModel):
    first_name: str
    last_name: str
    address1: str
    address2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    phone: str

class Order(BaseModel):
    id: str
    order_number: str
    customer_id: str
    items: List[OrderItem]
    subtotal: float
    shipping_cost: float
    tax_amount: float
    discount_amount: float = 0.0
    total: float
    currency: str = "USD"
    status: str = "pending"
    shipping_address: ShippingAddress
    supplier_id: Optional[str] = None
    tracking_number: Optional[str] = None
    carrier: Optional[str] = None
    created_at: str
    updated_at: str

class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[dict]
    shipping_address: dict

# Mock orders
MOCK_ORDERS: List[dict] = [
    {
        "id": "ord-001",
        "order_number": "GS-2024-00001",
        "customer_id": "cust-001",
        "items": [
            {
                "product_id": "prod-001",
                "variant_id": "v1",
                "title": "Smart Watch Fitness Tracker - Noir",
                "quantity": 1,
                "price": 29.99,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf33?w=200",
            }
        ],
        "subtotal": 29.99,
        "shipping_cost": 5.99,
        "tax_amount": 2.90,
        "discount_amount": 0.0,
        "total": 38.88,
        "currency": "USD",
        "status": "processing",
        "shipping_address": {
            "first_name": "Jean",
            "last_name": "Dupont",
            "address1": "123 Rue de la Paix",
            "city": "Paris",
            "state": "IDF",
            "postal_code": "75001",
            "country": "FR",
            "phone": "+33 6 12 34 56 78",
        },
        "supplier_id": "aliexpress",
        "tracking_number": "TRK123456789",
        "carrier": "DHL",
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T14:00:00Z",
    },
    {
        "id": "ord-002",
        "order_number": "GS-2024-00002",
        "customer_id": "cust-002",
        "items": [
            {
                "product_id": "prod-003",
                "title": "Lampe de Bureau LED USB",
                "quantity": 2,
                "price": 15.99,
                "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=200",
            }
        ],
        "subtotal": 31.98,
        "shipping_cost": 8.99,
        "tax_amount": 3.40,
        "discount_amount": 3.20,
        "total": 41.17,
        "currency": "USD",
        "status": "shipped",
        "shipping_address": {
            "first_name": "Marie",
            "last_name": "Durand",
            "address1": "45 Avenue des Champs-Élysées",
            "city": "Lyon",
            "postal_code": "69002",
            "country": "FR",
            "phone": "+33 6 98 76 54 32",
        },
        "supplier_id": "cj",
        "tracking_number": "TRK987654321",
        "carrier": "FedEx",
        "created_at": "2024-01-21T09:00:00Z",
        "updated_at": "2024-01-22T10:00:00Z",
    },
]

@router.get("/orders", response_model=List[dict])
async def list_orders(
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    limit: int = 20,
):
    """List orders"""
    orders = MOCK_ORDERS.copy()
    
    if status:
        orders = [o for o in orders if o.get("status") == status]
    if customer_id:
        orders = [o for o in orders if o.get("customer_id") == customer_id]
    
    return orders[:limit]

@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    """Get order details"""
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders")
async def create_order(request: CreateOrderRequest):
    """Create new order"""
    order_id = f"ord-{uuid.uuid4().hex[:8]}"
    order_number = f"GS-2024-{len(MOCK_ORDERS) + 1:05d}"
    
    items_data = request.items
    subtotal = sum(item.get("quantity", 1) * item.get("price", 0) for item in items_data)
    shipping_cost = 5.99
    tax_amount = subtotal * 0.10
    total = subtotal + shipping_cost + tax_amount
    
    new_order = {
        "id": order_id,
        "order_number": order_number,
        "customer_id": request.customer_id,
        "items": items_data,
        "subtotal": round(subtotal, 2),
        "shipping_cost": shipping_cost,
        "tax_amount": round(tax_amount, 2),
        "discount_amount": 0.0,
        "total": round(total, 2),
        "currency": "USD",
        "status": "pending",
        "shipping_address": request.shipping_address,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    
    MOCK_ORDERS.append(new_order)
    
    return {"order": new_order, "success": True}

@router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """Update order status"""
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order["status"] = status
    order["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"order": order}

@router.get("/orders/{order_id}/tracking")
async def get_tracking(order_id: str):
    """Get order tracking info"""
    order = next((o for o in MOCK_ORDERS if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "order_id": order_id,
        "tracking_number": order.get("tracking_number"),
        "carrier": order.get("carrier"),
        "status": order.get("status"),
        "updated_at": order.get("updated_at"),
    }

@router.get("/stats")
async def get_order_stats():
    """Get order statistics"""
    total_orders = len(MOCK_ORDERS)
    pending = len([o for o in MOCK_ORDERS if o.get("status") == "pending"])
    processing = len([o for o in MOCK_ORDERS if o.get("status") == "processing"])
    shipped = len([o for o in MOCK_ORDERS if o.get("status") == "shipped"])
    delivered = len([o for o in MOCK_ORDERS if o.get("status") == "delivered"])
    
    return {
        "total": total_orders,
        "pending": pending,
        "processing": processing,
        "shipped": shipped,
        "delivered": delivered,
        "revenue": sum(o.get("total", 0) for o in MOCK_ORDERS),
    }