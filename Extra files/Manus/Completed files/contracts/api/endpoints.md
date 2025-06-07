# Affiliate Matrix API Endpoints

This document defines the RESTful API endpoints for the Affiliate Matrix system, mapping the core functionality required by both the frontend and backend components.

## Authentication

All API endpoints require authentication using a Bearer token.

```
Authorization: Bearer <token>
```

## Programs

### List Programs

```
GET /api/programs
```

Query Parameters:
- `page` (integer): Page number for pagination (default: 1)
- `limit` (integer): Number of items per page (default: 20)
- `sort` (string): Field to sort by (e.g., "name", "dateAdded", "commission.value")
- `order` (string): Sort order ("asc" or "desc")
- `status` (string): Filter by status ("active", "inactive", "pending")
- `category` (string): Filter by category
- `tag` (string): Filter by tag
- `source` (string): Filter by source
- `search` (string): Search term for name, description, or URL
- `minCommission` (number): Minimum commission value
- `maxCommission` (number): Maximum commission value
- `minEpc` (number): Minimum earnings per click
- `minConversionRate` (number): Minimum conversion rate

Response:
- Status: 200 OK
- Body: Array of Program objects with pagination metadata

### Get Program

```
GET /api/programs/{id}
```

Path Parameters:
- `id` (string): Program ID

Response:
- Status: 200 OK
- Body: Program object
- Status: 404 Not Found if program doesn't exist

### Create Program

```
POST /api/programs
```

Request Body: Program object (without id)

Response:
- Status: 201 Created
- Body: Created Program object with id

### Update Program

```
PUT /api/programs/{id}
```

Path Parameters:
- `id` (string): Program ID

Request Body: Program object (partial updates allowed)

Response:
- Status: 200 OK
- Body: Updated Program object
- Status: 404 Not Found if program doesn't exist

### Delete Program

```
DELETE /api/programs/{id}
```

Path Parameters:
- `id` (string): Program ID

Response:
- Status: 204 No Content
- Status: 404 Not Found if program doesn't exist

### Get Program Metrics

```
GET /api/programs/{id}/metrics
```

Path Parameters:
- `id` (string): Program ID

Query Parameters:
- `period` (string): Time period for metrics ("day", "week", "month", "year", default: "month")

Response:
- Status: 200 OK
- Body: ProgramMetrics object
- Status: 404 Not Found if program doesn't exist

## Connections

### List Connections

```
GET /api/connections
```

Query Parameters:
- `page` (integer): Page number for pagination (default: 1)
- `limit` (integer): Number of items per page (default: 20)
- `type` (string): Filter by connection type ("aggregator", "api", "manual")
- `status` (string): Filter by connection status ("connected", "disconnected", "error", "syncing")

Response:
- Status: 200 OK
- Body: Array of Connection objects with pagination metadata

### Get Connection

```
GET /api/connections/{id}
```

Path Parameters:
- `id` (string): Connection ID

Response:
- Status: 200 OK
- Body: Connection object
- Status: 404 Not Found if connection doesn't exist

### Create Connection

```
POST /api/connections
```

Request Body: Connection object (without id)

Response:
- Status: 201 Created
- Body: Created Connection object with id

### Update Connection

```
PUT /api/connections/{id}
```

Path Parameters:
- `id` (string): Connection ID

Request Body: Connection object (partial updates allowed)

Response:
- Status: 200 OK
- Body: Updated Connection object
- Status: 404 Not Found if connection doesn't exist

### Delete Connection

```
DELETE /api/connections/{id}
```

Path Parameters:
- `id` (string): Connection ID

Response:
- Status: 204 No Content
- Status: 404 Not Found if connection doesn't exist

### Sync Connection

```
POST /api/connections/{id}/sync
```

Path Parameters:
- `id` (string): Connection ID

Response:
- Status: 202 Accepted
- Body: Updated Connection object with status
- Status: 404 Not Found if connection doesn't exist

### Test Connection

```
POST /api/connections/{id}/test
```

Path Parameters:
- `id` (string): Connection ID

Response:
- Status: 200 OK
- Body: ConnectionStatus object
- Status: 404 Not Found if connection doesn't exist

## Discovery

### List Discovery Results

```
GET /api/discovery
```

Query Parameters:
- `page` (integer): Page number for pagination (default: 1)
- `limit` (integer): Number of items per page (default: 20)
- `status` (string): Filter by status ("completed", "in_progress", "failed")
- `startDate` (string): Filter by start date (ISO format)
- `endDate` (string): Filter by end date (ISO format)

Response:
- Status: 200 OK
- Body: Array of DiscoveryResult objects with pagination metadata

### Get Discovery Result

```
GET /api/discovery/{id}
```

Path Parameters:
- `id` (string): Discovery result ID

Response:
- Status: 200 OK
- Body: DiscoveryResult object
- Status: 404 Not Found if discovery result doesn't exist

### Start Discovery

```
POST /api/discovery
```

Request Body:
```json
{
  "query": "string",
  "parameters": {
    "depth": "number",
    "maxResults": "number",
    "filters": "object"
  }
}
```

Response:
- Status: 202 Accepted
- Body: DiscoveryResult object with status "in_progress"

### Cancel Discovery

```
POST /api/discovery/{id}/cancel
```

Path Parameters:
- `id` (string): Discovery result ID

Response:
- Status: 200 OK
- Body: Updated DiscoveryResult object
- Status: 404 Not Found if discovery result doesn't exist
- Status: 400 Bad Request if discovery is already completed or failed

### Process Discovery Item

```
POST /api/discovery/{id}/items/{itemId}/process
```

Path Parameters:
- `id` (string): Discovery result ID
- `itemId` (string): Discovery item ID

Request Body:
```json
{
  "action": "string", // "add", "ignore", "review"
  "programDetails": "object" // Optional, Program object details if action is "add"
}
```

Response:
- Status: 200 OK
- Body: Updated DiscoveryItem object
- Status: 404 Not Found if discovery result or item doesn't exist

## System

### Get System Metrics

```
GET /api/system/metrics
```

Query Parameters:
- `period` (string): Time period for metrics ("hour", "day", "week", "month", default: "hour")

Response:
- Status: 200 OK
- Body: SystemMetrics object

### Get System Logs

```
GET /api/system/logs
```

Query Parameters:
- `level` (string): Filter by log level ("info", "warning", "error", "debug")
- `component` (string): Filter by component
- `startDate` (string): Filter by start date (ISO format)
- `endDate` (string): Filter by end date (ISO format)
- `limit` (integer): Number of log entries to return (default: 100)

Response:
- Status: 200 OK
- Body: Array of log objects

### Get System Status

```
GET /api/system/status
```

Response:
- Status: 200 OK
- Body: System status object with overall health and component statuses

## Budgets

### List Budgets

```
GET /api/budgets
```

Query Parameters:
- `page` (integer): Page number for pagination (default: 1)
- `limit` (integer): Number of items per page (default: 20)
- `status` (string): Filter by status ("active", "paused", "completed")
- `startDate` (string): Filter by start date (ISO format)
- `endDate` (string): Filter by end date (ISO format)

Response:
- Status: 200 OK
- Body: Array of Budget objects with pagination metadata

### Get Budget

```
GET /api/budgets/{id}
```

Path Parameters:
- `id` (string): Budget ID

Response:
- Status: 200 OK
- Body: Budget object
- Status: 404 Not Found if budget doesn't exist

### Create Budget

```
POST /api/budgets
```

Request Body: Budget object (without id)

Response:
- Status: 201 Created
- Body: Created Budget object with id

### Update Budget

```
PUT /api/budgets/{id}
```

Path Parameters:
- `id` (string): Budget ID

Request Body: Budget object (partial updates allowed)

Response:
- Status: 200 OK
- Body: Updated Budget object
- Status: 404 Not Found if budget doesn't exist

### Delete Budget

```
DELETE /api/budgets/{id}
```

Path Parameters:
- `id` (string): Budget ID

Response:
- Status: 204 No Content
- Status: 404 Not Found if budget doesn't exist

### Update Budget Status

```
POST /api/budgets/{id}/status
```

Path Parameters:
- `id` (string): Budget ID

Request Body:
```json
{
  "status": "string" // "active", "paused", "completed"
}
```

Response:
- Status: 200 OK
- Body: Updated Budget object
- Status: 404 Not Found if budget doesn't exist

## Automation Triggers

### List Automation Triggers

```
GET /api/automation/triggers
```

Query Parameters:
- `page` (integer): Page number for pagination (default: 1)
- `limit` (integer): Number of items per page (default: 20)
- `type` (string): Filter by trigger type ("scheduled", "event-based", "threshold")
- `action` (string): Filter by action ("discovery", "sync", "budget-adjustment", "notification")
- `enabled` (boolean): Filter by enabled status

Response:
- Status: 200 OK
- Body: Array of AutomationTrigger objects with pagination metadata

### Get Automation Trigger

```
GET /api/automation/triggers/{id}
```

Path Parameters:
- `id` (string): Trigger ID

Response:
- Status: 200 OK
- Body: AutomationTrigger object
- Status: 404 Not Found if trigger doesn't exist

### Create Automation Trigger

```
POST /api/automation/triggers
```

Request Body: AutomationTrigger object (without id)

Response:
- Status: 201 Created
- Body: Created AutomationTrigger object with id

### Update Automation Trigger

```
PUT /api/automation/triggers/{id}
```

Path Parameters:
- `id` (string): Trigger ID

Request Body: AutomationTrigger object (partial updates allowed)

Response:
- Status: 200 OK
- Body: Updated AutomationTrigger object
- Status: 404 Not Found if trigger doesn't exist

### Delete Automation Trigger

```
DELETE /api/automation/triggers/{id}
```

Path Parameters:
- `id` (string): Trigger ID

Response:
- Status: 204 No Content
- Status: 404 Not Found if trigger doesn't exist

### Enable/Disable Automation Trigger

```
POST /api/automation/triggers/{id}/toggle
```

Path Parameters:
- `id` (string): Trigger ID

Request Body:
```json
{
  "enabled": "boolean"
}
```

Response:
- Status: 200 OK
- Body: Updated AutomationTrigger object
- Status: 404 Not Found if trigger doesn't exist

### Execute Automation Trigger

```
POST /api/automation/triggers/{id}/execute
```

Path Parameters:
- `id` (string): Trigger ID

Response:
- Status: 202 Accepted
- Body: Status object with execution details
- Status: 404 Not Found if trigger doesn't exist

## User Settings

### Get User Settings

```
GET /api/settings
```

Response:
- Status: 200 OK
- Body: UserSettings object

### Update User Settings

```
PUT /api/settings
```

Request Body: UserSettings object (partial updates allowed)

Response:
- Status: 200 OK
- Body: Updated UserSettings object
