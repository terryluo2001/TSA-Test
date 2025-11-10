# To-Do List API Documentation

A simple REST API for managing a to-do list with full CRUD operations.

## Base URL
```
http://localhost:5000
```

## Technology Stack
- **Framework**: Flask 3.1.0
- **CORS**: Flask-CORS 5.0.0 (enabled for frontend integration)
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Database**: MySQL (via PyMySQL connector)
- **Storage**: Persistent MySQL database

## Task Data Structure

Each task has the following properties:

```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "status": "pending",
  "created_at": "2025-11-10T20:30:00.123456",
  "updated_at": "2025-11-10T20:30:00.123456"
}
```

### Status Values
- `pending` - Task is not started
- `in_progress` - Task is being worked on
- `completed` - Task is finished

---

## API Endpoints

### 1. Root Endpoint
Get API information and available endpoints.

**Request:**
```http
GET /
```

**Response:**
```json
{
  "message": "To-Do List API",
  "endpoints": {
    "GET /tasks": "Get all tasks",
    "POST /tasks": "Create a new task",
    "PUT /tasks/<id>": "Update a task",
    "DELETE /tasks/<id>": "Delete a task"
  }
}
```

---

### 2. Get All Tasks
Retrieve a list of all tasks.

**Request:**
```http
GET /tasks
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "status": "pending",
      "created_at": "2025-11-10T20:30:00.123456",
      "updated_at": "2025-11-10T20:30:00.123456"
    },
    {
      "id": 2,
      "title": "Finish homework",
      "description": "Math and science assignments",
      "status": "completed",
      "created_at": "2025-11-10T20:31:00.123456",
      "updated_at": "2025-11-10T20:35:00.123456"
    }
  ],
  "count": 2
}
```

---

### 3. Create a New Task
Add a new task to the list.

**Request:**
```http
POST /tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending"
}
```

**Required Fields:**
- `title` (string, non-empty)

**Optional Fields:**
- `description` (string, defaults to empty string)
- `status` (string, must be: `pending`, `in_progress`, or `completed`, defaults to `pending`)

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "created_at": "2025-11-10T20:30:00.123456",
    "updated_at": "2025-11-10T20:30:00.123456"
  },
  "message": "Task created successfully"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "Title is required"
}
```

---

### 4. Update a Task
Update an existing task (e.g., mark as completed, change title/description).

**Request:**
```http
PUT /tasks/1
Content-Type: application/json

{
  "status": "completed"
}
```

**Updatable Fields:**
- `title` (string, non-empty)
- `description` (string)
- `status` (string, must be: `pending`, `in_progress`, or `completed`)

**Note:** You can update one or multiple fields in a single request.

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "completed",
    "created_at": "2025-11-10T20:30:00.123456",
    "updated_at": "2025-11-10T20:35:00.789012"
  },
  "message": "Task updated successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "success": false,
  "error": "Task with id 999 not found"
}
```

**Error Response:** `400 Bad Request`
```json
{
  "success": false,
  "error": "Invalid status. Must be one of: pending, in_progress, completed"
}
```

---

### 5. Delete a Task
Remove a task from the list.

**Request:**
```http
DELETE /tasks/1
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Task 1 deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
  "success": false,
  "error": "Task with id 999 not found"
}
```

---

### 6. Get Task Statistics (Bonus)
Get statistics about tasks for the frontend stats display.

**Request:**
```http
GET /tasks/stats
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "total": 10,
    "pending": 3,
    "in_progress": 2,
    "completed": 5,
    "completion_percentage": 50.0
  }
}
```

---

## Setup Instructions

### 1. Install MySQL
Make sure MySQL Server is installed and running on your system.

### 2. Configure Database
Set environment variables or create a `.env` file:
```bash
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=todolist_db
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python setup_database.py
```
This creates the database and tables automatically.

### 5. Run the Server
```bash
python app.py
```

The server will start at `http://localhost:5000` with debug mode enabled.

See [README.md](README.md) for detailed setup instructions.

---

## Testing with cURL

### Create a task:
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

### Get all tasks:
```bash
curl http://localhost:5000/tasks
```

### Update a task:
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a task:
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

### Get statistics:
```bash
curl http://localhost:5000/tasks/stats
```

---

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:5000"

# Create a task
response = requests.post(f"{BASE_URL}/tasks", json={
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
})
print(response.json())

# Get all tasks
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())

# Update a task
response = requests.put(f"{BASE_URL}/tasks/1", json={
    "status": "completed"
})
print(response.json())

# Delete a task
response = requests.delete(f"{BASE_URL}/tasks/1")
print(response.json())

# Get statistics
response = requests.get(f"{BASE_URL}/tasks/stats")
print(response.json())
```

---

## Error Handling

All error responses follow this format:
```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Task not found

---

## CORS Configuration

CORS is enabled for all origins, allowing the frontend (running on a different port) to make API requests without issues.

---

## Data Persistence

This API uses **MySQL database** for persistent storage:
- Data persists across server restarts
- Transactional integrity with rollback on errors
- Efficient querying with SQLAlchemy ORM
- Production-ready database system

---

## Architecture Decisions

### Why MySQL?
- **Production-Ready**: Battle-tested, reliable database system
- **Persistent Storage**: Data survives server restarts
- **ACID Compliance**: Ensures data integrity
- **Scalability**: Can handle large amounts of data
- **SQL Power**: Complex queries and relationships when needed

### Task ID Generation
- Auto-incrementing integer primary key
- Handled automatically by MySQL
- Sequential and predictable

### Validation Strategy
- Required fields checked first
- Type and format validation
- Clear error messages for users

### Response Format
- Consistent `success` boolean field
- `data` field for successful responses
- `error` field for error responses
- `message` field for additional context

---

## Future Enhancements

Potential improvements for production:
1. Implement user authentication and authorization
2. Add task categories/tags
3. Add due dates and priorities
4. Implement search and filtering
5. Add pagination for large task lists
6. Add task sorting options
7. Implement rate limiting
8. Add comprehensive logging
9. Create unit and integration tests
10. Add database connection pooling
11. Implement caching (Redis)
12. Add API documentation (Swagger/OpenAPI)
