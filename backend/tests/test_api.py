"""Tests for E-Battisseurs API"""
import pytest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/workspace/E-Battisseurs/backend')

from main import app

client = TestClient(app)


def test_health():
    """Test health endpoint"""
    response = client.get("/api/v1/stats")
    assert response.status_code == 200


def test_products():
    """Test products endpoint"""
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data


def test_suppliers():
    """Test suppliers endpoint"""
    response = client.get("/api/v1/suppliers")
    assert response.status_code == 200


def test_carriers():
    """Test carriers endpoint"""
    response = client.get("/api/v1/carriers")
    assert response.status_code == 200


def test_dashboard():
    """Test dashboard endpoint"""
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200


def test_agents():
    """Test agents endpoint"""
    response = client.get("/api/v1/agents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 12


def test_search():
    """Test search endpoint"""
    response = client.get("/api/v1/search?q=watch")
    assert response.status_code == 200


def test_auth_login():
    """Test login endpoint"""
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@ebattisseurs.com",
        "password": "admin"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_auth_login_invalid():
    """Test login with invalid credentials"""
    response = client.post("/api/v1/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_auth_register():
    """Test register endpoint"""
    response = client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com",
        "password": "password123",
        "name": "New User"
    })
    assert response.status_code == 200


def test_affiliates():
    """Test affiliates endpoint"""
    response = client.get("/api/v1/affiliates")
    assert response.status_code == 200


def test_campaigns():
    """Test campaigns endpoint"""
    response = client.get("/api/v1/campaigns")
    assert response.status_code == 200


def test_tickets():
    """Test tickets endpoint"""
    response = client.get("/api/v1/tickets")
    assert response.status_code == 200