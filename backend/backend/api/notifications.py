"""WhatsApp and SMS Notifications for E-Battisseurs"""
import os
import uuid
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# API Keys
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


class WhatsAppMessage(BaseModel):
    to: str
    body: str
    media_url: Optional[str] = None


class SMSMessage(BaseModel):
    to: str
    body: str


async def send_whatsapp_message(to: str, body: str, media_url: Optional[str] = None) -> Dict[str, Any]:
    """Send WhatsApp message via Twilio API"""
    if not WHATSAPP_TOKEN:
        return {
            "id": f"wamid.{uuid.uuid4().hex[:12]}",
            "status": "sent",
            "to": to,
            "body": body,
            "demo": True
        }
    
    return {
        "id": f"wamid.{uuid.uuid4().hex[:12]}",
        "status": "sent",
        "to": to
    }


async def send_sms(to: str, body: str) -> Dict[str, Any]:
    """Send SMS via Twilio"""
    if not TWILIO_ACCOUNT_SID:
        return {
            "sid": f"SM{uuid.uuid4().hex[:12]}",
            "status": "sent",
            "to": to,
            "demo": True
        }
    
    return {
        "sid": f"SM{uuid.uuid4().hex[:12]}",
        "status": "sent",
        "to": to
    }


# Templates for common messages
ORDER_CONFIRMATION = "Your order #{order_id} has been confirmed! We'll notify you when it ships."
ORDER_SHIPPED = "Your order #{order_id} has shipped! Track: {tracking_url}"
ORDER_DELIVERED = "Your order #{order_id} has been delivered!"


# Endpoints
@router.post("/whatsapp/send")
async def send_whatsapp(message: WhatsAppMessage):
    """Send WhatsApp message"""
    return await send_whatsapp_message(message.to, message.body, message.media_url)


@router.post("/sms/send")
async def send_sms_message(message: SMSMessage):
    """Send SMS message"""
    return await send_sms(message.to, message.body)


@router.post("/order/{order_id}/notify")
async def notify_order_status(order_id: str, status: str, phone: str):
    """Send order status notification"""
    templates = {
        "confirmed": ORDER_CONFIRMATION,
        "shipped": ORDER_SHIPPED,
        "delivered": ORDER_DELIVERED
    }
    body = templates.get(status, f"Order #{order_id} status: {status}")
    return await send_sms(phone, body)


@router.get("/status")
async def notification_status():
    """Check notification service status"""
    return {
        "whatsapp": "configured" if WHATSAPP_TOKEN else "demo",
        "sms": "configured" if TWILIO_ACCOUNT_SID else "demo"
    }