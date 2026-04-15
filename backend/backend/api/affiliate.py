"""M-11 Affilié et Revendeur"""
from fastapi import APIRouter, Query
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class Affiliate(BaseModel):
    id: str
    name: str
    email: str
    level: int = 1  # 1, 2, 3 (MLM levels)
    parent_id: Optional[str] = None
    commission_rate: float
    total_sales: float = 0.0
    total_commission: float = 0.0
    status: str = "active"
    joined_at: str

class Reseller(BaseModel):
    id: str
    name: str
    domain: Optional[str] = None
    api_key: str
    commission_rate: float
    total_orders: int = 0
    status: str = "active"
    created_at: str

# Mock affiliates
AFFILIATES = [
    {
        "id": "aff-001",
        "name": "John Doe",
        "email": "john@affiliate.com",
        "level": 1,
        "parent_id": None,
        "commission_rate": 10.0,
        "total_sales": 15000.00,
        "total_commission": 1500.00,
        "status": "active",
        "joined_at": "2024-01-01T10:00:00Z",
    },
    {
        "id": "aff-002",
        "name": "Jane Smith",
        "email": "jane@affiliate.com",
        "level": 2,
        "parent_id": "aff-001",
        "commission_rate": 5.0,
        "total_sales": 8000.00,
        "total_commission": 400.00,
        "status": "active",
        "joined_at": "2024-01-05T10:00:00Z",
    },
]

# Mock resellers
RESELLERS = [
    {
        "id": "res-001",
        "name": "MonBoutique",
        "domain": "monboutique.com",
        "api_key": "sk_live_xxxxx",
        "commission_rate": 15.0,
        "total_orders": 250,
        "status": "active",
        "created_at": "2024-01-02T10:00:00Z",
    },
]

@router.get("/affiliates", response_model=list[dict])
async def list_affiliates(level: Optional[int] = None, status: Optional[str] = None):
    """List affiliates"""
    affiliates = AFFILIATES.copy()
    if level:
        affiliates = [a for a in affiliates if a.get("level") == level]
    if status:
        affiliates = [a for a in affiliates if a.get("status") == status]
    return affiliates

@router.get("/affiliates/{affiliate_id}")
async def get_affiliate(affiliate_id: str):
    """Get affiliate details"""
    affiliate = next((a for a in AFFILIATES if a["id"] == affiliate_id), None)
    if not affiliate:
        return {"error": "Affiliate not found"}
    return affiliate

@router.post("/affiliates")
async def create_affiliate(name: str, email: str, parent_id: Optional[str] = None):
    """Create new affiliate"""
    level = 1
    if parent_id:
        parent = next((a for a in AFFILIATES if a["id"] == parent_id), None)
        if parent:
            level = min(parent.get("level", 1) + 1, 3)
    
    affiliate = {
        "id": f"aff-{uuid.uuid4().hex[:6]}",
        "name": name,
        "email": email,
        "level": level,
        "parent_id": parent_id,
        "commission_rate": 10.0 - (level - 1) * 2.5,  # 10%, 7.5%, 5%
        "total_sales": 0.0,
        "total_commission": 0.0,
        "status": "active",
        "joined_at": datetime.utcnow().isoformat() + "Z",
    }
    AFFILIATES.append(affiliate)
    return {"affiliate": affiliate, "success": True}

@router.post("/affiliates/{affiliate_id}/commission")
async def add_commission(affiliate_id: str, amount: float):
    """Add commission to affiliate"""
    affiliate = next((a for a in AFFILIATES if a["id"] == affiliate_id), None)
    if not affiliate:
        return {"error": "Affiliate not found"}
    
    commission = amount * (affiliate["commission_rate"] / 100)
    affiliate["total_sales"] += amount
    affiliate["total_commission"] += commission
    
    # Add to parent (MLM)
    if affiliate.get("parent_id"):
        parent = next((a for a in AFFILIATES if a["id"] == affiliate["parent_id"]), None)
        if parent:
            parent_commission = amount * (parent["commission_rate"] / 100)
            parent["total_sales"] += amount
            parent["total_commission"] += parent_commission
    
    return {"success": True, "commission": round(commission, 2)}

@router.get("/resellers", response_model=list[dict])
async def list_resellers(status: Optional[str] = None):
    """List resellers"""
    if status:
        return [r for r in RESELLERS if r.get("status") == status]
    return RESELLERS

@router.get("/resellers/{reseller_id}")
async def get_reseller(reseller_id: str):
    """Get reseller details"""
    reseller = next((r for r in RESELLERS if r["id"] == reseller_id), None)
    if not reseller:
        return {"error": "Reseller not found"}
    return reseller

@router.post("/resellers")
async def create_reseller(name: str, domain: Optional[str] = None):
    """Create white-label reseller"""
    reseller = {
        "id": f"res-{uuid.uuid4().hex[:6]}",
        "name": name,
        "domain": domain,
        "api_key": f"sk_live_{uuid.uuid4().hex[:24]}",
        "commission_rate": 15.0,
        "total_orders": 0,
        "status": "active",
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    RESELLERS.append(reseller)
    return {"reseller": reseller, "success": True}

@router.get("/stats")
async def get_affiliate_stats():
    """Get affiliate program statistics"""
    total_affiliates = len(AFFILIATES)
    active_affiliates = len([a for a in AFFILIATES if a.get("status") == "active"])
    
    total_sales = sum(a.get("total_sales", 0) for a in AFFILIATES)
    total_commission = sum(a.get("total_commission", 0) for a in AFFILIATES)
    
    total_resellers = len(RESELLERS)
    active_resellers = len([r for r in RESELLERS if r.get("status") == "active"])
    
    return {
        "affiliates": {
            "total": total_affiliates,
            "active": active_affiliates,
            "total_sales": round(total_sales, 2),
            "total_commission": round(total_commission, 2),
        },
        "resellers": {
            "total": total_resellers,
            "active": active_resellers,
        },
    }

@router.get("/links")
async def generate_link(affiliate_id: str):
    """Generate affiliate link"""
    affiliate = next((a for a in AFFILIATES if a["id"] == affiliate_id), None)
    if not affiliate:
        return {"error": "Affiliate not found"}
    
    return {
        "affiliate_id": affiliate_id,
        "tracking_code": affiliate_id.split("-")[1],
        "link": f"https://e-battisseurs.com/?ref={affiliate_id.split('-')[1]}",
        "coupon": f"AFF{affiliate_id.split('-')[1].upper()}",
    }