"""M-05 Paiements - Payment Gateway"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, Literal, List
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class PaymentMethod(BaseModel):
    type: Literal["card", "paypal", "crypto", "mobile_money"]
    last4: Optional[str] = None
    brand: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None

class Payment(BaseModel):
    id: str
    order_id: str
    customer_id: str
    amount: float
    currency: str = "USD"
    status: str = "pending"
    method: PaymentMethod
    transaction_id: Optional[str] = None
    created_at: str
    updated_at: str

# Mock payments
MOCK_PAYMENTS: List[dict] = [
    {
        "id": "pay-001",
        "order_id": "ord-001",
        "customer_id": "cust-001",
        "amount": 38.88,
        "currency": "USD",
        "status": "succeeded",
        "method": {"type": "card", "last4": "4242", "brand": "Visa", "expiry_month": 12, "expiry_year": 2025},
        "transaction_id": "ch_3Oabc123",
        "created_at": "2024-01-20T10:05:00Z",
        "updated_at": "2024-01-20T10:05:02Z",
    },
    {
        "id": "pay-002",
        "order_id": "ord-002",
        "customer_id": "cust-002",
        "amount": 41.17,
        "currency": "USD",
        "status": "succeeded",
        "method": {"type": "paypal"},
        "transaction_id": "PAYID-MM123456",
        "created_at": "2024-01-21T09:05:00Z",
        "updated_at": "2024-01-21T09:05:01Z",
    },
]

@router.get("/payments", response_model=list[dict])
async def list_payments(order_id: Optional[str] = None, limit: int = 20):
    """List payments"""
    if order_id:
        return [p for p in MOCK_PAYMENTS if p.get("order_id") == order_id][:limit]
    return MOCK_PAYMENTS[:limit]

@router.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    """Get payment details"""
    payment = next((p for p in MOCK_PAYMENTS if p["id"] == payment_id), None)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.post("/payments/create-intent")
async def create_payment_intent(order_id: str, amount: float, currency: str = "USD"):
    """Create Stripe payment intent"""
    payment_id = f"pi_{uuid.uuid4().hex[:24]}"
    
    return {
        "client_secret": f"{payment_id}_secret_{uuid.uuid4().hex[:16]}",
        "payment_id": payment_id,
        "amount": amount,
        "currency": currency,
    }

@router.post("/payments/confirm")
async def confirm_payment(payment_id: str):
    """Confirm payment"""
    payment = next((p for p in MOCK_PAYMENTS if p["id"] == payment_id), None)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment["status"] = "succeeded"
    payment["transaction_id"] = f"ch_{uuid.uuid4().hex[:14]}"
    payment["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"payment": payment, "success": True}

@router.post("/payments/refund")
async def refund_payment(payment_id: str, amount: Optional[float] = None):
    """Process refund"""
    payment = next((p for p in MOCK_PAYMENTS if p["id"] == payment_id), None)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    refund_amount = amount or payment["amount"]
    
    return {
        "refund_id": f"re_{uuid.uuid4().hex[:14]}",
        "payment_id": payment_id,
        "amount": refund_amount,
        "status": "succeeded",
    }

@router.get("/methods")
async def get_payment_methods():
    """Get available payment methods"""
    return {
        "methods": [
            {"id": "card", "name": "Credit/Debit Card", "currencies": ["USD", "EUR", "GBP"], "enabled": True},
            {"id": "paypal", "name": "PayPal", "currencies": ["USD", "EUR"], "enabled": True},
            {"id": "crypto", "name": "Cryptocurrency", "currencies": ["USD", "EUR", "BTC", "ETH"], "enabled": True},
            {"id": "mobile_money", "name": "Mobile Money (Africa)", "currencies": ["XOF", "XAF", "USD"], "enabled": True},
        ]
    }

@router.get("/currencies")
async def get_supported_currencies():
    """Get supported currencies"""
    return {
        "currencies": [
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
            {"code": "XOF", "name": "West African Franc", "symbol": "CFA"},
            {"code": "XAF", "name": "Central African Franc", "symbol": "FCFA"},
        ]
    }

@router.get("/stats")
async def get_payment_stats():
    """Get payment statistics"""
    total = len(MOCK_PAYMENTS)
    succeeded = len([p for p in MOCK_PAYMENTS if p.get("status") == "succeeded"])
    pending = len([p for p in MOCK_PAYMENTS if p.get("status") == "pending"])
    failed = len([p for p in MOCK_PAYMENTS if p.get("status") == "failed"])
    
    return {
        "total_transactions": total,
        "succeeded": succeeded,
        "pending": pending,
        "failed": failed,
        "total_amount": sum(p.get("amount", 0) for p in MOCK_PAYMENTS),
    }