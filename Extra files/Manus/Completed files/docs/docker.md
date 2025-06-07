# Affiliate Matrix Docker Configuration

This directory contains Docker configuration files for the Affiliate Matrix system.

## Overview

The Affiliate Matrix system is containerized using Docker to ensure consistent development and deployment across different environments. The configuration includes:

- Docker Compose setup for local development
- Production-ready Dockerfiles for backend and frontend
- Environment configuration for different deployment scenarios
- Volume management for persistent data

## Getting Started

### Prerequisites

- Docker Engine 20.10.0+
- Docker Compose 2.0.0+

### Development Setup

1. Clone the repository
2. Navigate to the project root directory
3. Run the following command:

```bash
docker-compose up
```

This will start all services defined in the `docker-compose.yml` file:
- Backend API (FastAPI)
- Frontend (Vue.js)
- Database (PostgreSQL)
- Vault (optional, for secure credential storage)

### Accessing Services

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Vault UI: http://localhost:8200

## Configuration

### Environment Variables

The system uses environment variables for configuration. These can be set in the following ways:

1. In the `docker-compose.yml` file (for development)
2. In `.env` files (for different environments)
3. Directly in the environment (for production deployments)

#### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| ENVIRONMENT | Application environment | development |
| LOG_LEVEL | Logging level | debug |
| DATABASE_URL | Database connection string | postgresql://postgres:postgres@db:5432/affiliate_matrix |
| ENABLE_FEATURE_FLAGS | Enable feature flags | true |
| FEATURE_FLAGS | JSON string of feature flag overrides | {} |

#### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| NODE_ENV | Node environment | development |
| VITE_API_BASE_URL | Backend API base URL | http://localhost:8000 |

### Volumes

The Docker Compose configuration includes the following volumes:

- `postgres_data`: Persistent storage for the PostgreSQL database

## Production Deployment

For production deployment, you can use the provided Dockerfiles to build optimized images:

### Building Production Images

```bash
# Build backend image
docker build -t affiliate-matrix-backend:latest ./backend

# Build frontend image
docker build -t affiliate-matrix-frontend:latest ./frontend
```

### Running in Production

In a production environment, you would typically deploy these images using an orchestration tool like Kubernetes or Docker Swarm. Here's a simple example using Docker Compose:

```bash
# Create a production docker-compose file
cat > docker-compose.prod.yml << EOL
version: '3.8'

services:
  backend:
    image: affiliate-matrix-backend:latest
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/affiliate_matrix
      - ENABLE_FEATURE_FLAGS=true
    ports:
      - "8000:8000"
    depends_on:
      - db
    networks:
      - affiliate_matrix_network

  frontend:
    image: affiliate-matrix-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - affiliate_matrix_network

  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=affiliate_matrix
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - affiliate_matrix_network

networks:
  affiliate_matrix_network:
    driver: bridge

volumes:
  postgres_data:
EOL

# Run in production mode
docker-compose -f docker-compose.prod.yml up -d
```

## Advanced Configuration

### Scaling

The backend service can be scaled horizontally:

```bash
docker-compose up -d --scale backend=3
```

### Health Checks

Health checks are configured for all services to ensure they are running correctly:

- Backend: HTTP check on `/health`
- Frontend: HTTP check on `/`
- Database: PostgreSQL connection check

### Resource Limits

Resource limits can be configured in the Docker Compose file:

```yaml
services:
  backend:
    # ...
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check that the database service is running
   - Verify the DATABASE_URL environment variable

2. **Frontend cannot connect to backend**:
   - Check that the backend service is running
   - Verify the VITE_API_BASE_URL environment variable

3. **Volume permission issues**:
   - Ensure the postgres_data volume has the correct permissions

### Viewing Logs

```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f
```

## Security Considerations

1. **Environment Variables**:
   - Do not commit sensitive environment variables to version control
   - Use a secrets management solution for production deployments

2. **Network Security**:
   - In production, use a reverse proxy with HTTPS
   - Configure network policies to restrict access between services

3. **Container Security**:
   - Run containers with non-root users
   - Use minimal base images to reduce attack surface
