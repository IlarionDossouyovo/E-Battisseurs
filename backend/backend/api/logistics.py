"""M-04 Logistique - Logistics Platform"""
from fastapi import APIRouter, Query
from typing import Optional, List
from pydantic import BaseModel
import uuid

router = APIRouter()

# Models
class Carrier(BaseModel):
    id: str
    name: str
    logo: str
    countries: List[str]
    delivery_time: str
    price_range: str

class ShippingRate(BaseModel):
    carrier_id: str
    service: str
    price: float
    currency: str = "USD"
    estimated_days: int

class TrackingEvent(BaseModel):
    timestamp: str
    status: str
    location: str
    description: str

# Mock carriers
CARRIERS = [
    {"id": "dhl", "name": "DHL Express", "logo": "/images/carriers/dhl.png", "countries": ["US", "FR", "GB", "DE", "CN"], "delivery_time": "3-5 days", "price_range": "$15-$50"},
    {"id": "fedex", "name": "FedEx", "logo": "/images/carriers/fedex.png", "countries": ["US", "FR", "GB", "DE", "CN"], "delivery_time": "4-6 days", "price_range": "$12-$45"},
    {"id": "ups", "name": "UPS", "logo": "/images/carriers/ups.png", "countries": ["US", "FR", "GB", "DE"], "delivery_time": "4-7 days", "price_range": "$10-$40"},
    {"id": "aramex", "name": "Aramex", "logo": "/images/carriers/aramex.png", "countries": ["SA", "AE", "EG", "KE"], "delivery_time": "5-8 days", "price_range": "$8-$25"},
    {"id": "yunexpress", "name": "YunExpress", "logo": "/images/carriers/yun.png", "countries": ["CN", "US", "FR", "GB"], "delivery_time": "10-15 days", "price_range": "$3-$15"},
]

# Mock tracking events
TRACKING_EVENTS = [
    {
        "order_id": "ord-001",
        "events": [
            {"timestamp": "2024-01-20T14:00:00Z", "status": "in_transit", "location": "Paris, FR", "description": "Package in transit to destination"},
            {"timestamp": "2024-01-21T08:30:00Z", "status": "out_for_delivery", "location": "Paris, FR", "description": "Out for delivery"},
            {"timestamp": "2024-01-21T10:00:00Z", "status": "delivered", "location": "Paris, FR", "description": "Delivered - Signed by recipient"},
        ]
    },
    {
        "order_id": "ord-002", 
        "events": [
            {"timestamp": "2024-01-22T10:00:00Z", "status": "in_transit", "location": "Lyon, FR", "description": "Package dispatched from sorting center"},
        ]
    },
]

@router.get("/carriers", response_model=List[dict])
async def list_carriers(country: Optional[str] = None):
    """List available carriers"""
    if country:
        return [c for c in CARRIERS if country.upper() in c["countries"]]
    return CARRIERS

@router.get("/carriers/{carrier_id}")
async def get_carrier(carrier_id: str):
    """Get carrier details"""
    carrier = next((c for c in CARRIERS if c["id"] == carrier_id), None)
    if not carrier:
        return {"error": "Carrier not found"}
    return carrier

@router.get("/rates")
async def get_shipping_rates(
    origin_country: str = Query(..., min_length=2),
    destination_country: str = Query(..., min_length=2),
    weight: float = Query(1.0, gt=0),
):
    """Calculate shipping rates"""
    rates = []
    for carrier in CARRIERS:
        if destination_country.upper() in carrier["countries"]:
            base_price = 5.0
            weight_price = weight * 2.0
            total = base_price + weight_price
            
            rates.append({
                "carrier_id": carrier["id"],
                "carrier_name": carrier["name"],
                "service": "Standard",
                "price": round(total, 2),
                "currency": "USD",
                "estimated_days": int(carrier["delivery_time"].split("-")[0]) if "-" in carrier["delivery_time"] else 7,
            })
    
    return {"rates": rates}

@router.get("/track/{tracking_number}")
async def track_shipment(tracking_number: str):
    """Track a shipment"""
    for tracking in TRACKING_EVENTS:
        if tracking.get("tracking_number") == tracking_number:
            return tracking
    
    # Mock real-time tracking
    return {
        "tracking_number": tracking_number,
        "carrier": "DHL",
        "status": "in_transit",
        "events": [
            {
                "timestamp": "2024-01-22T10:00:00Z",
                "status": "in_transit",
                "location": "Hong Kong, CN",
                "description": "Package processed at distribution center"
            },
            {
                "timestamp": "2024-01-23T14:00:00Z",
                "status": "in_transit", 
                "location": "In Transit",
                "description": "Shipment in transit to destination country"
            },
        ]
    }

@router.get("/track/order/{order_id}")
async def track_order(order_id: str):
    """Track order by order ID"""
    tracking = next((t for t in TRACKING_EVENTS if t.get("order_id") == order_id), None)
    if tracking:
        return tracking
    
    # Return mock for unknown orders
    return {
        "order_id": order_id,
        "tracking_number": f"TRK{uuid.uuid4().hex[:10].upper()}",
        "carrier": "DHL",
        "status": "processing",
        "events": [
            {
                "timestamp": "2024-01-22T10:00:00Z",
                "status": "processing",
                "location": "Warehouse",
                "description": "Order being prepared for shipment"
            }
        ]
    }

@router.get("/estimates")
async def estimate_delivery(origin: str = "CN", destination: str = "FR"):
    """Estimate delivery times"""
    estimates = []
    for carrier in CARRIERS:
        if destination.upper() in carrier["countries"]:
            estimates.append({
                "carrier": carrier["name"],
                "delivery_time": carrier["delivery_time"],
                "reliability": "95%",
            })
    return {"estimates": estimates}

@router.post("/label")
async def create_shipping_label(order_id: str, carrier_id: str):
    """Create shipping label"""
    order = {"order_id": order_id}
    
    label = {
        "label_id": f"LBL{uuid.uuid4().hex[:10].upper()}",
        "order_id": order_id,
        "carrier": carrier_id,
        "tracking_number": f"TRK{uuid.uuid4().hex[:10].upper()}",
        "label_url": f"/api/v1/labels/{order_id}.pdf",
        "created_at": "2024-01-22T10:00:00Z",
    }
    
    return {"label": label, "success": True}