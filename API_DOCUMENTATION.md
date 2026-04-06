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

**Note:** The login response returns a nested token structure. Extract the access token from `token.access` field.

---

## Authentication API (`/api/auth/`)

### POST `/api/auth/login/`
Authenticate user and return JWT tokens.

**Request Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
    "email": "string",
    "password": "string"
}
```

**Response Headers:**
- `Content-Type: application/json`
- `Vary: Accept, origin`
- `Allow: POST, OPTIONS`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Cross-Origin-Opener-Policy: same-origin`
- `X-XSS-Protection: 1; mode=block`
- `Access-Control-Expose-Headers: Content-Type, Authorization`

**Response:**
```json
{
    "token": {
        "refresh": "string",
        "access": "string"
    },
    "msg": "User Logged Login",
    "user": {
        "id": "integer",
        "email": "string",
        "name": "string",
        "type": "admin|sales|operations"
    },
    "emp": {
        "id": "integer",
        "user": "integer",
        "type": "admin|sales|operations",
        "allot": "integer"
    }
}
```

**Authentication:**
Include the access token in the Authorization header:
```http
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Note:** The login response returns a nested token structure. Extract the access token from `token.access` field.

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

### POST `/api/auth/user/`
Create new user (requires admin authentication).

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

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

**Response:**
```json
{
    "token": {
        "refresh": "string",
        "access": "string"
    },
    "user": {
        "id": "integer",
        "email": "string",
        "name": "string",
        "type": "admin|sales|operations"
    },
    "emp": {
        "id": "integer",
        "user": "integer",
        "type": "admin|sales|operations",
        "allot": "integer"
    },
    "msg": "User created"
}
```

### GET `/api/auth/user/{id}/`
Get user details by ID.

**Response:**
```json
{
    "msg": "user obtained",
    "user": {
        "id": "integer",
        "email": "string",
        "name": "string",
        "type": "admin|sales|operations"
    },
    "employee": {
        "id": "integer",
        "user": "integer",
        "type": "admin|sales|operations",
        "allot": "integer"
    }
}
```

---

## Admin API (`/api/admin/`)

### GET `/api/admin/dashboard-stats/`
Get dashboard statistics.

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Response:**
```json
{
    "converted_leads": "integer",
    "dnp_leads": "integer",
    "active_leads": "integer",
    "total_leads": "integer"
}
```

### GET `/api/admin/total-pages/`
Get total pages for leads pagination.

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Response:**
```json
{
    "total_pages": "integer"
}
```

### GET `/api/admin/getLeads/{page}/`
Get paginated leads.

**Path Parameters:**
- `page` (integer): Page number (1-based)

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Response:**
```json
{
    "msg": "Leads fetched",
    "leads": [
        {
            "id": "integer",
            "name": "string",
            "contact_number": "string",
            "source": "string",
            "status": "string",
            "created_at": "datetime",
            "assigned_to": "integer|null",
            "sale_details": {
                "status": "string",
                "amount": "integer|null",
                "payment_status": "string|null",
                "form_ss": "string|null",
                "payment_ss": "string|null",
                "books_ss": "string|null",
                "buy_books": "boolean"
            }
        }
    ]
}
```

### GET `/api/admin/leads/`
Get all leads (no file upload).

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Response:**
```json
{
    "msg": "Obtained Leads",
    "leads": [
        {
            "id": "integer",
            "name": "string",
            "contact_number": "string",
            "source": "string",
            "status": "string",
            "created_at": "datetime",
            "assigned_to": "integer|null",
            "sale_details": {
                "status": "string",
                "amount": "integer|null",
                "payment_status": "string|null",
                "form_ss": "string|null",
                "payment_ss": "string|null",
                "books_ss": "string|null",
                "buy_books": "boolean"
            }
        }
    ]
}
```

### POST `/api/admin/leads/`
Upload lead sheet file.

**Request Headers:**
- `Content-Type: multipart/form-data`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Request Body (multipart/form-data):**
- `file`: Excel file (.xlsx, .xls)

**Response:**
```json
{
    "msg": "File uploaded successfully"
}
```

**File Upload Specifications:**
- **Supported Formats**: .xlsx, .xls
- **File Size Limit**: 10MB
- **Processing**: File is parsed and leads are imported into database
- **Required Fields**: name, contact_number, source, status

### GET `/api/admin/sales/`
Get sales data.

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Response:**
```json
{
    "msg": "all Employees",
    "employees": [
        {
            "id": "integer",
            "employee_details": {
                "user": "integer",
                "type": "admin|sales|operations",
                "allot": "integer",
                "assigned_leads": "integer|null",
                "revenue": "integer|null",
                "remaining_leads": "integer|null",
                "closed_leads": "integer|null"
            },
            "password": "string",
            "last_login": "datetime|null",
            "is_superuser": "boolean",
            "email": "string",
            "name": "string",
            "contact": "string",
            "type": "admin|sales|operations",
            "is_admin": "boolean",
            "is_staff": "boolean",
            "created_at": "datetime",
            "updated_at": "datetime",
            "groups": "array",
            "user_permissions": "array"
        }
    ]
}
```

### GET `/api/admin/closed-sales/`
Get closed sales data.

**Request Headers:**
- `Content-Type: application/json`
- `Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Response:**
```json
{
    "msg": "closed leads fetched",
    "revenue": "integer",
    "leads": [
        {
            "id": "integer",
            "name": "string",
            "contact_number": "string",
            "source": "string",
            "status": "string",
            "created_at": "datetime",
            "assigned_to": "integer|null",
            "sale_details": {
                "status": "string",
                "amount": "integer|null",
                "payment_status": "string|null",
                "form_ss": "string|null",
                "payment_ss": "string|null",
                "books_ss": "string|null",
                "buy_books": "boolean"
            }
        }
    ]
}
```

### GET `/api/admin/employee/`
Get all employees.

**Response:**
```json
{
    "employees": [
        {
            "id": "integer",
            "user": "integer",
            "type": "admin|sales|operations",
            "allot": "integer"
        }
    ]
}
```

### POST `/api/admin/employee/`
Create new employee.

**Request Body:**
```json
{
    "user": "integer",
    "type": "admin|sales|operations",
    "allot": "integer"
}
```

### GET `/api/admin/batch/`
Get all batches.

**Response:**
```json
{
    "batches": [
        {
            "id": "integer",
            "name": "string",
            "book_price": "integer",
            "price": "integer",
            "status": "string",
            "created_at": "datetime"
        }
    ]
}
```

### POST `/api/admin/batch/`
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

### POST `/api/admin/reset-allot-leads/`
Reset lead allotments.

**Response:**
```json
{
    "msg": "Lead allotments reset successfully"
}
```

---

## Sales API (`/api/sales/`)

### GET `/api/sales/leads/`
Get sales leads data.

**Response:**
```json
{
    "leads_data": "array"
}
```

### GET `/api/sales/boardScore/`
Get sales board score data.

**Response:**
```json
{
    "board_score": "array"
}
```

### GET `/api/sales/lead/`
Get lead details.

**Response:**
```json
{
    "lead": "object"
}
```

### GET `/api/sales/total-pages/`
Get total pages for sales leads.

**Response:**
```json
{
    "total_pages": "integer"
}
```

### GET `/api/sales/get-leads/{page}/`
Get paginated sales leads.

**Path Parameters:**
- `page` (integer): Page number (1-based)

**Response:**
```json
{
    "leads": "array"
}
```

---

## Operations API (`/api/ops/`)

### GET `/api/ops/lead/`
Get lead details for operations team.

**Response:**
```json
{
    "lead": "object"
}
```

---

## Accounts API (`/api/accounts/`)

### GET `/api/accounts/lead/`
Get lead account details.

**Response:**
```json
{
    "lead": "object"
}
```

---

## General API (`/api/gen/`)

### GET `/api/gen/total-pages/`
Get total pages for general leads.

**Response:**
```json
{
    "total_pages": "integer"
}
```

### GET `/api/gen/lead/{pk}/download-image/`
Download lead proof image.

**Path Parameters:**
- `pk` (integer): Lead primary key

**Response:** File download

### GET `/api/gen/batch/`
Get batch information.

**Response:**
```json
{
    "batches": "array"
}
```

### GET `/api/gen/under-review-leads/{page}/`
Get leads under review.

**Path Parameters:**
- `page` (integer): Page number (1-based)

**Response:**
```json
{
    "leads": "array"
}
```

### GET `/api/gen/current-user/`
Get current user information.

**Response:**
```json
{
    "user": "object"
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
