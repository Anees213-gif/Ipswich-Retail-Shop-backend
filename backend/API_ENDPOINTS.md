# API Endpoints Documentation

## Frontend API Calls → Backend Endpoints Mapping

### Public Endpoints

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|---------|-------------|
| `api.getProducts()` | `/api/products/` | GET | List products with filtering |
| `api.getProduct(slug)` | `/api/products/{slug}/` | GET | Get product by slug |
| `api.getCategories()` | `/api/categories/` | GET | List categories |
| `api.createOrder()` | `/api/orders/` | POST | Create new order |

### Admin Endpoints

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|---------|-------------|
| `api.getDashboardStats()` | `/api/admin/dashboard/stats/` | GET | Dashboard statistics |
| `api.getOrders()` | `/api/admin/orders/` | GET | List orders with filtering |
| `api.updateOrder()` | `/api/admin/orders/{order_number}/update/` | PATCH | Update order status |
| `api.getAdminProducts()` | `/api/admin/products/` | GET | List products for admin |
| `api.createProduct()` | `/api/admin/products/create/` | POST | Create new product |
| `api.updateProduct()` | `/api/admin/products/{id}/update/` | PATCH | Update product |

### Authentication Endpoints

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|---------|-------------|
| Admin Login | `/api/admin/auth/login/` | POST | Admin authentication |
| Admin Logout | `/api/admin/auth/logout/` | POST | Admin logout |
| User Info | `/api/admin/auth/user/` | GET | Get current user info |

### Customer Endpoints

| Frontend Call | Backend Endpoint | Method | Description |
|---------------|------------------|---------|-------------|
| Customer List | `/api/admin/customers/` | GET | List customers |
| Customer Stats | `/api/admin/customers/stats/` | GET | Customer statistics |

## Query Parameters Support

### Products Filtering
- `page` - Page number
- `page_size` - Items per page
- `category` - Filter by category slug
- `search` - Search in name/description
- `featured` - Filter featured products
- `sortBy` - Sort by field (name, price, rating, created_at)
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `min_rating` - Minimum rating filter

### Orders Filtering
- `page` - Page number
- `pageSize` - Items per page
- `status` - Filter by order status
- `search` - Search in order number/email
- `sortBy` - Sort by field (total, status, createdAt)
- `sortOrder` - Sort order (asc, desc)

### Admin Products Filtering
- `page` - Page number
- `pageSize` - Items per page
- `category` - Filter by category
- `search` - Search in name/description
- `inStock` - Filter by stock status

## Response Formats

### Product Response
```json
{
  "id": 1,
  "name": "Product Name",
  "slug": "product-name",
  "description": "Product description",
  "price": "299.99",
  "original_price": "399.99",
  "category": {
    "id": 1,
    "name": "Electronics",
    "slug": "electronics"
  },
  "stock_count": 25,
  "is_active": true,
  "is_featured": true,
  "rating": "4.8",
  "review_count": 156,
  "in_stock": true,
  "discount_percentage": 25,
  "images": [...],
  "specifications": [...],
  "tags": [...]
}
```

### Order Response
```json
{
  "id": 1,
  "order_number": "ORD-ABC123",
  "customer_email": "customer@example.com",
  "customer_first_name": "John",
  "customer_last_name": "Doe",
  "total_amount": "299.99",
  "status": "pending",
  "items": [...],
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Dashboard Stats Response
```json
{
  "ordersToday": 12,
  "revenueToday": 2847.50,
  "avgOrderValue": 237.29,
  "errorRate": 0.5,
  "ordersLast7Days": [
    {"date": "2024-01-09", "orders": 8},
    {"date": "2024-01-10", "orders": 12}
  ]
}
```

## Authentication

All admin endpoints require authentication. Use session-based authentication:

1. POST to `/api/admin/auth/login/` with email/password
2. Include session cookie in subsequent requests
3. POST to `/api/admin/auth/logout/` to logout

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Error message",
  "details": {...}
}
```

Status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error
