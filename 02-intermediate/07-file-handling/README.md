# Module 07: File Handling & I/O

## 🎯 Learning Objectives
- Read and write files in Python
- Work with different file formats (text, CSV, JSON, XML)
- Handle file paths and directories
- Implement context managers
- Work with binary files
- Handle file exceptions properly

## 📖 File I/O Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FILE OPERATIONS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐                                               │
│  │  Python  │                                               │
│  │  Program │                                               │
│  └────┬─────┘                                               │
│       │                                                      │
│       ├─────────► open() ──────► File Object                │
│       │                              │                       │
│       │                              ├─► read()             │
│       │                              ├─► write()            │
│       │                              ├─► readline()         │
│       │                              └─► close()            │
│       │                                                      │
│       └─────────► with statement ──► Auto-close             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1️⃣ Basic File Operations

### Opening and Closing Files

```python
# Java:
"""
FileReader reader = new FileReader("file.txt");
BufferedReader br = new BufferedReader(reader);
try {
    String line = br.readLine();
} finally {
    br.close();
}
"""

# Python - Manual close (not recommended)
file = open("file.txt", "r")
content = file.read()
file.close()

# Python - With statement (recommended)
with open("file.txt", "r") as file:
    content = file.read()
# File automatically closed after with block
```

### File Modes

| Mode | Description | Creates if not exists |
|------|-------------|----------------------|
| `'r'` | Read (default) | No (raises error) |
| `'w'` | Write (overwrites) | Yes |
| `'a'` | Append | Yes |
| `'x'` | Exclusive create | Yes (fails if exists) |
| `'r+'` | Read and write | No |
| `'w+'` | Write and read | Yes |
| `'a+'` | Append and read | Yes |
| `'rb'` | Read binary | No |
| `'wb'` | Write binary | Yes |

## 2️⃣ Reading Files

### Read Entire File

```python
# Method 1: read() - entire file as string
with open("data.txt", "r") as file:
    content = file.read()
    print(content)

# Method 2: readlines() - list of lines
with open("data.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())  # Remove newline

# Method 3: readline() - one line at a time
with open("data.txt", "r") as file:
    line = file.readline()
    while line:
        print(line.strip())
        line = file.readline()

# Method 4: Iterate (most Pythonic)
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())
```

### Read with Encoding

```python
# Specify encoding (important for non-ASCII)
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

## 3️⃣ Writing Files

### Write Text

```python
# Write (overwrites existing content)
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("Second line\n")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)

# Append (adds to existing content)
with open("output.txt", "a") as file:
    file.write("Appended line\n")
```

### Write with Print

```python
# Redirect print to file
with open("output.txt", "w") as file:
    print("Hello, World!", file=file)
    print("Second line", file=file)
```

## 4️⃣ Working with CSV Files

### Reading CSV

```python
import csv

# Method 1: csv.reader
with open("data.csv", "r") as file:
    csv_reader = csv.reader(file)
    
    # Skip header
    next(csv_reader)
    
    for row in csv_reader:
        print(f"Name: {row[0]}, Age: {row[1]}, City: {row[2]}")

# Method 2: csv.DictReader (better for named columns)
with open("data.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        print(f"Name: {row['name']}, Age: {row['age']}, City: {row['city']}")
```

### Writing CSV

```python
import csv

# Method 1: csv.writer
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "NYC"],
    ["Bob", 25, "LA"],
    ["Charlie", 35, "Chicago"]
]

with open("output.csv", "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

# Method 2: csv.DictWriter
data = [
    {"name": "Alice", "age": 30, "city": "NYC"},
    {"name": "Bob", "age": 25, "city": "LA"}
]

with open("output.csv", "w", newline="") as file:
    fieldnames = ["name", "age", "city"]
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    csv_writer.writeheader()
    csv_writer.writerows(data)
```

## 5️⃣ Working with JSON Files

### Reading JSON

```python
import json

# Read JSON file
with open("data.json", "r") as file:
    data = json.load(file)
    print(data)

# Parse JSON string
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)
print(data["name"])
```

### Writing JSON

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "city": "NYC",
    "hobbies": ["reading", "coding", "gaming"]
}

# Write to file
with open("output.json", "w") as file:
    json.dump(data, file, indent=4)

# Convert to string
json_string = json.dumps(data, indent=2)
print(json_string)
```

### Pretty Print JSON

```python
import json

data = {"name": "Alice", "age": 30, "city": "NYC"}

# Pretty print
print(json.dumps(data, indent=4, sort_keys=True))
```

## 6️⃣ File Paths and Directories

### Using pathlib (Modern Way)

```python
from pathlib import Path

# Current directory
current_dir = Path.cwd()
print(f"Current directory: {current_dir}")

# Home directory
home_dir = Path.home()
print(f"Home directory: {home_dir}")

# Create path
file_path = Path("data") / "files" / "example.txt"
print(file_path)

# Check if exists
if file_path.exists():
    print("File exists")

# Check if file or directory
if file_path.is_file():
    print("It's a file")
elif file_path.is_dir():
    print("It's a directory")

# Get file info
if file_path.exists():
    print(f"Name: {file_path.name}")
    print(f"Stem: {file_path.stem}")
    print(f"Suffix: {file_path.suffix}")
    print(f"Parent: {file_path.parent}")
```

### Directory Operations

```python
from pathlib import Path
import os

# Create directory
Path("new_folder").mkdir(exist_ok=True)

# Create nested directories
Path("parent/child/grandchild").mkdir(parents=True, exist_ok=True)

# List files in directory
for file in Path(".").iterdir():
    print(file)

# List specific files
for file in Path(".").glob("*.txt"):
    print(file)

# Recursive search
for file in Path(".").rglob("*.py"):
    print(file)

# Remove directory
Path("new_folder").rmdir()  # Only if empty

# Remove file
Path("file.txt").unlink(missing_ok=True)
```

### Using os module (Legacy)

```python
import os

# Current directory
print(os.getcwd())

# Change directory
os.chdir("/path/to/directory")

# List files
files = os.listdir(".")
print(files)

# Join paths
path = os.path.join("folder", "subfolder", "file.txt")

# Check if exists
if os.path.exists(path):
    print("Exists")

# Create directory
os.makedirs("parent/child", exist_ok=True)
```

## 7️⃣ Error Handling

### File Exceptions

```python
# Handle file not found
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Permission denied!")
except Exception as e:
    print(f"Error: {e}")

# Check before opening
from pathlib import Path

file_path = Path("data.txt")
if file_path.exists():
    with open(file_path, "r") as file:
        content = file.read()
else:
    print("File doesn't exist")
```

## 8️⃣ Context Managers

### Custom Context Manager

```python
class FileManager:
    """Custom context manager for file operations"""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Called when entering with block"""
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting with block"""
        if self.file:
            self.file.close()
        # Return False to propagate exceptions
        return False

# Usage
with FileManager("data.txt", "w") as file:
    file.write("Hello, World!")
```

### Using contextlib

```python
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    """Context manager using decorator"""
    file = open(filename, mode)
    try:
        yield file
    finally:
        file.close()

# Usage
with file_manager("data.txt", "w") as file:
    file.write("Hello, World!")
```

## 9️⃣ Binary Files

### Reading Binary

```python
# Read binary file
with open("image.jpg", "rb") as file:
    binary_data = file.read()
    print(f"File size: {len(binary_data)} bytes")

# Read in chunks
with open("large_file.bin", "rb") as file:
    chunk_size = 1024  # 1KB
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        # Process chunk
        print(f"Read {len(chunk)} bytes")
```

### Writing Binary

```python
# Write binary data
data = b"Binary data here"
with open("output.bin", "wb") as file:
    file.write(data)

# Copy binary file
with open("source.jpg", "rb") as source:
    with open("destination.jpg", "wb") as dest:
        dest.write(source.read())
```

## 🔟 Practical Examples

### Example 1: Log File Analyzer

```python
def analyze_log_file(filename):
    """Analyze log file and count error levels"""
    error_counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    
    try:
        with open(filename, "r") as file:
            for line in file:
                for level in error_counts:
                    if level in line:
                        error_counts[level] += 1
        
        return error_counts
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None

# Usage
counts = analyze_log_file("app.log")
if counts:
    for level, count in counts.items():
        print(f"{level}: {count}")
```

### Example 2: CSV to JSON Converter

```python
import csv
import json

def csv_to_json(csv_file, json_file):
    """Convert CSV file to JSON"""
    data = []
    
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Converted {len(data)} records")

# Usage
csv_to_json("data.csv", "data.json")
```

### Example 3: File Backup

```python
from pathlib import Path
from datetime import datetime
import shutil

def backup_file(source_file):
    """Create timestamped backup of file"""
    source = Path(source_file)
    
    if not source.exists():
        print(f"File {source_file} not found")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source.stem}_backup_{timestamp}{source.suffix}"
    backup_path = source.parent / backup_name
    
    shutil.copy2(source, backup_path)
    print(f"Backup created: {backup_path}")

# Usage
backup_file("important_data.txt")
```

## 💻 Complete Example

See `file_handling_demo.py` for comprehensive demonstrations.

## 🎯 Key Takeaways

1. **Use with statement** - Automatic resource cleanup
2. **pathlib over os.path** - Modern, object-oriented
3. **Specify encoding** - Especially for UTF-8
4. **Handle exceptions** - FileNotFoundError, PermissionError
5. **CSV/JSON modules** - Built-in support
6. **Context managers** - For custom resource management
7. **Binary mode** - For non-text files
8. **Check before operations** - exists(), is_file(), is_dir()

## 🔗 Next Module

[Module 08: Error Handling →](../08-error-handling/)

## 📚 Additional Resources

- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html)
- [pathlib Documentation](https://docs.python.org/3/library/pathlib.html)
- [CSV Module](https://docs.python.org/3/library/csv.html)
- [JSON Module](https://docs.python.org/3/library/json.html)