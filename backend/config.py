"""Configuration settings for GLOBALSHIP PRO"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    # App
    APP_NAME: str = "GLOBALSHIP PRO"
    ENVIRONMENT: str = "development"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/globalship"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Supplier APIs
    ALIEXPRESS_API_KEY: Optional[str] = None
    ALIEXPRESS_API_SECRET: Optional[str] = None
    CJ_DROPSHIPPING_API_KEY: Optional[str] = None
    ALIBABA_API_KEY: Optional[str] = None
    AMAZON_API_KEY: Optional[str] = None
    
    # Payment Gateways
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    
    # Logistics
    DHL_API_KEY: Optional[str] = None
    FEDEX_API_KEY: Optional[str] = None
    UPS_API_KEY: Optional[str] = None
    
    # AI
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    N8N_WEBHOOK_URL: Optional[str] = None
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]


settings = Settings()