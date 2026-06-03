# Module 17: Docker Integration

## 🎯 Learning Objectives
- Understand Docker concepts and architecture
- Create Dockerfiles for Python applications
- Build and run Docker containers
- Use Docker Compose for multi-container apps
- Implement best practices for Python Docker images
- Optimize Docker images for production

## 📖 Docker Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Docker Host                         │  │
│  │                                                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │  │
│  │  │Container │  │Container │  │Container │           │  │
│  │  │          │  │          │  │          │           │  │
│  │  │  App A   │  │  App B   │  │  App C   │           │  │
│  │  │          │  │          │  │          │           │  │
│  │  └──────────┘  └──────────┘  └──────────┘           │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │           Docker Engine                        │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │           Host Operating System                │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🐳 Docker vs Virtual Machines

| Feature | Docker Containers | Virtual Machines |
|---------|------------------|------------------|
| **Size** | Lightweight (MBs) | Heavy (GBs) |
| **Startup** | Seconds | Minutes |
| **Performance** | Near-native | Overhead |
| **Isolation** | Process-level | Full OS |
| **Resource Usage** | Shared kernel | Separate OS |
| **Portability** | High | Medium |

## 📦 Basic Docker Commands

```bash
# Images
docker images                    # List images
docker pull python:3.11         # Pull image
docker build -t myapp .         # Build image
docker rmi image_name           # Remove image

# Containers
docker ps                       # List running containers
docker ps -a                    # List all containers
docker run image_name           # Run container
docker stop container_id        # Stop container
docker rm container_id          # Remove container
docker logs container_id        # View logs
docker exec -it container_id bash  # Enter container

# System
docker system prune             # Clean up unused resources
docker system df                # Show disk usage
```

## 🔨 Creating a Dockerfile

### Basic Python Dockerfile

```dockerfile
# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run application
CMD ["python", "app.py"]
```

### Multi-Stage Build (Optimized)

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
```

## 🏗️ Flask Application with Docker

### Project Structure

```
flask-docker-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

### app.py

```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Docker!',
        'environment': os.getenv('FLASK_ENV', 'development')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### requirements.txt

```
flask==3.0.0
gunicorn==21.2.0
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Expose port
EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.gitignore
.mypy_cache
.pytest_cache
.hypothesis
*.db
*.sqlite
.DS_Store
```

### Build and Run

```bash
# Build image
docker build -t flask-app:latest .

# Run container
docker run -d -p 5000:5000 --name my-flask-app flask-app:latest

# Test
curl http://localhost:5000

# View logs
docker logs my-flask-app

# Stop and remove
docker stop my-flask-app
docker rm my-flask-app
```

## 🎼 Docker Compose

### What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications.

### docker-compose.yml

```yaml
version: '3.8'

services:
  # Flask API
  api:
    build: .
    container_name: flask-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    networks:
      - app-network
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

### Docker Compose Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Scale service
docker-compose up -d --scale api=3

# Execute command in service
docker-compose exec api python manage.py migrate
```

## 🚀 Complete Microservices Example

### Project Structure

```
microservices-app/
├── docker-compose.yml
├── api/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── worker/
│   ├── Dockerfile
│   ├── worker.py
│   └── requirements.txt
└── nginx/
    └── nginx.conf
```

### api/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### api/app.py

```python
from flask import Flask, jsonify, request
import redis
import json

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = redis_client.incr('task_counter')
    
    task = {
        'id': task_id,
        'data': data,
        'status': 'pending'
    }
    
    redis_client.set(f'task:{task_id}', json.dumps(task))
    redis_client.lpush('task_queue', task_id)
    
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task_data = redis_client.get(f'task:{task_id}')
    
    if not task_data:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(json.loads(task_data)), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### worker/worker.py

```python
import redis
import json
import time

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

def process_task(task_id):
    """Process a task"""
    task_data = redis_client.get(f'task:{task_id}')
    if not task_data:
        return
    
    task = json.loads(task_data)
    print(f"Processing task {task_id}: {task['data']}")
    
    # Simulate work
    time.sleep(2)
    
    # Update task status
    task['status'] = 'completed'
    redis_client.set(f'task:{task_id}', json.dumps(task))
    print(f"Task {task_id} completed")

def main():
    print("Worker started, waiting for tasks...")
    
    while True:
        # Block until task available
        task_id = redis_client.brpop('task_queue', timeout=1)
        
        if task_id:
            process_task(task_id[1])

if __name__ == '__main__':
    main()
```

## 🔒 Docker Best Practices

### 1. Use Official Base Images

```dockerfile
# ✓ Good
FROM python:3.11-slim

# ✗ Bad
FROM ubuntu:latest
RUN apt-get install python3
```

### 2. Minimize Layers

```dockerfile
# ✓ Good - Single RUN command
RUN apt-get update && \
    apt-get install -y package1 package2 && \
    rm -rf /var/lib/apt/lists/*

# ✗ Bad - Multiple layers
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2
```

### 3. Use .dockerignore

```
# .dockerignore
__pycache__
*.pyc
.git
.env
venv/
*.log
```

### 4. Don't Run as Root

```dockerfile
# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser
```

### 5. Use Multi-Stage Builds

```dockerfile
# Build stage
FROM python:3.11 as builder
# ... build steps

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /app /app
```

## 📊 Docker Image Optimization

### Before Optimization (500 MB)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

### After Optimization (150 MB)

```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

## 🎯 Key Takeaways

1. **Containers are lightweight** - Share host kernel
2. **Dockerfile defines image** - Reproducible builds
3. **Docker Compose for multi-container** - Easy orchestration
4. **Use .dockerignore** - Reduce image size
5. **Multi-stage builds** - Optimize production images
6. **Don't run as root** - Security best practice
7. **Official base images** - Maintained and secure

## 🔗 Next Module

[Module 18: Kubernetes Deployment →](../18-kubernetes/)

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Docker Images](https://hub.docker.com/_/python)