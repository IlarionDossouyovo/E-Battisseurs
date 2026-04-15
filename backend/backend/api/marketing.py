"""M-06 Marketing Automation"""
from fastapi import APIRouter
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class Campaign(BaseModel):
    id: str
    name: str
    type: str  # email, sms, social
    status: str  # draft, active, paused, completed
    audience_size: int
    budget: Optional[float] = None
    sent: int = 0
    opened: int = 0
    clicked: int = 0
    created_at: str

class EmailTemplate(BaseModel):
    id: str
    name: str
    subject: str
    body: str
    variables: List[str] = []

# Mock campaigns
CAMPAIGNS = [
    {
        "id": "camp-001",
        "name": "Spring Sale 2024",
        "type": "email",
        "status": "active",
        "audience_size": 5500,
        "budget": 250.00,
        "sent": 5200,
        "opened": 2340,
        "clicked": 890,
        "created_at": "2024-01-15T10:00:00Z",
    },
    {
        "id": "camp-002",
        "name": "New Product Launch",
        "type": "social",
        "status": "active",
        "audience_size": 25000,
        "budget": 500.00,
        "sent": 22000,
        "opened": 0,
        "clicked": 1500,
        "created_at": "2024-01-20T10:00:00Z",
    },
    {
        "id": "camp-003",
        "name": "Abandoned Cart Reminder",
        "type": "email",
        "status": "active",
        "audience_size": 1200,
        "sent": 850,
        "opened": 420,
        "clicked": 180,
        "created_at": "2024-01-22T10:00:00Z",
    },
]

TEMPLATES = [
    {
        "id": "tpl-001",
        "name": "Welcome_email",
        "subject": "Bienvenue chez E-Battisseurs!",
        "body": "Bonjour {{name}},\n\nMerci de votre inscription...",
        "variables": ["name"],
    },
    {
        "id": "tpl-002",
        "name": "order_confirmation",
        "subject": "Confirmation de commande #{{order_number}}",
        "body": "Votre commande a été confirmée...",
        "variables": ["order_number", "name"],
    },
]

@router.get("/campaigns", response_model=List[dict])
async def list_campaigns(status: Optional[str] = None):
    """List marketing campaigns"""
    if status:
        return [c for c in CAMPAIGNS if c["status"] == status]
    return CAMPAIGNS

@router.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get campaign details"""
    campaign = next((c for c in CAMPAIGNS if c["id"] == campaign_id), None)
    if not campaign:
        return {"error": "Campaign not found"}
    return campaign

@router.post("/campaigns")
async def create_campaign(name: str, type: str, audience_size: int, budget: Optional[float] = None):
    """Create new campaign"""
    campaign = {
        "id": f"camp-{uuid.uuid4().hex[:6]}",
        "name": name,
        "type": type,
        "status": "draft",
        "audience_size": audience_size,
        "budget": budget,
        "sent": 0,
        "opened": 0,
        "clicked": 0,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    CAMPAIGNS.append(campaign)
    return {"campaign": campaign, "success": True}

@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(campaign_id: str):
    """Send/launch campaign"""
    campaign = next((c for c in CAMPAIGNS if c["id"] == campaign_id), None)
    if not campaign:
        return {"error": "Campaign not found"}
    
    campaign["status"] = "active"
    campaign["sent"] = campaign["audience_size"]
    
    return {"campaign": campaign, "success": True, "sent": campaign["sent"]}

@router.get("/templates", response_model=List[dict])
async def list_templates():
    """List email templates"""
    return TEMPLATES

@router.get("/analytics")
async def get_marketing_analytics():
    """Get marketing performance metrics"""
    total_sent = sum(c["sent"] for c in CAMPAIGNS)
    total_opened = sum(c["opened"] for c in CAMPAIGNS)
    total_clicked = sum(c["clicked"] for c in CAMPAIGNS)
    
    open_rate = (total_opened / total_sent * 100) if total_sent > 0 else 0
    click_rate = (total_clicked / total_opened * 100) if total_opened > 0 else 0
    
    return {
        "campaigns": len(CAMPAIGNS),
        "total_sent": total_sent,
        "total_opened": total_opened,
        "total_clicked": total_clicked,
        "open_rate": round(open_rate, 1),
        "click_rate": round(click_rate, 1),
        "roi": 4.2,
    }