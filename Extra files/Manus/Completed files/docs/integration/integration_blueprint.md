# Affiliate Matrix Integration Documentation

## Overview

This document outlines how the frontend and backend components of the Affiliate Matrix system integrate with each other. It provides a comprehensive guide for developers to understand the system architecture, data flow, and communication patterns between components.

## System Architecture

The Affiliate Matrix system follows a client-server architecture with a clear separation between frontend and backend:

### Backend (FastAPI)
- RESTful API built with Python FastAPI
- Handles data processing, business logic, and persistence
- Provides standardized endpoints for all system functionality
- Implements validation using Pydantic models

### Frontend (Vue.js)
- Single-page application built with Vue 3 and TypeScript
- Uses Composition API for reusable logic
- Implements Pinia stores for state management
- Communicates with backend via HTTP requests

## Communication Flow

1. **Frontend to Backend Communication**:
   - Frontend composables make HTTP requests to backend endpoints
   - Requests are processed through Axios HTTP client
   - Responses update Pinia stores which trigger UI updates

2. **Backend to Frontend Communication**:
   - Backend responds to HTTP requests with JSON data
   - Response formats follow the OpenAPI specification
   - Error handling includes appropriate HTTP status codes and error messages

## Integration Points

### 1. Programs Management

**Frontend Components**:
- `usePrograms` composable: Handles API calls for program operations
- `programsStore`: Manages program state and provides access to components

**Backend Endpoints**:
- `GET /api/programs`: List all programs with pagination and filtering
- `POST /api/programs`: Create a new program
- `GET /api/programs/{id}`: Get a specific program
- `PUT /api/programs/{id}`: Update a program
- `DELETE /api/programs/{id}`: Delete a program
- `GET /api/programs/{id}/metrics`: Get program performance metrics

**Data Flow Example**:
```
User action → Vue component → usePrograms.fetchPrograms() → 
HTTP GET /api/programs → Backend processes request → 
JSON response → programsStore.fetchPrograms updates state → 
UI updates with new data
```

### 2. Connections Management

**Frontend Components**:
- `useConnections` composable: Handles API calls for connection operations
- `connectionsStore`: Manages connection state and provides access to components

**Backend Endpoints**:
- `GET /api/connections`: List all connections with pagination and filtering
- `POST /api/connections`: Create a new connection
- `GET /api/connections/{id}`: Get a specific connection
- `PUT /api/connections/{id}`: Update a connection
- `DELETE /api/connections/{id}`: Delete a connection
- `POST /api/connections/{id}/sync`: Trigger synchronization
- `POST /api/connections/{id}/test`: Test connection

**Integration Notes**:
- Connection status updates may take time to complete
- Frontend should poll for status updates after triggering sync operations

### 3. Discovery Process

**Frontend Components**:
- `useDiscovery` composable: Handles API calls for discovery operations
- `discoveryStore`: Manages discovery state and provides access to components

**Backend Endpoints**:
- `GET /api/discovery`: List all discovery results with pagination and filtering
- `POST /api/discovery`: Start a new discovery operation
- `GET /api/discovery/{id}`: Get a specific discovery result
- `POST /api/discovery/{id}/cancel`: Cancel an in-progress discovery
- `POST /api/discovery/{id}/items/{itemId}/process`: Process a discovery item

**Integration Notes**:
- Discovery operations are asynchronous and may take time to complete
- Frontend should poll for status updates after starting discovery
- Processing discovery items updates both the item and the parent discovery result

### 4. System Monitoring

**Frontend Components**:
- `useSystem` composable: Handles API calls for system operations
- `systemStore`: Manages system state and provides access to components

**Backend Endpoints**:
- `GET /api/system/metrics`: Get system performance metrics
- `GET /api/system/logs`: Get system logs with filtering
- `GET /api/system/status`: Get current system status

**Integration Notes**:
- System metrics should be refreshed periodically (e.g., every minute)
- Log retrieval should use pagination and filtering to manage data volume

### 5. Budget Management

**Frontend Components**:
- `useBudgets` composable: Handles API calls for budget operations
- `budgetsStore`: Manages budget state and provides access to components

**Backend Endpoints**:
- `GET /api/budgets`: List all budgets with pagination and filtering
- `POST /api/budgets`: Create a new budget
- `GET /api/budgets/{id}`: Get a specific budget
- `PUT /api/budgets/{id}`: Update a budget
- `DELETE /api/budgets/{id}`: Delete a budget
- `POST /api/budgets/{id}/status`: Update budget status

**Integration Notes**:
- Budget allocations are managed as part of the budget entity
- Performance metrics are calculated by the backend and included in responses

### 6. Automation

**Frontend Components**:
- `useAutomation` composable: Handles API calls for automation operations
- `automationStore`: Manages automation state and provides access to components

**Backend Endpoints**:
- `GET /api/automation/triggers`: List all automation triggers
- `POST /api/automation/triggers`: Create a new trigger
- `GET /api/automation/triggers/{id}`: Get a specific trigger
- `PUT /api/automation/triggers/{id}`: Update a trigger
- `DELETE /api/automation/triggers/{id}`: Delete a trigger
- `POST /api/automation/triggers/{id}/toggle`: Enable/disable a trigger
- `POST /api/automation/triggers/{id}/execute`: Manually execute a trigger

**Integration Notes**:
- Trigger execution is asynchronous
- Frontend should display appropriate loading and success/error states

### 7. User Settings

**Frontend Components**:
- `useSettings` composable: Handles API calls for settings operations
- `settingsStore`: Manages settings state and provides access to components

**Backend Endpoints**:
- `GET /api/settings`: Get user settings
- `PUT /api/settings`: Update user settings

**Integration Notes**:
- Settings are applied immediately after update
- Theme changes should trigger UI updates without page reload

## Error Handling

### Frontend Error Handling
- All composables implement consistent error handling
- Errors are captured and stored in both composables and stores
- UI components can access error states to display appropriate messages
- Network errors are distinguished from validation and business logic errors

### Backend Error Handling
- HTTP status codes indicate the type of error
- Error responses include detailed messages for debugging
- Validation errors return 422 status with field-specific error details
- Authentication/authorization errors return 401/403 status

## Authentication Flow

1. User credentials are sent to authentication endpoint
2. Backend validates credentials and returns JWT token
3. Frontend stores token in secure storage
4. Subsequent requests include token in Authorization header
5. Backend validates token for each protected endpoint
6. Token expiration is handled with refresh token mechanism

## Performance Considerations

1. **Pagination**:
   - All list endpoints support pagination
   - Frontend should respect pagination limits
   - Infinite scrolling implemented for large data sets

2. **Caching**:
   - Frontend implements caching for frequently accessed data
   - Cache invalidation occurs on data updates
   - Backend sets appropriate cache headers

3. **Lazy Loading**:
   - Frontend implements lazy loading for components and routes
   - Data is fetched only when needed

## Testing Integration

1. **Backend Tests**:
   - Unit tests for each endpoint
   - Integration tests for complex workflows
   - Tests verify correct response formats and status codes

2. **Frontend Tests**:
   - Unit tests for composables and stores
   - Tests verify correct API calls and state updates
   - Mock responses simulate backend behavior

3. **End-to-End Tests**:
   - Test complete user workflows
   - Verify data consistency between frontend and backend

## Deployment Considerations

1. **API Versioning**:
   - API endpoints include version in path
   - Frontend specifies required API version
   - Backward compatibility maintained for minor versions

2. **Environment Configuration**:
   - Frontend uses environment variables for API base URL
   - Backend configuration varies by deployment environment
   - Deployment scripts handle environment-specific settings

## Future Integration Enhancements

1. **Real-time Updates**:
   - Implement WebSocket connection for real-time data updates
   - Notify frontend of backend state changes without polling

2. **Offline Support**:
   - Implement service workers for offline functionality
   - Queue operations when offline for later synchronization

3. **Performance Monitoring**:
   - Add client-side performance tracking
   - Correlate frontend and backend performance metrics
