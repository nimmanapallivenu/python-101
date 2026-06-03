# Module 21: Async Programming

## 🎯 Learning Objectives
- Understand asynchronous programming concepts
- Master async/await syntax
- Work with asyncio library
- Handle concurrent operations
- Build async web applications
- Implement async database operations

## 📖 Async Programming Overview

```
┌─────────────────────────────────────────────────────────────┐
│              SYNCHRONOUS VS ASYNCHRONOUS                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SYNCHRONOUS (Blocking):                                    │
│  Task 1 ████████████ (wait)                                │
│  Task 2              ████████████ (wait)                   │
│  Task 3                           ████████████             │
│  Total Time: ████████████████████████████████████          │
│                                                              │
│  ASYNCHRONOUS (Non-blocking):                               │
│  Task 1 ████████████                                        │
│  Task 2 ████████████                                        │
│  Task 3 ████████████                                        │
│  Total Time: ████████████                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Basic Async/Await

### Simple Async Function

```python
import asyncio

# Define async function
async def greet(name):
    """Async function using async def"""
    print(f"Hello, {name}!")
    await asyncio.sleep(1)  # Simulate I/O operation
    print(f"Goodbye, {name}!")

# Run async function
asyncio.run(greet("Alice"))
```

### Multiple Async Tasks

```python
import asyncio

async def fetch_data(id):
    """Simulate fetching data"""
    print(f"Fetching data {id}...")
    await asyncio.sleep(2)  # Simulate network delay
    print(f"Data {id} fetched!")
    return f"Data {id}"

async def main():
    """Run multiple tasks concurrently"""
    # Sequential execution (slow)
    result1 = await fetch_data(1)
    result2 = await fetch_data(2)
    result3 = await fetch_data(3)
    # Total time: ~6 seconds
    
    # Concurrent execution (fast)
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3)
    )
    # Total time: ~2 seconds
    print(results)

asyncio.run(main())
```

## 2️⃣ Asyncio Patterns

### Creating Tasks

```python
import asyncio

async def task_function(name, delay):
    """Task that takes some time"""
    print(f"{name} starting...")
    await asyncio.sleep(delay)
    print(f"{name} completed!")
    return f"{name} result"

async def main():
    # Create tasks
    task1 = asyncio.create_task(task_function("Task 1", 2))
    task2 = asyncio.create_task(task_function("Task 2", 1))
    task3 = asyncio.create_task(task_function("Task 3", 3))
    
    # Wait for all tasks
    results = await asyncio.gather(task1, task2, task3)
    print(f"Results: {results}")

asyncio.run(main())
```

### Timeout Handling

```python
import asyncio

async def slow_operation():
    """Operation that might take too long"""
    await asyncio.sleep(5)
    return "Completed"

async def main():
    try:
        # Set timeout of 2 seconds
        result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out!")

asyncio.run(main())
```

## 3️⃣ Async HTTP Requests

### Using aiohttp

```python
import aiohttp
import asyncio

async def fetch_url(session, url):
    """Fetch URL asynchronously"""
    async with session.get(url) as response:
        return await response.text()

async def fetch_multiple_urls(urls):
    """Fetch multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Usage
urls = [
    'https://api.example.com/users/1',
    'https://api.example.com/users/2',
    'https://api.example.com/users/3'
]

results = asyncio.run(fetch_multiple_urls(urls))
```

### Async API Client

```python
import aiohttp
import asyncio
from typing import List, Dict

class AsyncAPIClient:
    """Async API client"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.session.close()
    
    async def get(self, endpoint: str) -> Dict:
        """GET request"""
        url = f"{self.base_url}/{endpoint}"
        async with self.session.get(url) as response:
            return await response.json()
    
    async def post(self, endpoint: str, data: Dict) -> Dict:
        """POST request"""
        url = f"{self.base_url}/{endpoint}"
        async with self.session.post(url, json=data) as response:
            return await response.json()
    
    async def fetch_all(self, endpoints: List[str]) -> List[Dict]:
        """Fetch multiple endpoints concurrently"""
        tasks = [self.get(endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)

# Usage
async def main():
    async with AsyncAPIClient("https://api.example.com") as client:
        # Single request
        user = await client.get("users/1")
        
        # Multiple requests
        endpoints = ["users/1", "users/2", "users/3"]
        users = await client.fetch_all(endpoints)
        print(users)

asyncio.run(main())
```

## 4️⃣ Async Database Operations

### Async PostgreSQL

```python
import asyncpg
import asyncio

class AsyncDatabase:
    """Async PostgreSQL database handler"""
    
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool = None
    
    async def connect(self):
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(self.dsn)
    
    async def close(self):
        """Close connection pool"""
        await self.pool.close()
    
    async def fetch_one(self, query: str, *args):
        """Fetch single row"""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def fetch_all(self, query: str, *args):
        """Fetch multiple rows"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def execute(self, query: str, *args):
        """Execute query"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

# Usage
async def main():
    db = AsyncDatabase("postgresql://user:pass@localhost/db")
    await db.connect()
    
    # Fetch users
    users = await db.fetch_all("SELECT * FROM users WHERE age > $1", 25)
    
    # Insert user
    await db.execute(
        "INSERT INTO users (name, email) VALUES ($1, $2)",
        "John Doe", "john@example.com"
    )
    
    await db.close()

asyncio.run(main())
```

## 5️⃣ Async Web Framework (FastAPI)

### Basic FastAPI App

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    """Async endpoint"""
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Fetch user asynchronously"""
    # Simulate database query
    await asyncio.sleep(0.1)
    return {"user_id": user_id, "name": "John Doe"}

@app.get("/data")
async def get_data():
    """Fetch data from multiple sources"""
    # Concurrent API calls
    results = await asyncio.gather(
        fetch_api_1(),
        fetch_api_2(),
        fetch_api_3()
    )
    return {"data": results}

async def fetch_api_1():
    await asyncio.sleep(1)
    return "Data from API 1"

async def fetch_api_2():
    await asyncio.sleep(1)
    return "Data from API 2"

async def fetch_api_3():
    await asyncio.sleep(1)
    return "Data from API 3"
```

## 6️⃣ Async Generators

### Async Generator Function

```python
import asyncio

async def async_range(count):
    """Async generator"""
    for i in range(count):
        await asyncio.sleep(0.1)
        yield i

async def main():
    # Consume async generator
    async for value in async_range(5):
        print(value)

asyncio.run(main())
```

### Async Comprehension

```python
import asyncio

async def fetch_data(id):
    await asyncio.sleep(0.1)
    return id * 2

async def main():
    # Async list comprehension
    results = [await fetch_data(i) for i in range(5)]
    print(results)
    
    # Async generator expression
    results = [x async for x in async_range(5)]
    print(results)

asyncio.run(main())
```

## 7️⃣ Error Handling in Async

### Try-Except in Async

```python
import asyncio

async def risky_operation():
    """Operation that might fail"""
    await asyncio.sleep(1)
    raise ValueError("Something went wrong!")

async def main():
    try:
        await risky_operation()
    except ValueError as e:
        print(f"Error: {e}")
    
    # Handle errors in gather
    results = await asyncio.gather(
        risky_operation(),
        return_exceptions=True  # Return exceptions instead of raising
    )
    
    for result in results:
        if isinstance(result, Exception):
            print(f"Task failed: {result}")
        else:
            print(f"Task succeeded: {result}")

asyncio.run(main())
```

## 8️⃣ Async Queue

### Producer-Consumer Pattern

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, n: int):
    """Produce items"""
    for i in range(n):
        await asyncio.sleep(0.1)
        await queue.put(i)
        print(f"Produced: {i}")
    await queue.put(None)  # Sentinel value

async def consumer(queue: Queue, name: str):
    """Consume items"""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        
        await asyncio.sleep(0.2)
        print(f"{name} consumed: {item}")
        queue.task_done()

async def main():
    queue = Queue()
    
    # Create producer and consumers
    await asyncio.gather(
        producer(queue, 10),
        consumer(queue, "Consumer 1"),
        consumer(queue, "Consumer 2")
    )

asyncio.run(main())
```

## 9️⃣ Complete Example: Async Web Scraper

```python
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List

class AsyncWebScraper:
    """Async web scraper"""
    
    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_page(self, session, url):
        """Fetch single page"""
        async with self.semaphore:
            try:
                async with session.get(url, timeout=10) as response:
                    return await response.text()
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None
    
    async def scrape_urls(self, urls: List[str]):
        """Scrape multiple URLs"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            return results
    
    def parse_html(self, html: str):
        """Parse HTML content"""
        if not html:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        return {
            'title': soup.title.string if soup.title else None,
            'links': [a['href'] for a in soup.find_all('a', href=True)]
        }

# Usage
async def main():
    scraper = AsyncWebScraper(max_concurrent=5)
    
    urls = [
        'https://example.com/page1',
        'https://example.com/page2',
        'https://example.com/page3'
    ]
    
    results = await scraper.scrape_urls(urls)
    
    for url, html in zip(urls, results):
        data = scraper.parse_html(html)
        print(f"{url}: {data}")

asyncio.run(main())
```

## 🎯 Key Takeaways

1. **async/await** - Modern Python async syntax
2. **asyncio.gather()** - Run tasks concurrently
3. **asyncio.create_task()** - Create background tasks
4. **aiohttp** - Async HTTP client
5. **FastAPI** - Async web framework
6. **Async generators** - Yield values asynchronously
7. **Error handling** - Try-except in async context
8. **Semaphores** - Limit concurrent operations

## 🔗 Next Module

[Module 22: Testing & TDD →](../22-testing/)

## 📚 Additional Resources

- [Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [FastAPI Async](https://fastapi.tiangolo.com/async/)
- [Real Python Async Guide](https://realpython.com/async-io-python/)