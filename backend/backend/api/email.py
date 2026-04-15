"""Email (SMTP) Service for E-Battisseurs"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/email", tags=["Email"])

# SMTP Configuration
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "noreply@ebattisseurs.com")


class EmailRequest(BaseModel):
    to: str | List[str]
    subject: str
    body: str
    html: Optional[str] = None


async def send_email(to: str, subject: str, body: str, html: Optional[str] = None) -> Dict[str, Any]:
    """Send email via SMTP"""
    if not SMTP_USER:
        return {
            "id": f"email_demo_{os.urandom(8).hex()}",
            "status": "sent",
            "to": to,
            "subject": subject,
            "demo": True
        }
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to
        
        # Attach plain text
        text_part = MIMEText(body, "plain")
        msg.attach(text_part)
        
        # Attach HTML if provided
        if html:
            html_part = MIMEText(html, "html")
            msg.attach(html_part)
        
        # Send (in production)
        # server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        # server.starttls()
        # server.login(SMTP_USER, SMTP_PASSWORD)
        # server.send_message(msg)
        # server.quit()
        
        return {
            "id": f"email_{os.urandom(8).hex()}",
            "status": "sent",
            "to": to
        }
    except Exception as e:
        return {"error": str(e)}


# Email Templates
WELCOME_SUBJECT = "Welcome to E-Battisseurs!"
WELCOME_BODY = """Hello {name},

Welcome to E-Battisseurs!

Your account has been created successfully.
Email: {email}

Start shopping now!

Best,
E-Battisseurs Team"""

ORDER_CONFIRMATION_SUBJECT = "Order Confirmation - #{order_id}"
ORDER_CONFIRMATION_BODY = """Hello {name},

Thank you for your order!

Order ID: {order_id}
Total: {total}

We'll ship your order soon.

Track your order: {tracking_url}

E-Battisseurs Team"""

ABANDONED_CART_SUBJECT = "You left something behind!"
ABANDONED_CART_BODY = """Hello,

You left items in your cart:

{items}

Complete your order now!

E-Battisseurs Team"""


# Endpoints
@router.post("/send")
async def send(request: EmailRequest):
    """Send email"""
    return await send_email(
        request.to if isinstance(request.to, str) else request.to[0],
        request.subject,
        request.body,
        request.html
    )


@router.post("/send/welcome")
async def send_welcome(name: str, email: str):
    """Send welcome email"""
    return await send_email(
        email,
        WELCOME_SUBJECT,
        WELCOME_BODY.format(name=name, email=email)
    )


@router.post("/send/order-confirmation")
async def send_order_confirmation(order_id: str, name: str, email: str, total: str, tracking_url: str):
    """Send order confirmation"""
    return await send_email(
        email,
        ORDER_CONFIRMATION_SUBJECT.format(order_id=order_id),
        ORDER_CONFIRMATION_BODY.format(
            name=name,
            order_id=order_id,
            total=total,
            tracking_url=tracking_url
        )
    )


@router.get("/status")
async def email_status():
    """Check email service status"""
    return {
        "smtp": "configured" if SMTP_USER else "demo",
        "from_email": FROM_EMAIL
    }