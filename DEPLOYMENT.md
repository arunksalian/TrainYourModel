# Resume Classifier API Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- SSL certificate (for production)
- Domain name configured

## Configuration
1. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your production values:
   - Generate strong secret keys
   - Set allowed hosts
   - Configure JWT settings
   - Set file upload limits

## Deployment Steps

### Local Development
1. Build and start the services:
   ```bash
   docker-compose up --build
   ```

2. Access the API at http://localhost:8000
   - API documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

### Production Deployment

1. Set up SSL certificate:
   - Place your SSL certificate and key in a secure location
   - Update nginx.conf with SSL configuration

2. Configure firewall:
   ```bash
   # Allow HTTP/HTTPS
   sudo ufw allow 80
   sudo ufw allow 443
   ```

3. Deploy with Docker Compose:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

4. Monitor the deployment:
   ```bash
   # View logs
   docker-compose logs -f

   # Check container status
   docker-compose ps
   ```

## Security Considerations
1. Always use HTTPS in production
2. Regularly update dependencies
3. Monitor system logs
4. Back up training data regularly
5. Implement rate limiting
6. Use strong API keys

## Scaling
The API can be scaled horizontally by:
1. Adding more API containers:
   ```bash
   docker-compose up -d --scale api=3
   ```
2. Using a load balancer (already configured in nginx)
3. Implementing caching if needed

## Monitoring
1. Health check endpoint: `/health`
2. Container metrics available through Docker
3. Set up monitoring with Prometheus/Grafana (optional)

## Backup and Recovery
1. Regular backups of:
   - Training data
   - Environment configuration
   - Model files

2. Recovery procedure:
   ```bash
   # Stop services
   docker-compose down

   # Restore data
   cp -r backup/training_data ./

   # Restart services
   docker-compose up -d
   ```

## Troubleshooting
1. Check logs:
   ```bash
   docker-compose logs api
   docker-compose logs nginx
   ```

2. Common issues:
   - Permission denied: Check volume mounts
   - Connection refused: Verify service health
   - Memory issues: Adjust container limits
