# UniERP API Reference Documentation

## Overview

This comprehensive API reference provides developers with detailed information about UniERP's REST API, RPC methods, and integration endpoints for building custom applications and integrations.

## Table of Contents

1. [Authentication](#authentication)
2. [REST API Endpoints](#rest-api-endpoints)
3. [RPC Methods](#rpc-methods)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Webhooks](#webhooks)
8. [Response Formats](#response-formats)
9. [Examples](#examples)
10. [Best Practices](#best-practices)

## Authentication

### API Key Authentication

UniERP API uses API key authentication for secure access:

```http
GET /api/v1/auth
Authorization: Bearer your_api_key_here
Content-Type: application/json
```

### Session Authentication

For web applications, use session-based authentication:

```http
POST /web/session/authenticate
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "common",
        "method": "login",
        "args": ["database", "username", "password"]
    }
}
```

### OAuth2 Authentication

For third-party integrations:

```http
GET /api/v1/oauth/authorize
?client_id=your_client_id
&redirect_uri=https://your-app.com/callback
&response_type=code
&scope=read write
```

## REST API Endpoints

### Base URL

```
Production: https://api.unierp.com
Development: https://api-dev.unierp.com
```

### Common Endpoints

#### Users API

```http
# Get current user
GET /api/v1/user/me
Authorization: Bearer {api_key}

# Get user by ID
GET /api/v1/users/{id}
Authorization: Bearer {api_key}

# Create user
POST /api/v1/users
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "name": "John Doe",
    "email": "john@example.com",
    "login": "john.doe",
    "groups_id": [1, 2]
}

# Update user
PUT /api/v1/users/{id}
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "name": "John Smith",
    "email": "john.smith@example.com"
}

# Delete user
DELETE /api/v1/users/{id}
Authorization: Bearer {api_key}
```

#### Partners API

```http
# List partners
GET /api/v1/partners
Authorization: Bearer {api_key}
?limit=20&offset=0&filter=customer

# Get partner details
GET /api/v1/partners/{id}
Authorization: Bearer {api_key}

# Create partner
POST /api/v1/partners
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "name": "Customer Name",
    "email": "customer@example.com",
    "is_company": true,
    "street": "123 Main St",
    "city": "Anytown",
    "country_id": 233
}

# Search partners
POST /api/v1/partners/search
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "domain": [["name", "ilike", "customer"]],
    "limit": 10,
    "order": "name asc"
}
```

#### Sales API

```http
# List sales orders
GET /api/v1/sales/orders
Authorization: Bearer {api_key}
?state=sale&limit=50

# Create sales order
POST /api/v1/sales/orders
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "partner_id": 123,
    "order_line": [
        {
            "product_id": 456,
            "quantity": 2,
            "price_unit": 99.99
        }
    ],
    "validity_date": "2024-01-15"
}

# Confirm sales order
POST /api/v1/sales/orders/{id}/confirm
Authorization: Bearer {api_key}
```

#### Inventory API

```http
# Get products
GET /api/v1/products
Authorization: Bearer {api_key}
?category=stockable&limit=100

# Update stock
POST /api/v1/stock/update
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "product_id": 789,
    "location_id": 12,
    "quantity": 50,
    "operation": "set"
}

# Stock movements
GET /api/v1/stock/moves
Authorization: Bearer {api_key}
?product_id=789&from_date=2024-01-01
```

## RPC Methods

### JSON-RPC Endpoint

```
POST /jsonrpc
Content-Type: application/json
{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "service": "object",
        "method": "execute_kw",
        "args": [
            "database",
            "uid",
            "password",
            "res.partner",
            "search_read",
            [],
            {"fields": ["name", "email", "phone"]}
        ]
    }
}
```

### Common RPC Methods

#### Search Records

```javascript
// Search partners
odoo.rpc('/web/dataset/call_kw', {
    model: 'res.partner',
    method: 'search_read',
    args: [[['is_company', '=', true]], ['name', 'email'], 0, 100],
    kwargs: {}
}).then(function(result) {
    console.log('Partners:', result);
});
```

#### Create Records

```javascript
// Create partner
odoo.rpc('/web/dataset/call_kw', {
    model: 'res.partner',
    method: 'create',
    args: [{
        name: 'New Company',
        email: 'info@company.com',
        is_company: true
    }]
}).then(function(result) {
    console.log('Created partner:', result);
});
```

#### Update Records

```javascript
// Update partner
odoo.rpc('/web/dataset/call_kw', {
    model: 'res.partner',
    method: 'write',
    args: [123, {
        phone: '+1234567890',
        website: 'https://company.com'
    }]
}).then(function(result) {
    console.log('Updated partner:', result);
});
```

#### Delete Records

```javascript
// Delete partner
odoo.rpc('/web/dataset/call_kw', {
    model: 'res.partner',
    method: 'unlink',
    args: [[123, 124]]
}).then(function(result) {
    console.log('Deleted partners:', result);
});
```

## Data Models

### Core Models

#### User Model (res.users)

```json
{
    "id": 1,
    "name": "Administrator",
    "login": "admin",
    "email": "admin@company.com",
    "company_id": {
        "id": 1,
        "name": "Your Company"
    },
    "groups_id": [
        {
            "id": 1,
            "name": "Access Rights"
        }
    ],
    "active": true,
    "share": false,
    "create_date": "2024-01-01T00:00:00Z",
    "write_date": "2024-01-01T00:00:00Z"
}
```

#### Partner Model (res.partner)

```json
{
    "id": 123,
    "name": "Customer Name",
    "email": "customer@example.com",
    "phone": "+1234567890",
    "is_company": false,
    "street": "123 Main St",
    "city": "Anytown",
    "country_id": {
        "id": 233,
        "name": "United States"
    },
    "commercial_partner_id": null,
    "active": true,
    "create_date": "2024-01-01T00:00:00Z",
    "write_date": "2024-01-01T00:00:00Z"
}
```

#### Product Model (product.product)

```json
{
    "id": 456,
    "name": "Product Name",
    "default_code": "PROD001",
    "type": "product",
    "categ_id": {
        "id": 1,
        "name": "All Products"
    },
    "list_price": 99.99,
    "cost": 50.00,
    "uom_id": {
        "id": 1,
        "name": "Units"
    },
    "qty_available": 100,
    "active": true,
    "sale_ok": true,
    "purchase_ok": true
}
```

#### Sales Order Model (sale.order)

```json
{
    "id": 789,
    "name": "SO001",
    "state": "sale",
    "partner_id": {
        "id": 123,
        "name": "Customer Name"
    },
    "order_line": [
        {
            "id": 101,
            "product_id": {
                "id": 456,
                "name": "Product Name"
            },
            "product_uom_qty": 2.0,
            "price_unit": 99.99,
            "price_total": 199.98
        }
    ],
    "amount_total": 199.98,
    "amount_untaxed": 199.98,
    "date_order": "2024-01-15",
    "validity_date": "2024-01-15",
    "create_date": "2024-01-15T00:00:00Z"
}
```

## Error Handling

### HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Authentication failed
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error occurred

### Error Response Format

```json
{
    "error": {
        "code": "validation_error",
        "message": "Invalid email format",
        "data": {
            "field": "email",
            "value": "invalid-email",
            "expected": "user@example.com"
        }
    },
    "jsonrpc": "2.0",
    "id": null
}
```

### Common Error Codes

| Code | Message | Description |
|-------|----------|-------------|
| `validation_error` | Invalid input data |
| `authentication_failed` | Invalid credentials |
| `permission_denied` | Insufficient access rights |
| `resource_not_found` | Resource does not exist |
| `rate_limit_exceeded` | Too many requests |
| `server_error` | Internal server error |
| `maintenance_mode` | System under maintenance |

## Rate Limiting

### Default Limits

- **Authenticated requests**: 1000 per hour
- **Unauthenticated requests**: 100 per hour
- **Bulk operations**: 100 per hour
- **File uploads**: 50 per hour

### Rate Limit Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

### Rate Limit Response

```json
{
    "error": {
        "code": "rate_limit_exceeded",
        "message": "Rate limit exceeded. Try again later.",
        "retry_after": 1640995200
    }
}
```

## Webhooks

### Webhook Configuration

```http
POST /api/v1/webhooks
Authorization: Bearer {api_key}
Content-Type: application/json
{
    "name": "Order Status Updates",
    "url": "https://your-app.com/webhook",
    "events": ["order.created", "order.confirmed", "order.cancelled"],
    "active": true,
    "secret": "webhook_secret_key"
}
```

### Webhook Events

#### Order Events
- `order.created`: New sales order created
- `order.confirmed`: Sales order confirmed
- `order.cancelled`: Sales order cancelled
- `order.paid`: Payment received

#### Partner Events
- `partner.created`: New partner created
- `partner.updated`: Partner information updated

#### Inventory Events
- `product.low_stock`: Product stock below threshold
- `stock.movement`: Inventory movement occurred

### Webhook Payload Example

```json
{
    "event": "order.created",
    "timestamp": "2024-01-15T10:30:00Z",
    "data": {
        "order_id": 789,
        "name": "SO001",
        "partner_id": 123,
        "amount_total": 199.98,
        "state": "sale"
    },
    "signature": "sha256_hash_here"
}
```

### Webhook Verification

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    """Verify webhook signature"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)
```

## Response Formats

### Success Response

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "id": 123,
        "name": "Success Result",
        "data": [...]
    }
}
```

### Paginated Response

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "records": [...],
        "length": 150,
        "records_per_page": 20,
        "page": 1,
        "pages": 8
    }
}
```

### File Response

```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="export.csv"
Content-Length: 1024

CSV file content here...
```

## Examples

### JavaScript Integration

```javascript
// UniERP API client setup
class UniERPClient {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }
    
    async request(method, endpoint, data = null) {
        const url = `${this.baseUrl}/api/v1${endpoint}`;
        const options = {
            method: method,
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        return response.json();
    }
    
    async getPartners(limit = 20) {
        return this.request('GET', `/partners?limit=${limit}`);
    }
    
    async createPartner(partnerData) {
        return this.request('POST', '/partners', partnerData);
    }
}

// Usage
const client = new UniERPClient('https://api.unierp.com', 'your_api_key');

client.getPartners().then(partners => {
    console.log('Partners:', partners);
});

client.createPartner({
    name: 'New Customer',
    email: 'customer@example.com'
}).then(result => {
    console.log('Created:', result);
});
```

### Python Integration

```python
import requests
import json

class UniERPAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def request(self, method, endpoint, data=None):
        url = f'{self.base_url}/api/v1{endpoint}'
        
        if method.upper() == 'GET':
            response = self.session.get(url, params=data)
        elif method.upper() == 'POST':
            response = self.session.post(url, json=data)
        elif method.upper() == 'PUT':
            response = self.session.put(url, json=data)
        elif method.upper() == 'DELETE':
            response = self.session.delete(url)
        else:
            raise ValueError(f'Unsupported method: {method}')
        
        response.raise_for_status()
        return response.json()
    
    def get_partners(self, limit=20, offset=0):
        return self.request('GET', '/partners', {
            'limit': limit,
            'offset': offset
        })
    
    def create_partner(self, partner_data):
        return self.request('POST', '/partners', partner_data)

# Usage
api = UniERPAPI('https://api.unierp.com', 'your_api_key')

# Get partners
partners = api.get_partners(limit=50)
print(f'Found {len(partners)} partners')

# Create partner
new_partner = api.create_partner({
    'name': 'Python Customer',
    'email': 'python@example.com',
    'is_company': True
})
print(f'Created partner with ID: {new_partner["id"]}')
```

## Best Practices

### Security

1. **Use HTTPS**: Always use encrypted connections
2. **Protect API Keys**: Never expose keys in client-side code
3. **Validate Input**: Sanitize all user inputs
4. **Use Webhook Signatures**: Verify webhook authenticity
5. **Implement Rate Limiting**: Respect API limits
6. **Log Requests**: Monitor API usage and errors

### Performance

1. **Batch Operations**: Use bulk endpoints when possible
2. **Cache Responses**: Cache frequently accessed data
3. **Use Compression**: Enable gzip compression
4. **Limit Fields**: Request only needed fields
5. **Pagination**: Use pagination for large datasets

### Error Handling

1. **Check Status Codes**: Handle all HTTP status codes appropriately
2. **Parse Error Responses**: Extract meaningful error messages
3. **Implement Retries**: Handle temporary failures gracefully
4. **Log Errors**: Record errors for debugging
5. **User Feedback**: Provide clear error messages to users

### Integration Patterns

1. **Async Operations**: Use async/await for better performance
2. **Connection Pooling**: Reuse connections when possible
3. **Timeout Handling**: Set appropriate timeouts
4. **Backoff Strategy**: Implement exponential backoff for retries
5. **Graceful Degradation**: Handle service unavailability

## SDK and Libraries

### Official SDKs

- **JavaScript**: `npm install @unierp/api-client`
- **Python**: `pip install unierp-api-client`
- **PHP**: `composer require unierp/api-client`
- **Java**: Maven dependency available

### Community Libraries

Check the UniERP marketplace for community-maintained libraries and integrations.

## Support and Resources

- **API Documentation**: https://www.uslbd.com/api/docs
- **Developer Forum**: https://www.uslbd.com/community/developer
- **Support Tickets**: https://www.uslbd.com/support
- **Status Page**: https://status.unierp.com
- **Changelog**: https://www.uslbd.com/api/changelog

---

This comprehensive API reference provides developers with all the necessary information to build robust integrations with UniERP, following best practices for security, performance, and reliability.