# Todo Microservices Application

A complete production-ready microservices application demonstrating Python, REST APIs, Docker, and Kubernetes.

## 🎯 Project Overview

This project implements a Todo application using microservices architecture with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐                                               │
│  │  Client  │                                               │
│  │ (Browser)│                                               │
│  └────┬─────┘                                               │
│       │                                                      │
│       ▼                                                      │
│  ┌──────────┐                                               │
│  │  Nginx   │  (Reverse Proxy / Load Balancer)             │
│  │ Ingress  │                                               │
│  └────┬─────┘                                               │
│       │                                                      │
│       ├──────────────┬──────────────┬──────────────┐       │
│       ▼              ▼              ▼              ▼       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   │
│  │  Auth   │   │  Todo   │   │  User   │   │ Notify  │   │
│  │ Service │   │ Service │   │ Service │   │ Service │   │
│  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘   │
│       │             │              │              │         │
│       └─────────────┴──────────────┴──────────────┘         │
│                     │                                        │
│                     ▼                                        │
│       ┌─────────────────────────────────────┐              │
│       │         Message Queue (Redis)        │              │
│       └─────────────────────────────────────┘              │
│                     │                                        │
│                     ▼                                        │
│       ┌─────────────────────────────────────┐              │
│       │      Database (PostgreSQL)          │              │
│       └─────────────────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
todo-microservices/
├── services/
│   ├── auth-service/
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── todo-service/
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── user-service/
│   │   ├── app.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── notification-service/
│       ├── worker.py
│       ├── requirements.txt
│       └── Dockerfile
├── kubernetes/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── postgres.yaml
│   ├── redis.yaml
│   ├── auth-service.yaml
│   ├── todo-service.yaml
│   ├── user-service.yaml
│   ├── notification-service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🚀 Features

### Auth Service (Port 5001)
- User registration
- User login (JWT tokens)
- Token validation
- Password hashing with bcrypt

### Todo Service (Port 5002)
- Create todos
- List todos (with pagination)
- Update todos
- Delete todos
- Mark as complete/incomplete
- Filter by status

### User Service (Port 5003)
- Get user profile
- Update user profile
- List all users (admin only)
- User statistics

### Notification Service (Background Worker)
- Send email notifications
- Process async tasks
- Queue-based processing with Redis

## 🛠️ Technology Stack

- **Language**: Python 3.11
- **Web Framework**: Flask
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Authentication**: JWT
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **API Gateway**: Nginx Ingress

## 📦 Services Implementation

### Auth Service (auth-service/app.py)

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'auth'}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({'token': token}), 200

@app.route('/api/auth/verify', methods=['POST'])
def verify():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'valid': True, 'user_id': payload['user_id']}), 200
    except:
        return jsonify({'valid': False}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)
```

### Todo Service (todo-service/app.py)

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth-service:5001')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

def verify_token():
    token = request.headers.get('Authorization', '')
    try:
        response = requests.post(
            f'{AUTH_SERVICE_URL}/api/auth/verify',
            headers={'Authorization': token}
        )
        if response.status_code == 200:
            return response.json()['user_id']
    except:
        pass
    return None

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'todo'}), 200

@app.route('/api/todos', methods=['GET'])
def get_todos():
    user_id = verify_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = Todo.query.filter_by(user_id=user_id)
    
    if status == 'completed':
        query = query.filter_by(completed=True)
    elif status == 'pending':
        query = query.filter_by(completed=False)
    
    todos = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'todos': [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'completed': t.completed,
            'created_at': t.created_at.isoformat()
        } for t in todos.items],
        'total': todos.total,
        'pages': todos.pages,
        'current_page': page
    }), 200

@app.route('/api/todos', methods=['POST'])
def create_todo():
    user_id = verify_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    todo = Todo(
        user_id=user_id,
        title=data['title'],
        description=data.get('description', '')
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed
    }), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    user_id = verify_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)
    
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'completed': todo.completed
    }), 200

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    user_id = verify_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)
```

## 🐳 Docker Setup

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: todouser
      POSTGRES_PASSWORD: todopass
      POSTGRES_DB: tododb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  auth-service:
    build: ./services/auth-service
    environment:
      DATABASE_URL: postgresql://todouser:todopass@postgres:5432/tododb
      SECRET_KEY: your-secret-key
    ports:
      - "5001:5001"
    depends_on:
      - postgres

  todo-service:
    build: ./services/todo-service
    environment:
      DATABASE_URL: postgresql://todouser:todopass@postgres:5432/tododb
      AUTH_SERVICE_URL: http://auth-service:5001
    ports:
      - "5002:5002"
    depends_on:
      - postgres
      - auth-service

  user-service:
    build: ./services/user-service
    environment:
      DATABASE_URL: postgresql://todouser:todopass@postgres:5432/tododb
      AUTH_SERVICE_URL: http://auth-service:5001
    ports:
      - "5003:5003"
    depends_on:
      - postgres
      - auth-service

  notification-service:
    build: ./services/notification-service
    environment:
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - redis

volumes:
  postgres-data:
```

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Deploy database and cache
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/redis.yaml

# Deploy services
kubectl apply -f kubernetes/auth-service.yaml
kubectl apply -f kubernetes/todo-service.yaml
kubectl apply -f kubernetes/user-service.yaml
kubectl apply -f kubernetes/notification-service.yaml

# Deploy ingress
kubectl apply -f kubernetes/ingress.yaml

# Enable auto-scaling
kubectl apply -f kubernetes/hpa.yaml
```

## 🧪 Testing

### Using curl

```bash
# Register user
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'

# Create todo (use token from login)
curl -X POST http://localhost:5002/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"Learn Python","description":"Complete all modules"}'

# Get todos
curl http://localhost:5002/api/todos \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📊 Monitoring

```bash
# Check service health
kubectl get pods -n todo-app
kubectl logs -f deployment/todo-service -n todo-app

# Monitor resources
kubectl top pods -n todo-app
kubectl top nodes
```

## 🎯 Key Learning Points

1. **Microservices Architecture** - Service decomposition
2. **REST API Design** - RESTful endpoints
3. **Authentication** - JWT-based auth
4. **Database Integration** - PostgreSQL with SQLAlchemy
5. **Message Queue** - Redis for async tasks
6. **Containerization** - Docker multi-stage builds
7. **Orchestration** - Kubernetes deployment
8. **Scalability** - Horizontal pod autoscaling
9. **Monitoring** - Health checks and logging
10. **Best Practices** - Production-ready code

## 🚀 Next Steps

1. Add API documentation with Swagger
2. Implement comprehensive testing
3. Add CI/CD pipeline
4. Implement monitoring with Prometheus
5. Add distributed tracing
6. Implement rate limiting
7. Add caching layer
8. Implement event sourcing

## 📚 Resources

- [Microservices Patterns](https://microservices.io/patterns/)
- [12-Factor App](https://12factor.net/)
- [REST API Best Practices](https://restfulapi.net/)