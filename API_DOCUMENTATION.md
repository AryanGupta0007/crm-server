# API Documentation

## Overview

This CRM system provides RESTful APIs for managing educational sales leads, user authentication, batch operations, and administrative functions.

## Base URL

```
http://localhost:8000/api
```

## Authentication

All API endpoints (except login) require JWT authentication.

### Login Endpoint
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "John Doe",
        "type": "sales",
        "is_admin": false
    }
}
```

### Using the Token
Include the access token in the Authorization header:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## Authentication API (`/api/auth/`)

### POST `/api/auth/login/`
Authenticate user and return JWT tokens.

**Request Body:**
```json
{
    "email": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "refresh": "string",
    "access": "string",
    "user": {
        "id": "integer",
        "email": "string",
        "name": "string",
        "type": "admin|sales|operations",
        "is_admin": "boolean"
    }
}
```

### POST `/api/auth/refresh/`
Refresh access token using refresh token.

**Request Body:**
```json
{
    "refresh": "string"
}
```

**Response:**
```json
{
    "access": "string"
}
```

### POST `/api/auth/register/`
Register a new user (admin only).

**Request Body:**
```json
{
    "email": "string",
    "name": "string",
    "contact": "string",
    "type": "sales|operations",
    "password": "string",
    "confirm_password": "string"
}
```

---

## Admin API (`/api/admin/`)

### GET `/api/admin/dashboard-stats/`
Get dashboard statistics.

**Response:**
```json
{
    "converted_leads": 5,
    "dnp_leads": 3,
    "active_leads": 12,
    "total_leads": 20
}
```

### GET `/api/admin/total-pages/`
Get total number of pages for lead pagination.

**Response:**
```json
{
    "total_pages": 4
}
```

### GET `/api/admin/getLeads/{page}/`
Get paginated list of leads.

**Path Parameters:**
- `page` (integer): Page number (1-based)

**Response:**
```json
{
    "msg": "Leads fetched",
    "leads": [
        {
            "id": 1,
            "name": "John Doe",
            "contact_number": "+12345678901",
            "source": "website",
            "status": "new",
            "assigned_to": {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com"
            },
            "created_at": "2024-01-01T10:00:00Z"
        }
    ]
}
```

### POST `/api/admin/leads/`
Create a new lead.

**Request Body:**
```json
{
    "name": "string",
    "contact_number": "string",
    "source": "website|referral|direct",
    "status": "new|contacted|interested|not_interested",
    "assigned_to": "integer (optional)"
}
```

**Response:**
```json
{
    "msg": "Lead created successfully",
    "lead": {
        "id": 1,
        "name": "John Doe",
        "contact_number": "+12345678901",
        "source": "website",
        "status": "new",
        "assigned_to": null
    }
}
```

### PATCH `/api/admin/leads/{id}/`
Update an existing lead.

**Path Parameters:**
- `id` (integer): Lead ID

**Request Body:**
```json
{
    "name": "string (optional)",
    "source": "string (optional)",
    "status": "string (optional)",
    "assigned_to": "integer (optional)"
}
```

**Response:**
```json
{
    "msg": "Lead updated successfully",
    "lead": {
        "id": 1,
        "name": "John Doe",
        "contact_number": "+12345678901",
        "source": "website",
        "status": "contacted",
        "assigned_to": 2
    }
}
```

### GET `/api/admin/leads/`
Get all leads (no pagination).

**Response:**
```json
{
    "leads": [
        {
            "id": 1,
            "name": "John Doe",
            "contact_number": "+12345678901",
            "source": "website",
            "status": "new"
        }
    ]
}
```

### POST `/api/admin/import-leads/`
Import leads from Excel file.

**Request Body (multipart/form-data):**
- `file`: Excel file (.xlsx, .xls, .csv)

**Response:**
```json
{
    "msg": "Leads imported successfully",
    "imported_count": 25
}
```

### GET `/api/admin/employees/`
Get all employees.

**Response:**
```json
{
    "employees": [
        {
            "id": 1,
            "user": {
                "id": 2,
                "email": "jane@example.com",
                "name": "Jane Smith"
            },
            "type": "sales",
            "allot": 50
        }
    ]
}
```

### PATCH `/api/admin/employees/{id}/`
Update employee details.

**Path Parameters:**
- `id` (integer): Employee ID

**Request Body:**
```json
{
    "type": "admin|sales|operations (optional)",
    "allot": "integer (optional)"
}
```

**Response:**
```json
{
    "msg": "Employee updated successfully",
    "employee": {
        "id": 1,
        "type": "sales",
        "allot": 75
    }
}
```

### GET `/api/admin/batches/`
Get all batches.

**Response:**
```json
{
    "batches": [
        {
            "id": 1,
            "name": "Batch-2024-01",
            "book_price": 5000,
            "price": 15000,
            "status": "active",
            "created_at": "2024-01-01T10:00:00Z"
        }
    ]
}
```

### POST `/api/admin/batches/`
Create a new batch.

**Request Body:**
```json
{
    "name": "string",
    "book_price": "integer",
    "price": "integer",
    "status": "active|inactive|completed|upcoming"
}
```

**Response:**
```json
{
    "msg": "New Batch added successfully",
    "batch": {
        "id": 1,
        "name": "Batch-2024-01",
        "book_price": 5000,
        "price": 15000,
        "status": "active"
    }
}
```

### PATCH `/api/admin/batches/{id}/`
Update an existing batch.

**Path Parameters:**
- `id` (integer): Batch ID

**Request Body:**
```json
{
    "name": "string (optional)",
    "book_price": "integer (optional)",
    "price": "integer (optional)",
    "status": "string (optional)"
}
```

**Response:**
```json
{
    "msg": "Batch updated successfully",
    "batch": {
        "id": 1,
        "name": "Updated Batch",
        "book_price": 5500,
        "price": 16000,
        "status": "active"
    }
}
```

### GET `/api/admin/closed-sales/`
Get closed sales leads.

**Response:**
```json
{
    "msg": "closed leads fetched",
    "revenue": 75000,
    "leads": [
        {
            "id": 1,
            "name": "John Doe",
            "contact_number": "+12345678901",
            "status": "closed-success",
            "sale_details": {
                "status": "verified",
                "batch": {
                    "name": "Batch-2024-01",
                    "price": 15000
                }
            }
        }
    ]
}
```

### GET `/api/admin/download-database/`
Download database file (admin only).

**Response:** File download (db.sqlite3)

---

## Sales API (`/api/sales/`)

### GET `/api/sales/my-leads/`
Get leads assigned to current user.

**Response:**
```json
{
    "leads": [
        {
            "id": 1,
            "name": "John Doe",
            "contact_number": "+12345678901",
            "source": "website",
            "status": "new"
        }
    ]
}
```

### POST `/api/sales/update-lead-status/`
Update lead status and upload documents.

**Request Body (multipart/form-data):**
- `lead_id`: integer
- `status`: string
- `form_ss`: image file (optional)
- `payment_ss`: image file (optional)
- `books_ss`: image file (optional)
- `buy_books`: boolean

**Response:**
```json
{
    "msg": "Lead status updated successfully",
    "lead": {
        "id": 1,
        "status": "payment_received"
    }
}
```

---

## Operations API (`/api/ops/`)

### GET `/api/ops/leads/`
Get leads for operations team.

**Response:**
```json
{
    "leads": [
        {
            "id": 1,
            "name": "John Doe",
            "contact_number": "+12345678901",
            "status": "payment_received",
            "sale_details": {
                "status": "verified",
                "form_ss": "/media/form_screenshots/image.jpg"
            }
        }
    ]
}
```

### POST `/api/ops/add-to-group/`
Mark lead as added to group.

**Request Body:**
```json
{
    "lead_id": "integer"
}
```

**Response:**
```json
{
    "msg": "Lead added to group successfully"
}
```

### POST `/api/ops/mark-registered/`
Mark lead as registered on app.

**Request Body:**
```json
{
    "lead_id": "integer"
}
```

**Response:**
```json
{
    "msg": "Lead marked as registered successfully"
}
```

---

## Error Responses

All endpoints return consistent error responses:

### Validation Error (400)
```json
{
    "error": "Validation Error",
    "message": "Invalid phone number format. Please use a valid international format.",
    "code": "validation_error",
    "status": "error"
}
```

### Authentication Error (401)
```json
{
    "error": "Authentication Failed",
    "message": "Invalid authentication credentials",
    "code": "authentication_error",
    "status": "error"
}
```

### Permission Error (403)
```json
{
    "error": "Permission Denied",
    "message": "You do not have permission to perform this action",
    "code": "permission_denied",
    "status": "error"
}
```

### Not Found Error (404)
```json
{
    "error": "Not Found",
    "message": "The requested resource was not found",
    "code": "not_found",
    "status": "error"
}
```

### Server Error (500)
```json
{
    "error": "Server Error",
    "message": "An internal server error occurred",
    "code": "server_error",
    "status": "error"
}
```

---

## Data Models

### User
```json
{
    "id": "integer",
    "email": "string",
    "name": "string",
    "contact": "string",
    "type": "admin|sales|operations",
    "is_admin": "boolean",
    "created_at": "datetime"
}
```

### Lead
```json
{
    "id": "integer",
    "name": "string",
    "contact_number": "string",
    "source": "website|referral|direct",
    "status": "new|contacted|interested|not_interested|payment_received|payment_pending|closed-success|closed-failed|dnp",
    "assigned_to": "User object (nullable)",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Batch
```json
{
    "id": "integer",
    "name": "string",
    "book_price": "integer",
    "price": "integer",
    "status": "active|inactive|completed|upcoming",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Employee
```json
{
    "id": "integer",
    "user": "User object",
    "type": "admin|sales|operations",
    "allot": "integer"
}
```

---

## Rate Limiting

- **Limit**: 100 requests per minute per IP address
- **Response** when exceeded:
```json
{
    "error": "Rate Limit Exceeded",
    "message": "Too many requests. Please try again later.",
    "code": "rate_limit_exceeded",
    "status": "error"
}
```

---

## Testing the API

Use the Django REST Framework browsable API:
- Navigate to `http://localhost:8000/api/`
- Use the web interface to test endpoints
- Or use tools like Postman/curl with the provided examples

---

## File Uploads

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)

### File Size Limits
- Images: 5MB maximum
- Excel files: 10MB maximum

### Upload Endpoints
- `/api/admin/import-leads/` - Excel files
- `/api/sales/update-lead-status/` - Images (form_ss, payment_ss, books_ss)
