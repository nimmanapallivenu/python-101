# Advanced Python Integrations

A comprehensive guide to integrating Python applications with various services and technologies.

## 🎯 Overview

This project demonstrates real-world integrations including:
- Downstream REST APIs
- Apache Kafka for event streaming
- Redis for caching and queuing
- Database operations (PostgreSQL, MongoDB)
- Ollama API for local LLMs
- Batch processing patterns

```
┌─────────────────────────────────────────────────────────────┐
│              INTEGRATION ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │   Python     │                                           │
│  │ Application  │                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ├──────────► REST APIs (Downstream)                 │
│         │                                                    │
│         ├──────────► Kafka (Event Streaming)                │
│         │              ├─► Producer                         │
│         │              └─► Consumer                         │
│         │                                                    │
│         ├──────────► Redis (Cache/Queue)                    │
│         │              ├─► Cache Layer                      │
│         │              └─► Task Queue                       │
│         │                                                    │
│         ├──────────► Databases                              │
│         │              ├─► PostgreSQL (Relational)          │
│         │              └─► MongoDB (NoSQL)                  │
│         │                                                    │
│         ├──────────► Ollama API (Local LLM)                 │
│         │                                                    │
│         └──────────► Batch Processing                       │
│                        ├─► Scheduled Jobs                   │
│                        └─► Data Pipeline                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
advanced-integrations/
├── api_integration/
│   ├── downstream_api.py
│   ├── retry_handler.py
│   └── circuit_breaker.py
├── kafka_integration/
│   ├── producer.py
│   ├── consumer.py
│   └── event_processor.py
├── redis_integration/
│   ├── cache_manager.py
│   ├── task_queue.py
│   └── rate_limiter.py
├── database_integration/
│   ├── postgres_handler.py
│   ├── mongodb_handler.py
│   └── connection_pool.py
├── ollama_integration/
│   ├── llm_client.py
│   ├── prompt_manager.py
│   └── streaming_handler.py
├── batch_processing/
│   ├── job_scheduler.py
│   ├── data_pipeline.py
│   └── parallel_processor.py
├── docker-compose.yml
└── requirements.txt
```

## 1️⃣ Downstream API Integration

### Basic API Client

```python
# api_integration/downstream_api.py
import requests
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class APIClient:
    """Robust API client with retry and error handling"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Python-API-Client/1.0'
        })
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """GET request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def post(self, endpoint: str, data: Dict) -> Dict[Any, Any]:
        """POST request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

# Usage
api = APIClient("https://api.example.com", api_key="your-key")
data = api.get("/users/123")
```

### Retry Handler with Exponential Backoff

```python
# api_integration/retry_handler.py
import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple

logger = logging.getLogger(__name__)

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator for retry with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Max retries reached for {func.__name__}")
                        raise
                    
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)
            
        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, base_delay=1.0)
def fetch_user_data(user_id: int):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()
```

### Circuit Breaker Pattern

```python
# api_integration/circuit_breaker.py
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker for API calls"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker"""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        return (
            self.last_failure_time and
            datetime.now() - self.last_failure_time >= timedelta(seconds=self.timeout)
        )
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning("Circuit breaker opened")

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

def fetch_data():
    return circuit_breaker.call(api.get, "/data")
```

## 2️⃣ Apache Kafka Integration

### Kafka Producer

```python
# kafka_integration/producer.py
from kafka import KafkaProducer
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EventProducer:
    """Kafka event producer"""
    
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1
        )
    
    def send_event(self, topic: str, event: Dict[Any, Any], key: str = None):
        """Send event to Kafka topic"""
        try:
            future = self.producer.send(topic, value=event, key=key)
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"Event sent to {record_metadata.topic} "
                f"partition {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )
            
            return record_metadata
        except Exception as e:
            logger.error(f"Failed to send event: {e}")
            raise
    
    def close(self):
        """Close producer"""
        self.producer.flush()
        self.producer.close()

# Usage
producer = EventProducer()

# Send user created event
event = {
    "event_type": "user_created",
    "user_id": 123,
    "email": "user@example.com",
    "timestamp": "2024-01-01T10:00:00Z"
}

producer.send_event("user-events", event, key="user-123")
```

### Kafka Consumer

```python
# kafka_integration/consumer.py
from kafka import KafkaConsumer
import json
import logging
from typing import Callable

logger = logging.getLogger(__name__)

class EventConsumer:
    """Kafka event consumer"""
    
    def __init__(
        self,
        topics: list,
        group_id: str,
        bootstrap_servers: str = 'localhost:9092'
    ):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
    
    def consume(self, handler: Callable):
        """Consume events and process with handler"""
        try:
            for message in self.consumer:
                try:
                    logger.info(
                        f"Received event from {message.topic} "
                        f"partition {message.partition} "
                        f"offset {message.offset}"
                    )
                    
                    # Process message
                    handler(message.value)
                    
                    # Commit offset after successful processing
                    self.consumer.commit()
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    # Don't commit offset on error
                    
        except KeyboardInterrupt:
            logger.info("Consumer interrupted")
        finally:
            self.consumer.close()

# Usage
def handle_user_event(event):
    """Process user event"""
    print(f"Processing event: {event['event_type']}")
    # Process event logic here

consumer = EventConsumer(
    topics=['user-events'],
    group_id='user-service-group'
)

consumer.consume(handle_user_event)
```

## 3️⃣ Redis Integration

### Cache Manager

```python
# redis_integration/cache_manager.py
import redis
import json
import logging
from typing import Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class CacheManager:
    """Redis cache manager"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        try:
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete key from cache"""
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return self.redis_client.exists(key) > 0

def cached(ttl: int = 3600):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = CacheManager()
            
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.info(f"Cached result for {cache_key}")
            
            return result
        return wrapper
    return decorator

# Usage
@cached(ttl=300)
def get_user_data(user_id: int):
    """Expensive database query"""
    # Simulate expensive operation
    return {"id": user_id, "name": "John Doe"}
```

### Task Queue with Redis

```python
# redis_integration/task_queue.py
import redis
import json
import time
from typing import Callable, Dict
import logging

logger = logging.getLogger(__name__)

class TaskQueue:
    """Redis-based task queue"""
    
    def __init__(self, queue_name: str = 'tasks', host: str = 'localhost'):
        self.queue_name = queue_name
        self.redis_client = redis.Redis(host=host, decode_responses=True)
    
    def enqueue(self, task: Dict):
        """Add task to queue"""
        try:
            self.redis_client.lpush(self.queue_name, json.dumps(task))
            logger.info(f"Task enqueued: {task.get('id')}")
        except Exception as e:
            logger.error(f"Failed to enqueue task: {e}")
            raise
    
    def dequeue(self, timeout: int = 0) -> Dict:
        """Get task from queue (blocking)"""
        try:
            result = self.redis_client.brpop(self.queue_name, timeout=timeout)
            if result:
                _, task_json = result
                return json.loads(task_json)
            return None
        except Exception as e:
            logger.error(f"Failed to dequeue task: {e}")
            return None
    
    def process_tasks(self, handler: Callable):
        """Process tasks from queue"""
        logger.info(f"Starting task processor for {self.queue_name}")
        
        while True:
            try:
                task = self.dequeue(timeout=5)
                if task:
                    logger.info(f"Processing task: {task.get('id')}")
                    handler(task)
            except KeyboardInterrupt:
                logger.info("Task processor stopped")
                break
            except Exception as e:
                logger.error(f"Error processing task: {e}")

# Usage
queue = TaskQueue('email-queue')

# Producer
queue.enqueue({
    'id': '123',
    'type': 'send_email',
    'to': 'user@example.com',
    'subject': 'Welcome!'
})

# Consumer
def handle_email_task(task):
    print(f"Sending email to {task['to']}")
    # Send email logic

queue.process_tasks(handle_email_task)
```

## 4️⃣ Database Integration

### PostgreSQL Handler

```python
# database_integration/postgres_handler.py
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class PostgreSQLHandler:
    """PostgreSQL database handler with connection pooling"""
    
    def __init__(self, config: dict):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            port=config.get('port', 5432)
        )
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool"""
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute SELECT query"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    
    def execute_update(self, query: str, params: tuple = None):
        """Execute INSERT/UPDATE/DELETE query"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount

# Usage
db = PostgreSQLHandler({
    'host': 'localhost',
    'database': 'mydb',
    'user': 'user',
    'password': 'password'
})

# Query
users = db.execute_query("SELECT * FROM users WHERE age > %s", (25,))

# Insert
db.execute_update(
    "INSERT INTO users (name, email) VALUES (%s, %s)",
    ("John Doe", "john@example.com")
)
```

### MongoDB Handler

```python
# database_integration/mongodb_handler.py
from pymongo import MongoClient
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class MongoDBHandler:
    """MongoDB handler"""
    
    def __init__(self, connection_string: str, database: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[database]
    
    def insert_one(self, collection: str, document: Dict) -> str:
        """Insert single document"""
        result = self.db[collection].insert_one(document)
        return str(result.inserted_id)
    
    def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        """Find single document"""
        return self.db[collection].find_one(query)
    
    def find_many(self, collection: str, query: Dict) -> List[Dict]:
        """Find multiple documents"""
        return list(self.db[collection].find(query))
    
    def update_one(self, collection: str, query: Dict, update: Dict):
        """Update single document"""
        result = self.db[collection].update_one(query, {'$set': update})
        return result.modified_count
    
    def delete_one(self, collection: str, query: Dict):
        """Delete single document"""
        result = self.db[collection].delete_one(query)
        return result.deleted_count

# Usage
mongo = MongoDBHandler('mongodb://localhost:27017', 'mydb')

# Insert
user_id = mongo.insert_one('users', {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# Find
user = mongo.find_one('users', {'email': 'john@example.com'})
```

## 5️⃣ Ollama API Integration

### LLM Client

```python
# ollama_integration/llm_client.py
import requests
import json
from typing import Generator, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for Ollama local LLM API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        options: Optional[Dict] = None
    ):
        """Generate completion"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        if options:
            payload["options"] = options
        
        if stream:
            return self._stream_response(url, payload)
        else:
            return self._single_response(url, payload)
    
    def _single_response(self, url: str, payload: Dict) -> str:
        """Get single response"""
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['response']
    
    def _stream_response(self, url: str, payload: Dict) -> Generator:
        """Stream response"""
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if not data.get('done'):
                    yield data['response']
    
    def chat(
        self,
        model: str,
        messages: list,
        stream: bool = False
    ):
        """Chat completion"""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        if stream:
            return self._stream_chat(url, payload)
        else:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()['message']['content']
    
    def _stream_chat(self, url: str, payload: Dict) -> Generator:
        """Stream chat response"""
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if not data.get('done'):
                    yield data['message']['content']

# Usage
ollama = OllamaClient()

# Simple generation
response = ollama.generate(
    model="llama2",
    prompt="Explain Python in one sentence"
)
print(response)

# Streaming generation
for chunk in ollama.generate(
    model="llama2",
    prompt="Write a short poem about Python",
    stream=True
):
    print(chunk, end='', flush=True)

# Chat
messages = [
    {"role": "user", "content": "What is Python?"}
]
response = ollama.chat(model="llama2", messages=messages)
print(response)
```

## 6️⃣ Batch Processing

### Job Scheduler

```python
# batch_processing/job_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

class JobScheduler:
    """Schedule and run batch jobs"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def add_job(self, func, trigger, **kwargs):
        """Add scheduled job"""
        self.scheduler.add_job(func, trigger, **kwargs)
        logger.info(f"Added job: {func.__name__}")
    
    def add_cron_job(self, func, cron_expression: str):
        """Add cron-style job"""
        trigger = CronTrigger.from_crontab(cron_expression)
        self.add_job(func, trigger)
    
    def start(self):
        """Start scheduler"""
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def shutdown(self):
        """Shutdown scheduler"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

# Usage
scheduler = JobScheduler()

def daily_report():
    print("Generating daily report...")
    # Report generation logic

def hourly_sync():
    print("Syncing data...")
    # Data sync logic

# Run daily at 9 AM
scheduler.add_cron_job(daily_report, "0 9 * * *")

# Run every hour
scheduler.add_cron_job(hourly_sync, "0 * * * *")

scheduler.start()
```

### Data Pipeline

```python
# batch_processing/data_pipeline.py
from typing import Callable, List, Any
import logging

logger = logging.getLogger(__name__)

class DataPipeline:
    """ETL data pipeline"""
    
    def __init__(self):
        self.steps: List[Callable] = []
    
    def add_step(self, step: Callable):
        """Add processing step"""
        self.steps.append(step)
        return self
    
    def execute(self, data: Any) -> Any:
        """Execute pipeline"""
        result = data
        
        for i, step in enumerate(self.steps):
            try:
                logger.info(f"Executing step {i + 1}: {step.__name__}")
                result = step(result)
            except Exception as e:
                logger.error(f"Error in step {i + 1}: {e}")
                raise
        
        return result

# Usage
def extract_data():
    """Extract data from source"""
    return [{"id": 1, "value": 100}, {"id": 2, "value": 200}]

def transform_data(data):
    """Transform data"""
    return [{"id": item["id"], "value": item["value"] * 2} for item in data]

def load_data(data):
    """Load data to destination"""
    print(f"Loading {len(data)} records")
    return data

pipeline = DataPipeline()
pipeline.add_step(extract_data)
pipeline.add_step(transform_data)
pipeline.add_step(load_data)

result = pipeline.execute(None)
```

## 🐳 Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama

volumes:
  postgres-data:
  mongo-data:
  ollama-data:
```

## 📦 Requirements

```txt
# requirements.txt
requests==2.31.0
kafka-python==2.0.2
redis==5.0.1
psycopg2-binary==2.9.9
pymongo==4.6.1
APScheduler==3.10.4
python-dotenv==1.0.0
```

## 🚀 Getting Started

```bash
# Start all services
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run examples
python api_integration/downstream_api.py
python kafka_integration/producer.py
python redis_integration/cache_manager.py
```

## 🎯 Key Takeaways

1. **API Integration** - Retry, circuit breaker, error handling
2. **Kafka** - Event streaming, producer/consumer patterns
3. **Redis** - Caching, task queues, rate limiting
4. **Databases** - Connection pooling, transactions
5. **Ollama** - Local LLM integration, streaming
6. **Batch Processing** - Scheduling, pipelines, parallel processing

## 📚 Additional Resources

- [Kafka Python Documentation](https://kafka-python.readthedocs.io/)
- [Redis Python Documentation](https://redis-py.readthedocs.io/)
- [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)