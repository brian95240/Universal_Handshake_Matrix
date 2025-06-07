# Affiliate Matrix API Documentation

## Overview

This document provides detailed API documentation for the Affiliate Matrix system. The API follows RESTful principles and uses JSON for data exchange.

## Base URL

```
https://api.affiliatematrix.com/v1
```

## Authentication

All API requests require authentication using an API key. The API key should be included in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

## Programs API

### List Programs

Retrieves a paginated list of affiliate programs.

**Endpoint:** `GET /programs`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number (1-indexed) |
| limit | integer | Number of items per page |
| status | string | Filter by status (active, inactive, pending) |
| category | string | Filter by category |
| min_commission | number | Filter by minimum commission value |
| sort | string | Field to sort by |
| order | string | Sort order (asc, desc) |

**Response:**

```json
{
  "data": [
    {
      "id": "prog_1",
      "name": "Amazon Associates",
      "url": "https://affiliate-program.amazon.com/",
      "description": "Amazon's affiliate program",
      "status": "active",
      "category": ["E-commerce"],
      "tags": ["Retail", "High Volume"],
      "commission": {
        "type": "percentage",
        "value": 3.0
      },
      "cookieDuration": 24,
      "epc": 0.85,
      "conversionRate": 2.1,
      "paymentMethods": ["Direct Deposit", "Check"],
      "paymentFrequency": "monthly",
      "minimumPayout": 10,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z"
    },
    // More programs...
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 42,
    "total_pages": 5
  }
}
```

### Get Program

Retrieves a specific program by ID.

**Endpoint:** `GET /programs/{program_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| program_id | string | Program ID |

**Response:**

```json
{
  "id": "prog_1",
  "name": "Amazon Associates",
  "url": "https://affiliate-program.amazon.com/",
  "description": "Amazon's affiliate program",
  "status": "active",
  "category": ["E-commerce"],
  "tags": ["Retail", "High Volume"],
  "commission": {
    "type": "percentage",
    "value": 3.0
  },
  "cookieDuration": 24,
  "epc": 0.85,
  "conversionRate": 2.1,
  "paymentMethods": ["Direct Deposit", "Check"],
  "paymentFrequency": "monthly",
  "minimumPayout": 10,
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

### Create Program

Creates a new affiliate program.

**Endpoint:** `POST /programs`

**Request Body:**

```json
{
  "name": "New Affiliate Program",
  "url": "https://example.com/affiliate",
  "description": "Description of the program",
  "status": "active",
  "category": ["Technology"],
  "tags": ["SaaS", "High Commission"],
  "commission": {
    "type": "percentage",
    "value": 20.0
  },
  "cookieDuration": 30,
  "paymentMethods": ["PayPal"],
  "paymentFrequency": "monthly",
  "minimumPayout": 50
}
```

**Response:**

```json
{
  "id": "prog_new",
  "name": "New Affiliate Program",
  "url": "https://example.com/affiliate",
  "description": "Description of the program",
  "status": "active",
  "category": ["Technology"],
  "tags": ["SaaS", "High Commission"],
  "commission": {
    "type": "percentage",
    "value": 20.0
  },
  "cookieDuration": 30,
  "epc": 0,
  "conversionRate": 0,
  "paymentMethods": ["PayPal"],
  "paymentFrequency": "monthly",
  "minimumPayout": 50,
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

### Update Program

Updates an existing affiliate program.

**Endpoint:** `PUT /programs/{program_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| program_id | string | Program ID |

**Request Body:**

```json
{
  "name": "Updated Program Name",
  "status": "inactive",
  "description": "Updated description"
}
```

**Response:**

```json
{
  "id": "prog_1",
  "name": "Updated Program Name",
  "url": "https://affiliate-program.amazon.com/",
  "description": "Updated description",
  "status": "inactive",
  "category": ["E-commerce"],
  "tags": ["Retail", "High Volume"],
  "commission": {
    "type": "percentage",
    "value": 3.0
  },
  "cookieDuration": 24,
  "epc": 0.85,
  "conversionRate": 2.1,
  "paymentMethods": ["Direct Deposit", "Check"],
  "paymentFrequency": "monthly",
  "minimumPayout": 10,
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-02T00:00:00Z"
}
```

### Delete Program

Deletes an affiliate program.

**Endpoint:** `DELETE /programs/{program_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| program_id | string | Program ID |

**Response:**

```json
{
  "success": true,
  "message": "Program deleted successfully"
}
```

### Get Program Metrics

Retrieves metrics for a specific program.

**Endpoint:** `GET /programs/{program_id}/metrics`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| program_id | string | Program ID |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| period | string | Time period (day, week, month, year) |
| start_date | string | Start date (ISO format) |
| end_date | string | End date (ISO format) |

**Response:**

```json
{
  "clicks": 1250,
  "impressions": 25000,
  "conversions": 75,
  "revenue": 1500.50,
  "epc": 1.2,
  "conversionRate": 6.0,
  "timeSeries": [
    {
      "date": "2023-01-01",
      "clicks": 100,
      "impressions": 2000,
      "conversions": 6,
      "revenue": 120.00
    },
    // More time series data...
  ]
}
```

## Connections API

### List Connections

Retrieves a paginated list of connections.

**Endpoint:** `GET /connections`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| page | integer | Page number (1-indexed) |
| limit | integer | Number of items per page |
| type | string | Filter by connection type |
| status | string | Filter by connection status |

**Response:**

```json
{
  "data": [
    {
      "id": "conn_1",
      "name": "ShareASale API",
      "type": "api",
      "url": "https://api.shareasale.com/",
      "description": "ShareASale affiliate network API connection",
      "status": {
        "state": "connected",
        "lastChecked": "2023-01-01T00:00:00Z",
        "message": "Connection is active"
      },
      "credentials": {
        "apiKey": "***********",
        "apiSecret": "***********",
        "tokenExpiry": "2024-01-01T00:00:00Z"
      },
      "settings": {
        "refreshInterval": 60,
        "autoSync": true,
        "filters": {
          "categories": ["Technology"],
          "minCommission": 5.0
        }
      },
      "lastSync": "2023-01-01T00:00:00Z",
      "nextScheduledSync": "2023-01-02T00:00:00Z",
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z"
    },
    // More connections...
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "total_pages": 1
  }
}
```

### Get Connection

Retrieves a specific connection by ID.

**Endpoint:** `GET /connections/{connection_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| connection_id | string | Connection ID |

**Response:**

```json
{
  "id": "conn_1",
  "name": "ShareASale API",
  "type": "api",
  "url": "https://api.shareasale.com/",
  "description": "ShareASale affiliate network API connection",
  "status": {
    "state": "connected",
    "lastChecked": "2023-01-01T00:00:00Z",
    "message": "Connection is active"
  },
  "credentials": {
    "apiKey": "***********",
    "apiSecret": "***********",
    "tokenExpiry": "2024-01-01T00:00:00Z"
  },
  "settings": {
    "refreshInterval": 60,
    "autoSync": true,
    "filters": {
      "categories": ["Technology"],
      "minCommission": 5.0
    }
  },
  "lastSync": "2023-01-01T00:00:00Z",
  "nextScheduledSync": "2023-01-02T00:00:00Z",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

### Create Connection

Creates a new connection.

**Endpoint:** `POST /connections`

**Request Body:**

```json
{
  "name": "New Connection",
  "type": "api",
  "url": "https://api.example.com/",
  "description": "Example API connection",
  "credentials": {
    "apiKey": "example_key",
    "apiSecret": "example_secret"
  },
  "settings": {
    "refreshInterval": 120,
    "autoSync": false,
    "filters": {
      "categories": ["Digital Products"],
      "minCommission": 10.0
    }
  }
}
```

**Response:**

```json
{
  "id": "conn_new",
  "name": "New Connection",
  "type": "api",
  "url": "https://api.example.com/",
  "description": "Example API connection",
  "status": {
    "state": "pending",
    "lastChecked": null,
    "message": "Connection created, not yet tested"
  },
  "credentials": {
    "apiKey": "***********",
    "apiSecret": "***********",
    "tokenExpiry": null
  },
  "settings": {
    "refreshInterval": 120,
    "autoSync": false,
    "filters": {
      "categories": ["Digital Products"],
      "minCommission": 10.0
    }
  },
  "lastSync": null,
  "nextScheduledSync": null,
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

### Update Connection

Updates an existing connection.

**Endpoint:** `PUT /connections/{connection_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| connection_id | string | Connection ID |

**Request Body:**

```json
{
  "name": "Updated Connection Name",
  "description": "Updated description",
  "settings": {
    "refreshInterval": 240,
    "autoSync": true
  }
}
```

**Response:**

```json
{
  "id": "conn_1",
  "name": "Updated Connection Name",
  "type": "api",
  "url": "https://api.shareasale.com/",
  "description": "Updated description",
  "status": {
    "state": "connected",
    "lastChecked": "2023-01-01T00:00:00Z",
    "message": "Connection is active"
  },
  "credentials": {
    "apiKey": "***********",
    "apiSecret": "***********",
    "tokenExpiry": "2024-01-01T00:00:00Z"
  },
  "settings": {
    "refreshInterval": 240,
    "autoSync": true,
    "filters": {
      "categories": ["Technology"],
      "minCommission": 5.0
    }
  },
  "lastSync": "2023-01-01T00:00:00Z",
  "nextScheduledSync": "2023-01-02T00:00:00Z",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-02T00:00:00Z"
}
```

### Delete Connection

Deletes a connection.

**Endpoint:** `DELETE /connections/{connection_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| connection_id | string | Connection ID |

**Response:**

```json
{
  "success": true,
  "message": "Connection deleted successfully"
}
```

### Test Connection

Tests a connection to verify it's working correctly.

**Endpoint:** `POST /connections/{connection_id}/test`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| connection_id | string | Connection ID |

**Response:**

```json
{
  "status": {
    "state": "connected",
    "lastChecked": "2023-01-02T00:00:00Z",
    "message": "Connection successful"
  }
}
```

### Sync Connection

Triggers a synchronization for a connection.

**Endpoint:** `POST /connections/{connection_id}/sync`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| connection_id | string | Connection ID |

**Response:**

```json
{
  "id": "conn_1",
  "status": {
    "state": "syncing",
    "lastChecked": "2023-01-02T00:00:00Z",
    "message": "Synchronization started",
    "syncProgress": 0
  },
  "lastSync": "2023-01-01T00:00:00Z",
  "nextScheduledSync": "2023-01-03T00:00:00Z",
  "updatedAt": "2023-01-02T00:00:00Z"
}
```

## System API

### Get System Metrics

Retrieves system-wide metrics.

**Endpoint:** `GET /system/metrics`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| period | string | Time period (day, week, month, year) |

**Response:**

```json
{
  "totalPrograms": 42,
  "activePrograms": 35,
  "totalConnections": 5,
  "activeConnections": 4,
  "totalClicks": 25000,
  "totalConversions": 1200,
  "totalRevenue": 35000.50,
  "averageEpc": 1.4,
  "averageConversionRate": 4.8,
  "topPrograms": [
    {
      "id": "prog_1",
      "name": "Amazon Associates",
      "clicks": 5000,
      "conversions": 300,
      "revenue": 6000.00
    },
    // More programs...
  ],
  "timeSeries": [
    {
      "date": "2023-01-01",
      "clicks": 800,
      "conversions": 40,
      "revenue": 1200.00
    },
    // More time series data...
  ]
}
```

### Get System Status

Retrieves the current system status.

**Endpoint:** `GET /system/status`

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": 86400,
  "lastBackup": "2023-01-01T00:00:00Z",
  "services": [
    {
      "name": "database",
      "status": "healthy",
      "message": "Connected"
    },
    {
      "name": "cache",
      "status": "healthy",
      "message": "Connected"
    },
    {
      "name": "scheduler",
      "status": "healthy",
      "message": "Running"
    }
  ]
}
```

## Feature Flags API

### List Feature Flags

Retrieves all feature flags and their current values.

**Endpoint:** `GET /system/feature-flags`

**Response:**

```json
{
  "enable_delta_endpoints": true,
  "enable_vault_integration": false,
  "enable_advanced_filtering": true,
  "enable_telemetry": true,
  "enable_background_tasks": true,
  "enable_caching": true,
  "enable_rate_limiting": false,
  "enable_experimental_features": false
}
```

### Update Feature Flag

Updates a specific feature flag.

**Endpoint:** `PUT /system/feature-flags/{flag_name}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| flag_name | string | Feature flag name |

**Request Body:**

```json
{
  "enabled": true
}
```

**Response:**

```json
{
  "name": "enable_vault_integration",
  "enabled": true,
  "updated_at": "2023-01-02T00:00:00Z"
}
```

## Error Responses

All API endpoints return appropriate HTTP status codes:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses include a JSON body with details:

```json
{
  "error": {
    "code": "not_found",
    "message": "Program not found: prog_invalid",
    "details": {
      "resource_type": "Program",
      "resource_id": "prog_invalid"
    }
  }
}
```

## Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (1-indexed)
- `limit`: Number of items per page

Response includes pagination metadata:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 42,
    "total_pages": 5
  }
}
```

## Filtering

List endpoints support filtering through query parameters. Available filters depend on the resource type.

## Sorting

List endpoints support sorting with the following parameters:

- `sort`: Field to sort by
- `order`: Sort order (asc, desc)

## Rate Limiting

API requests are subject to rate limiting. The current limits are:

- 100 requests per minute per API key
- 5,000 requests per day per API key

Rate limit information is included in response headers:

- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Time when the limit resets (Unix timestamp)

When rate limit is exceeded, the API returns `429 Too Many Requests`.
