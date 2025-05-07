# Address Book API Documentation

This document provides detailed information about the Address Book API endpoints, their usage, and example requests/responses.

## Base URL

```
https://itmd504-webapp.vrraajan.com
```

## Authentication

Currently, the API does not require authentication.

## Endpoints

### 1. List Contacts
Retrieves a list of contacts with filtering, sorting, and pagination options.

**Endpoint:** `GET /api/contacts`

**Query Parameters:**
- `search` (optional): Search term to filter contacts (searches in firstname, lastname, email, and phone)
- `phone_type` (optional): Filter by phone type (mobile/home/work)
- `sort_by` (optional): Field to sort by (default: firstname)
- `sort_order` (optional): Sort order (asc/desc, default: asc)
- `page` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Number of items per page (default: 10)

**Example Request:**
```bash
curl "https://itmd504-webapp.vrraajan.com/api/contacts?search=john&phone_type=mobile&sort_by=lastname&sort_order=desc&page=1&per_page=5"
```

**Example Response:**
```json
{
    "contacts": [
        {
            "id": 1,
            "firstname": "John",
            "lastname": "Smith",
            "email": "john.smith@example.com",
            "phone": "555-0101",
            "phone_type": "mobile",
            "created_at": "2024-05-06 20:57:07"
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 5,
        "total": 1,
        "pages": 1
    }
}
```

### 2. Get Single Contact
Retrieves a specific contact by ID.

**Endpoint:** `GET /api/contacts/{id}`

**Path Parameters:**
- `id`: Contact ID

**Example Request:**
```bash
curl "https://itmd504-webapp.vrraajan.com/api/contacts/1"
```

**Example Response:**
```json
{
    "id": 1,
    "firstname": "John",
    "lastname": "Smith",
    "email": "john.smith@example.com",
    "phone": "555-0101",
    "phone_type": "mobile",
    "created_at": "2024-05-06 20:57:07"
}
```

### 3. Create Contact
Creates a new contact.

**Endpoint:** `POST /api/contacts`

**Request Body:**
```json
{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "phone_type": "mobile"
}
```

**Example Request:**
```bash
curl -X POST https://itmd504-webapp.vrraajan.com/api/contacts \
  -H "Content-Type: application/json" \
  -d '{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "phone_type": "mobile"
  }'
```

**Example Response:**
```json
{
    "id": 2,
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "phone_type": "mobile",
    "created_at": "2024-05-06 21:00:00"
}
```

### 4. Update Contact
Updates an existing contact.

**Endpoint:** `PUT /api/contacts/{id}`

**Path Parameters:**
- `id`: Contact ID

**Request Body:**
```json
{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "phone": "555-9999",
    "phone_type": "mobile"
}
```

**Example Request:**
```bash
curl -X PUT https://itmd504-webapp.vrraajan.com/api/contacts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "555-9999"
  }'
```

**Example Response:**
```json
{
    "id": 1,
    "firstname": "John",
    "lastname": "Smith",
    "email": "john.smith@example.com",
    "phone": "555-9999",
    "phone_type": "mobile",
    "created_at": "2024-05-06 20:57:07"
}
```

### 5. Delete Contact
Deletes a contact.

**Endpoint:** `DELETE /api/contacts/{id}`

**Path Parameters:**
- `id`: Contact ID

**Example Request:**
```bash
curl -X DELETE https://itmd504-webapp.vrraajan.com/api/contacts/1
```

**Example Response:**
- Status Code: 204 No Content

## Error Responses

The API may return the following error responses:

### 400 Bad Request
```json
{
    "error": "Invalid input data"
}
```

### 404 Not Found
```json
{
    "error": "Contact not found"
}
```

## Data Types

### Contact Object
```json
{
    "id": "integer",
    "firstname": "string",
    "lastname": "string",
    "email": "string",
    "phone": "string",
    "phone_type": "string (mobile/home/work)",
    "created_at": "datetime"
}
```

## Rate Limiting

Currently, there are no rate limits implemented.

## Best Practices

1. Always include the `Content-Type: application/json` header for POST and PUT requests
2. Use pagination when retrieving large lists of contacts
3. Implement proper error handling for API responses
4. Cache responses when appropriate to improve performance 