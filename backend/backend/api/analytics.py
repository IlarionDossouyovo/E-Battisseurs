"""M-09 Analytics Pro"""
from fastapi import APIRouter
from typing import List, Optional
from datetime import datetime, timedelta
import random

router = APIRouter()

# Mock analytics data
@router.get("/dashboard")
async def get_dashboard():
    """Get analytics dashboard"""
    return {
        "period": "last_30_days",
        "revenue": {
            "total": 125000.00,
            "change": 15.3,
            "currency": "USD",
        },
        "orders": {
            "total": 3420,
            "change": 22.1,
            "pending": 45,
            "processing": 120,
            "shipped": 890,
            "delivered": 2365,
        },
        "customers": {
            "total": 2850,
            "new": 456,
            "returning": 2394,
        },
        "conversion_rate": 3.2,
        "average_order_value": 36.55,
    }

@router.get("/revenue")
async def get_revenue(period: str = "30d"):
    """Get revenue analytics"""
    days = int(period.rstrip("d")) if period.endswith("d") else 30
    
    data = []
    base_revenue = 4000
    for i in range(days):
        date = datetime.utcnow() - timedelta(days=days - i - 1)
        revenue = base_revenue + random.uniform(-500, 1500)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "revenue": round(revenue, 2),
            "orders": random.randint(80, 150),
        })
    
    return {"data": data, "period": period}

@router.get("/top-products")
async def get_top_products(limit: int = 10):
    """Get top selling products"""
    return {
        "products": [
            {"id": "prod-001", "title": "Smart Watch Fitness Tracker", "revenue": 15600, "orders": 520},
            {"id": "prod-002", "title": "Wireless Earbuds Pro", "revenue": 12300, "orders": 307},
            {"id": "prod-003", "title": "Lampe de Bureau LED USB", "revenue": 8900, "orders": 556},
            {"id": "prod-004", "title": "USB-C Hub 7-en-1", "revenue": 6700, "orders": 223},
            {"id": "prod-005", "title": "Power Bank 20000mAh", "revenue": 5400, "orders": 180},
        ][:limit]
    }

@router.get("/top-countries")
async def get_top_countries():
    """Get revenue by country"""
    return {
        "countries": [
            {"code": "US", "name": "United States", "revenue": 45000, "orders": 1200},
            {"code": "FR", "name": "France", "revenue": 28000, "orders": 750},
            {"code": "GB", "name": "United Kingdom", "revenue": 22000, "orders": 580},
            {"code": "DE", "name": "Germany", "revenue": 18000, "orders": 450},
            {"code": "CA", "name": "Canada", "revenue": 12000, "orders": 320},
        ]
    }

@router.get("/customers")
async def get_customer_analytics():
    """Get customer analytics"""
    return {
        "total_customers": 2850,
        "new_customers_30d": 456,
        "customer_lifetime_value": {
            "average": 156.00,
            "top_10": 2500.00,
        },
        "retention_rate": 78.5,
        "top_countries": [
            {"country": "US", "customers": 950},
            {"country": "FR", "customers": 650},
            {"country": "GB", "customers": 420},
        ]
    }

@router.get("/marketing")
async def get_marketing_analytics():
    """Get marketing performance"""
    return {
        "campaigns": [
            {"name": "Spring Sale", "spend": 2500, "revenue": 12500, "roi": 5.0},
            {"name": "Facebook Ads", "spend": 1800, "revenue": 7200, "roi": 4.0},
            {"name": "Influencer Promo", "spend": 1000, "revenue": 4500, "roi": 4.5},
        ],
        "channel_performance": [
            {"channel": "Organic Search", "sessions": 15000, "conversions": 450},
            {"channel": "Paid Social", "sessions": 8500, "conversions": 340},
            {"channel": "Email", "sessions": 4200, "conversions": 210},
            {"channel": "Direct", "sessions": 3800, "conversions": 152},
        ]
    }

@router.get("/reports")
async def get_reports():
    """Available report types"""
    return {
        "reports": [
            {"id": "sales", "name": "Sales Report", "description": "Daily sales summary"},
            {"id": "inventory", "name": "Inventory Report", "description": "Stock levels"},
            {"id": "financial", "name": "Financial Report", "description": "Revenue and profit"},
            {"id": "customer", "name": "Customer Report", "description": "Customer metrics"},
        ]
    }