# Running UniERP with Docker

This guide explains how to run UniERP using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose v2.0 or later
- At least 4GB of RAM available for Docker

## Quick Start

1. **Clone or download the UniERP project** (if you haven't already)

2. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

3. **Wait for the services to be ready** (this may take a few minutes on first run):
   ```bash
   docker-compose logs -f
   ```

4. **Access UniERP**:
   - Open your browser and go to: http://localhost:8019
   - Use the master password: `admin123`
   - Create a new database to get started

## Services

The Docker Compose setup includes:

- **unierp_app**: The UniERP application server
  - Port 8019: HTTP interface
  - Port 8072: Longpolling interface
- **unierp_db**: PostgreSQL database server
  - Port 5432: Database connection

## Configuration

The configuration is managed through the `unierp.conf` file. The Docker setup uses the following defaults:

- Database host: `db` (the PostgreSQL container)
- Database port: `5432`
- Database user: `unierp`
- Database password: `unierp`
- HTTP port: `8019`
- Longpolling port: `8072`

### Customizing Configuration

You can modify the `unierp.conf` file before starting the containers, or you can override settings using environment variables in the `docker-compose.yml` file.

## Data Persistence

The following data volumes are created to persist data:

- `postgres_data`: PostgreSQL database data
- `unierp_data`: UniERP filestore and session data
- `unierp_logs`: Application logs

## Common Commands

### Start the services
```bash
docker-compose up -d
```

### Stop the services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f unierp
docker-compose logs -f db
```

### Rebuild the UniERP image
```bash
docker-compose build --no-cache unierp
```

### Access the UniERP container
```bash
docker-compose exec unierp bash
```

### Access the database container
```bash
docker-compose exec db psql -U unierp -d postgres
```

## Development

For development purposes, you might want to mount additional volumes:

```yaml
volumes:
  - ./odoo:/opt/unierp/odoo
  - ./addons:/opt/unierp/addons
```

This allows you to modify the source code on your host machine and see the changes reflected immediately in the container.

## Troubleshooting

### Database Connection Issues
If UniERP cannot connect to the database:
1. Ensure the database container is healthy: `docker-compose ps`
2. Check the database logs: `docker-compose logs db`
3. Wait a bit longer for PostgreSQL to fully initialize

### Permission Issues
If you encounter permission errors with the filestore:
```bash
sudo chown -R 1000:1000 ./data/unierp
```

### Port Conflicts
If ports 8019, 8072, or 5432 are already in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "8019:8019"  # Change to "8020:8019" if 8019 is in use
```

## Production Considerations

For production use, consider:

1. **Security**:
   - Change default passwords
   - Use environment variables for sensitive data
   - Enable HTTPS

2. **Performance**:
   - Increase worker count based on CPU cores
   - Adjust memory limits
   - Use a reverse proxy (nginx)

3. **Backup**:
   - Regular database backups
   - Filestore backups

4. **Monitoring**:
   - Implement health checks
   - Set up log aggregation

## Environment Variables

You can override configuration using environment variables:

```yaml
environment:
  ODOO_RC: /etc/unierp/unierp.conf
  HOST: 0.0.0.0
  PORT: 8019
  WORKERS: 4
  LIMIT_MEMORY_HARD: 1073741824
  LIMIT_MEMORY_SOFT: 838860800
  LIMIT_REQUEST: 8192
  LIMIT_TIME_CPU: 600
  LIMIT_TIME_REAL: 1200
```

## Support

For issues related to:
- UniERP functionality: Check the UniERP documentation
- Docker setup: Create an issue in the project repository
- Docker itself: Refer to Docker documentation