# Web App API Documentation

## Overview

This API provides endpoints for managing users and their associated metrics in our web application.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, no authentication is required for development. In production, all endpoints will require JWT authentication.

## Endpoints

### Users

#### GET /users/{user_id}

Retrieve a specific user by ID.

**Parameters:**
- `user_id` (integer): The unique identifier of the user

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### POST /users

Create a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Metrics

#### GET /metrics/{user_id}

Retrieve all metrics for a specific user.

**Parameters:**
- `user_id` (integer): The unique identifier of the user

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "page_views",
    "value": 1250.0,
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

#### POST /metrics

Create a new metric.

**Request Body:**
```json
{
  "user_id": 1,
  "name": "page_views",
  "value": 1250.0
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful GET requests
- `201 Created`: Successful POST requests
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a JSON object with an error message:

```json
{
  "error": "User not found"
}
```
