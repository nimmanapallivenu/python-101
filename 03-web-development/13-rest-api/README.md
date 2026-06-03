# Module 13: REST API Development

## 🎯 Learning Objectives
- Understand REST API principles and architecture
- Build RESTful APIs with Flask and FastAPI
- Implement CRUD operations
- Handle request/response with JSON
- Implement authentication and authorization
- Add error handling and validation
- Document APIs with Swagger/OpenAPI

## 📖 REST API Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    REST API ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CLIENT                    SERVER                            │
│  ┌──────┐                 ┌──────┐                          │
│  │      │  HTTP Request   │      │                          │
│  │ App  │ ──────────────> │ API  │                          │
│  │      │                 │      │                          │
│  │      │  HTTP Response  │      │                          │
│  │      │ <────────────── │      │                          │
│  └──────┘                 └──────┘                          │
│                              │                               │
│                              ▼                               │
│                         ┌─────────┐                         │
│                         │Database │                         │
│                         └─────────┘                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🔑 REST Principles

### 1. HTTP Methods (CRUD Operations)

| Method | Operation | Description | Idempotent |
|--------|-----------|-------------|------------|
| GET | Read | Retrieve resource(s) | Yes |
| POST | Create | Create new resource | No |
| PUT | Update | Update entire resource | Yes |
| PATCH | Update | Partial update | No |
| DELETE | Delete | Remove resource | Yes |

### 2. Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server error |

### 3. RESTful URL Structure

```
Good REST API URLs:
✓ GET    /api/users              - Get all users
✓ GET    /api/users/123          - Get user by ID
✓ POST   /api/users              - Create new user
✓ PUT    /api/users/123          - Update user
✓ DELETE /api/users/123          - Delete user
✓ GET    /api/users/123/orders   - Get user's orders

Bad URLs:
✗ GET    /api/getUsers
✗ POST   /api/createUser
✗ GET    /api/user?action=delete
```

## 🚀 Flask REST API

### Basic Setup

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory database (for demo)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### CRUD Operations

```python
# GET all users
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify({"users": users, "count": len(users)}), 200

# GET single user
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user), 200

# POST - Create user
@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    
    # Validation
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400
    
    # Create new user
    new_user = {
        "id": max([u['id'] for u in users]) + 1 if users else 1,
        "name": data['name'],
        "email": data['email']
    }
    
    users.append(new_user)
    return jsonify(new_user), 201

# PUT - Update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    
    return jsonify(user), 200

# DELETE user
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted successfully"}), 200
```

## ⚡ FastAPI (Modern Alternative)

### Why FastAPI?

- **Fast**: High performance, on par with NodeJS and Go
- **Type hints**: Built-in validation using Python type hints
- **Auto documentation**: Automatic Swagger UI
- **Async support**: Native async/await support
- **Modern**: Based on latest Python features

### Basic FastAPI Setup

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI(title="User API", version="1.0.0")

# Pydantic models for validation
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

# In-memory database
users_db = []
user_id_counter = 1

@app.get("/")
def root():
    return {"message": "Welcome to User API"}

@app.get("/api/users", response_model=List[User])
def get_users():
    """Get all users"""
    return users_db

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get user by ID"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Create new user"""
    global user_id_counter
    
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email
    }
    
    users_db.append(new_user)
    user_id_counter += 1
    
    return new_user

@app.put("/api/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate):
    """Update user"""
    existing_user = next((u for u in users_db if u["id"] == user_id), None)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user["name"] = user.name
    existing_user["email"] = user.email
    
    return existing_user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Delete user"""
    global users_db
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db = [u for u in users_db if u["id"] != user_id]
    return None
```

### Run FastAPI

```bash
# Install
pip install fastapi uvicorn

# Run
uvicorn main:app --reload

# Access Swagger UI
# http://localhost:8000/docs

# Access ReDoc
# http://localhost:8000/redoc
```

## 🔐 Authentication & Authorization

### JWT Authentication

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    
    return user

# Login endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoint
@app.get("/api/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## 🛡️ Error Handling

### Custom Error Handlers

```python
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Custom exception
class ValidationError(Exception):
    pass

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({"error": str(error)}), 400
```

## 📊 Request/Response Examples

### JSON Request Body

```python
# POST /api/users
{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}
```

### JSON Response

```python
# Success Response (201 Created)
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "created_at": "2024-01-01T10:00:00Z"
}

# Error Response (400 Bad Request)
{
    "error": "Validation failed",
    "details": {
        "email": "Invalid email format"
    }
}
```

## 🧪 Testing REST APIs

### Using curl

```bash
# GET request
curl http://localhost:5000/api/users

# POST request
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# PUT request
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","email":"john@example.com"}'

# DELETE request
curl -X DELETE http://localhost:5000/api/users/1

# With authentication
curl http://localhost:5000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:5000/api"

# GET
response = requests.get(f"{BASE_URL}/users")
print(response.json())

# POST
new_user = {"name": "John", "email": "john@example.com"}
response = requests.post(f"{BASE_URL}/users", json=new_user)
print(response.json())

# PUT
updated_user = {"name": "John Updated", "email": "john@example.com"}
response = requests.put(f"{BASE_URL}/users/1", json=updated_user)
print(response.json())

# DELETE
response = requests.delete(f"{BASE_URL}/users/1")
print(response.status_code)
```

## 📁 Project Structure

```
rest-api-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models.py            # Data models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   ├── auth.py              # Authentication logic
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User routes
│       └── products.py      # Product routes
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_products.py
├── requirements.txt
├── .env
└── README.md
```

## 💻 Complete Examples

See the following files:
- `flask_api.py` - Complete Flask REST API
- `fastapi_api.py` - Complete FastAPI implementation
- `api_client.py` - API client examples
- `test_api.py` - API testing examples

## 🎯 Key Takeaways

1. **REST principles** - Use proper HTTP methods and status codes
2. **URL structure** - Keep URLs resource-oriented
3. **JSON format** - Standard for request/response
4. **Validation** - Always validate input data
5. **Error handling** - Provide meaningful error messages
6. **Authentication** - Secure your APIs with JWT
7. **Documentation** - Use Swagger/OpenAPI
8. **Testing** - Write comprehensive API tests

## 🔗 Next Module

[Module 14: Database Integration →](../14-database-integration/)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)