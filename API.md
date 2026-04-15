# API Reference - E-Battisseurs by ELECTRON

Base URL: `https://api.e-battisseurs.com` (prod) ou `http://localhost:8000` (dev)

## Authentication

Currently public for demo. JWT auth coming soon.

## Endpoints

### M-01 Products (Vitrine)
```
GET /api/v1/products
GET /api/v1/products/{id}
GET /api/v1/categories
GET /api/v1/featured
```

### M-03 Orders
```
GET /api/v1/orders
GET /api/v1/orders/{id}
POST /api/v1/orders
PATCH /api/v1/orders/{id}/status
GET /api/v1/orders/{id}/tracking
GET /api/v1/stats
```

### M-04 Logistics
```
GET /api/v1/carriers
GET /api/v1/rates?origin_country=CN&destination_country=FR&weight=1.0
GET /api/v1/track/{tracking_number}
POST /api/v1/label
```

### M-05 Payments
```
GET /api/v1/payments
POST /api/v1/payments/create-intent
POST /api/v1/payments/confirm
POST /api/v1/payments/refund
GET /api/v1/methods
```

### M-06 Marketing
```
GET /api/v1/campaigns
GET /api/v1/campaigns/{id}
POST /api/v1/campaigns
POST /api/v1/campaigns/{id}/send
GET /api/v1/templates
```

### M-07 CRM
```
GET /api/v1/customers
GET /api/v1/customers/{id}
POST /api/v1/customers
GET /api/v1/tickets
POST /api/v1/tickets
POST /api/v1/tickets/{id}/respond
GET /api/v1/chatbot?message=...
```

### M-08 Suppliers
```
GET /api/v1/suppliers
GET /api/v1/suppliers/{id}/products
GET /api/v1/search?q=...
GET /api/v1/products/{id}
```

### M-09 Analytics
```
GET /api/v1/dashboard
GET /api/v1/revenue?period=30d
GET /api/v1/top-products
GET /api/v1/top-countries
```

### M-10 Compliance
```
GET /api/v1/restrictions?country=FR
GET /api/v1/taxes?country=FR
GET /api/v1/compliance/check?product_category=electronics&destination_country=FR
GET /api/v1/certifications
```

### M-11 Affiliate
```
GET /api/v1/affiliates
POST /api/v1/affiliates
GET /api/v1/resellers
POST /api/v1/resellers
GET /api/v1/links?affiliate_id=...
```

### M-12 IA Orchestrator
```
GET /api/v1/agents
POST /api/v1/agents/{id}/run
POST /api/v1/agents/run-all
GET /api/v1/history
GET /api/v1/status
GET /api/v1/workflows
```

## Example Usage

```bash
# Get products
curl http://localhost:8000/api/v1/products

# Search suppliers
curl "http://localhost:8000/api/v1/search?q=watch"

# Calculate shipping
curl "http://localhost:8000/api/v1/rates?origin_country=CN&destination_country=FR&weight=1.0"

# Create order
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"cust-001","items":[...],"shipping_address":{...}}'
```