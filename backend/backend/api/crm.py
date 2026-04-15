"""M-07 CRM et Support Client"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class Customer(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    country: str
    total_orders: int = 0
    total_spent: float = 0.0
    status: str = "active"
    tags: List[str] = []
    created_at: str

class Ticket(BaseModel):
    id: str
    customer_id: str
    subject: str
    description: str
    status: str = "open"  # open, in_progress, resolved, closed
    priority: str = "medium"  # low, medium, high, urgent
    assigned_to: Optional[str] = None
    messages: List[dict] = []
    created_at: str
    updated_at: str

class ChatMessage(BaseModel):
    from_user: bool
    message: str
    timestamp: str

# Mock customers
CUSTOMERS = [
    {
        "id": "cust-001",
        "email": "jean.dupont@email.com",
        "first_name": "Jean",
        "last_name": "Dupont",
        "phone": "+33 6 12 34 56 78",
        "country": "FR",
        "total_orders": 3,
        "total_spent": 125.50,
        "status": "active",
        "tags": ["vip", "frequent"],
        "created_at": "2024-01-10T10:00:00Z",
    },
    {
        "id": "cust-002",
        "email": "marie.durand@email.com",
        "first_name": "Marie",
        "last_name": "Durand",
        "phone": "+33 6 98 76 54 32",
        "country": "FR",
        "total_orders": 1,
        "total_spent": 41.17,
        "status": "active",
        "tags": [],
        "created_at": "2024-01-15T10:00:00Z",
    },
]

# Mock tickets
TICKETS = [
    {
        "id": "ticket-001",
        "customer_id": "cust-001",
        "subject": "Problème de livraison",
        "description": "Ma commande n'est pas encore arrivée après 15 jours",
        "status": "in_progress",
        "priority": "high",
        "assigned_to": "support-team",
        "messages": [
            {"from_user": True, "message": "Ma commande n'est pas arrivée", "timestamp": "2024-01-20T10:00:00Z"},
            {"from_user": False, "message": "Je vérifie votre dossier", "timestamp": "2024-01-20T10:30:00Z"},
        ],
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T10:30:00Z",
    },
]

@router.get("/customers", response_model=List[dict])
async def list_customers(
    status: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = 50,
):
    """List customers"""
    customers = CUSTOMERS.copy()
    if status:
        customers = [c for c in customers if c.get("status") == status]
    if country:
        customers = [c for c in customers if c.get("country") == country.upper()]
    return customers[:limit]

@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    """Get customer details"""
    customer = next((c for c in CUSTOMERS if c["id"] == customer_id), None)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers")
async def create_customer(
    email: str,
    first_name: str,
    last_name: str,
    country: str,
    phone: Optional[str] = None,
):
    """Create new customer"""
    customer = {
        "id": f"cust-{uuid.uuid4().hex[:6]}",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "country": country.upper(),
        "total_orders": 0,
        "total_spent": 0.0,
        "status": "active",
        "tags": [],
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    CUSTOMERS.append(customer)
    return {"customer": customer, "success": True}

@router.get("/tickets", response_model=List[dict])
async def list_tickets(
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
):
    """List support tickets"""
    tickets = TICKETS.copy()
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    if customer_id:
        tickets = [t for t in tickets if t["customer_id"] == customer_id]
    return tickets

@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Get ticket details"""
    ticket = next((t for t in TICKETS if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/tickets")
async def create_ticket(
    customer_id: str,
    subject: str,
    description: str,
    priority: str = "medium",
):
    """Create support ticket"""
    ticket = {
        "id": f"ticket-{uuid.uuid4().hex[:6]}",
        "customer_id": customer_id,
        "subject": subject,
        "description": description,
        "status": "open",
        "priority": priority,
        "assigned_to": None,
        "messages": [
            {"from_user": True, "message": description, "timestamp": datetime.utcnow().isoformat() + "Z"}
        ],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    TICKETS.append(ticket)
    return {"ticket": ticket, "success": True}

@router.post("/tickets/{ticket_id}/respond")
async def respond_ticket(ticket_id: str, message: str):
    """Respond to ticket"""
    ticket = next((t for t in TICKETS if t["id"] == ticket_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket["messages"].append({
        "from_user": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })
    ticket["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"ticket": ticket, "success": True}

@router.get("/stats")
async def get_crm_stats():
    """Get CRM statistics"""
    total_customers = len(CUSTOMERS)
    active_customers = len([c for c in CUSTOMERS if c.get("status") == "active"])
    
    open_tickets = len([t for t in TICKETS if t["status"] == "open"])
    in_progress_tickets = len([t for t in TICKETS if t["status"] == "in_progress"])
    
    total_revenue = sum(c.get("total_spent", 0) for c in CUSTOMERS)
    
    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "total_revenue": round(total_revenue, 2),
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "avg_order_value": round(total_revenue / total_customers, 2) if total_customers > 0 else 0,
    }

@router.get("/chatbot")
async def chatbot(message: str, customer_id: Optional[str] = None):
    """AI Chatbot response"""
    # Simple keyword-based responses
    responses = {
        "order": "Pour suivre votre commande, gunakan le numéro de suivi fourni dans l'email de confirmation.",
        "delivery": "Les délais de livraison varient entre 10-20 jours selon votre pays.",
        "return": "Vous pouvez retourner un produit dans les 14 jours suivant la réception.",
        "refund": "Les remboursements sont traités sous 5-10 jours ouvrés.",
        "default": "Je comprends votre demande. Un agent va vous répondre sous peu.",
    }
    
    message_lower = message.lower()
    for keyword, response in responses.items():
        if keyword in message_lower:
            return {"response": response, "intent": keyword}
    
    return {"response": responses["default"], "intent": "unknown"}