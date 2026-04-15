"""M-10 Compliance - Moteur de conformité"""
from fastapi import APIRouter
from typing import Optional, List, Dict
from pydantic import BaseModel

router = APIRouter()

# Models
class ImportRestriction(BaseModel):
    country: str
    product_category: str
    allowed: bool
    notes: str

class TaxRule(BaseModel):
    country: str
    vat_rate: float
    threshold: float  # Threshold for VAT registration

# Customs restrictions by country
RESTRICTIONS = [
    {"country": "FR", "product_category": "electronics", "allowed": True, "notes": "CE required"},
    {"country": "FR", "product_category": "cosmetics", "allowed": True, "notes": "CPNP notification required"},
    {"country": "US", "product_category": "electronics", "allowed": True, "notes": "FCC certification"},
    {"country": "US", "product_category": "food", "allowed": False, "notes": "FDA approval required"},
    {"country": "CN", "product_category": "electronics", "allowed": True, "notes": "CCC required"},
    {"country": "BR", "product_category": "toys", "allowed": True, "notes": "INMETRO certification"},
    {"country": "DE", "product_category": "electronics", "allowed": True, "notes": "CE + RoHS required"},
]

# Tax rules by country
TAX_RULES = [
    {"country": "FR", "vat_rate": 20.0, "threshold": 0},
    {"country": "DE", "vat_rate": 19.0, "threshold": 0},
    {"country": "GB", "vat_rate": 20.0, "threshold": 0},
    {"country": "US", "vat_rate": 0.0, "threshold": 800},  # No federal VAT
    {"country": "CN", "vat_rate": 13.0, "threshold": 0},
    {"country": "BJ", "vat_rate": 18.0, "threshold": 0},  # Benin
    {"country": "SN", "vat_rate": 18.0, "threshold": 0},  # Senegal
    {"country": "CI", "vat_rate": 18.0, "threshold": 0},  # Ivory Coast
]

# Certifications
CERTIFICATIONS = [
    {"id": "ce", "name": "CE Marking", "regions": ["EU", "EEA"], "categories": ["electronics", "toys", "machinery"]},
    {"id": "fcc", "name": "FCC Certification", "regions": ["US"], "categories": ["electronics"]},
    {"id": "fda", "name": "FDA Approval", "regions": ["US"], "categories": ["food", "cosmetics", "health"]},
    {"id": "ccc", "name": "CCC Certification", "regions": ["CN"], "categories": ["electronics"]},
    {"id": "inmetro", "name": "INMETRO", "regions": ["BR"], "categories": ["toys", "electronics"]},
    {"id": "cpnp", "name": "CPNP Notification", "regions": ["EU"], "categories": ["cosmetics"]},
]

@router.get("/restrictions", response_model=List[dict])
async def get_restrictions(country: Optional[str] = None):
    """Get import restrictions by country"""
    if country:
        return [r for r in RESTRICTIONS if r["country"] == country.upper()]
    return RESTRICTIONS

@router.get("/restrictions/{country}/{category}")
async def check_restriction(country: str, category: str):
    """Check if product can be imported"""
    restriction = next(
        (r for r in RESTRICTIONS if r["country"] == country.upper() and r["product_category"] == category.lower()),
        None
    )
    if not restriction:
        return {"allowed": True, "notes": "No specific restrictions found"}
    return restriction

@router.get("/taxes", response_model=List[dict])
async def get_tax_rules(country: Optional[str] = None):
    """Get tax rules by country"""
    if country:
        return [t for t in TAX_RULES if t["country"] == country.upper()]
    return TAX_RULES

@router.get("/taxes/calculate")
async def calculate_tax(amount: float, country: str):
    """Calculate tax for amount"""
    rule = next((t for t in TAX_RULES if t["country"] == country.upper()), None)
    if not rule:
        return {"amount": amount, "tax": 0, "total": amount, "vat_rate": 0}
    
    tax = amount * (rule["vat_rate"] / 100)
    total = amount + tax
    
    return {
        "amount": round(amount, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "vat_rate": rule["vat_rate"],
        "country": country.upper(),
    }

@router.get("/certifications", response_model=List[dict])
async def get_certifications(category: Optional[str] = None):
    """Get required certifications"""
    if category:
        return [c for c in CERTIFICATIONS if category.lower() in c["categories"]]
    return CERTIFICATIONS

@router.get("/compliance/check")
async def check_compliance(product_category: str, destination_country: str):
    """Full compliance check"""
    restriction = next(
        (r for r in RESTRICTIONS if r["country"] == destination_country.upper() and r["product_category"] == product_category.lower()),
        None
    )
    
    tax_rule = next((t for t in TAX_RULES if t["country"] == destination_country.upper()), None)
    
    certifications = [c for c in CERTIFICATIONS if product_category.lower() in c["categories"] and destination_country.upper() in c["regions"]]
    
    return {
        "product_category": product_category,
        "destination": destination_country.upper(),
        "import_allowed": restriction["allowed"] if restriction else True,
        "import_notes": restriction["notes"] if restriction else "No restrictions",
        "vat_rate": tax_rule["vat_rate"] if tax_rule else 0,
        "required_certifications": [c["id"] for c in certifications],
        "compliant": (restriction["allowed"] if restriction else True) and len(certifications) >= 0,
    }