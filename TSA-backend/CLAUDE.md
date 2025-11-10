# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Flask backend API for the TSA-Test application, a full-stack task management system that provides CRUD operations for tasks. The API uses MySQL database with SQLAlchemy ORM for persistent data storage. This backend works in conjunction with the React + TypeScript + Vite frontend located in the sibling `TSA-frontend` directory.

## Development Commands

### Install Dependencies
```bash
# Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup Database
```bash
python setup_database.py
```
Creates the MySQL database and tables. Configure database credentials via environment variables or `.env` file.

### Running the Development Server
```bash
python app.py
```
Starts the Flask development server with debug mode enabled on port 5000 at `http://localhost:5000`.

### Testing the API
```bash
python test_api.py
```
Runs a comprehensive test suite that demonstrates all API endpoints. Server must be running first.

## Architecture

### Current Structure
The application uses SQLAlchemy ORM with MySQL:
- **app.py**: Main application file with Flask routes and SQLAlchemy models
- **config.py**: Database configuration (reads from environment variables)
- **setup_database.py**: Database initialization script
- **requirements.txt**: Python dependencies
- **test_api.py**: Comprehensive API test script
- **.env.example**: Template for environment variables
- **API_DOCUMENTATION.md**: Complete API documentation
- **README.md**: Setup and usage instructions

### Database
- **System**: MySQL 5.7+ or MariaDB 10.2+
- **ORM**: SQLAlchemy via Flask-SQLAlchemy
- **Connector**: PyMySQL
- **Database Name**: `todolist_db` (configurable)
- **Table**: `tasks`

### Task Model (app.py:20-39)
SQLAlchemy model with columns:
- `id` - Integer, primary key, auto-increment
- `title` - String(255), required
- `description` - Text, optional
- `status` - String(50), default 'pending'
- `created_at` - DateTime, auto-set on creation
- `updated_at` - DateTime, auto-updated on modification

The `to_dict()` method converts model instances to JSON-serializable dictionaries.

### Configuration
Database settings are loaded from `config.py` which reads:
1. Environment variables (highest priority)
2. Default values

Key variables:
- `DB_HOST` - MySQL host (default: localhost)
- `DB_PORT` - MySQL port (default: 3306)
- `DB_USER` - MySQL username (default: root)
- `DB_PASSWORD` - MySQL password (default: empty)
- `DB_NAME` - Database name (default: todolist_db)
- `SQLALCHEMY_ECHO` - Log SQL queries for debugging

## API Endpoints

All endpoints return JSON responses with consistent format:
- Success: `{"success": true, "data": {...}, "message": "..."}`
- Error: `{"success": false, "error": "error message"}`

### Implemented Routes

1. **GET /** - API information and endpoint list
2. **GET /tasks** - Get all tasks (ordered by created_at DESC)
3. **POST /tasks** - Create new task (requires `title`)
4. **PUT /tasks/<id>** - Update task fields (partial updates supported)
5. **DELETE /tasks/<id>** - Delete task by ID
6. **GET /tasks/stats** - Get task statistics (total, by status, completion %)

All endpoints include try-catch blocks with database rollback on errors.

## Key Features

### Database Persistence
- All data persists across server restarts
- Transactions with automatic rollback on errors
- SQLAlchemy handles SQL generation and ORM mapping

### CORS Configuration
Flask-CORS is enabled for all origins (app.py:13) to allow frontend integration.

### Input Validation
- Required fields checked (title for new tasks)
- Status must be one of: `pending`, `in_progress`, `completed`
- Empty strings are rejected
- Clear error messages returned

### Error Handling
- 400 Bad Request: Invalid input data
- 404 Not Found: Task doesn't exist
- 500 Internal Server Error: Database errors
- 200 OK: Successful GET, PUT, DELETE
- 201 Created: Successful POST

### Auto-initialization
The application automatically creates tables on startup (app.py:43-44) using SQLAlchemy's `create_all()`.

## Integration with Frontend

The frontend (`../TSA-frontend`) expects:
- API running on `http://localhost:5000`
- JSON responses with `success` boolean
- Task objects with id, title, description, status, timestamps
- Stats endpoint for dashboard (total, pending, in_progress, completed counts, completion %)

## Database Setup

### Prerequisites
- MySQL Server 5.7+ or MariaDB 10.2+
- Python 3.7+

### Quick Setup
1. Install MySQL and start the service
2. Set environment variables or create `.env` file:
   ```bash
   export DB_USER=root
   export DB_PASSWORD=your_password
   export DB_NAME=todolist_db
   ```
3. Run setup script: `python setup_database.py`

The setup script:
- Creates the database if it doesn't exist
- Creates the `tasks` table
- Verifies the setup

### Manual Database Creation
If needed, create manually:
```sql
CREATE DATABASE todolist_db;
USE todolist_db;
-- Tables will be created automatically by SQLAlchemy
```

## Testing

### Automated Testing
```bash
python test_api.py
```
Tests all CRUD operations, validation, error handling, and statistics.

### Manual Testing with cURL
```bash
# Create task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing"}'

# Get all tasks
curl http://localhost:5000/tasks

# Update task
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete task
curl -X DELETE http://localhost:5000/tasks/1

# Get stats
curl http://localhost:5000/tasks/stats
```

## Code Organization

### Database Operations
- **Query**: `Task.query.filter_by().all()` or `Task.query.get(id)`
- **Create**: Instantiate `Task()`, `db.session.add()`, `db.session.commit()`
- **Update**: Modify object properties, `db.session.commit()`
- **Delete**: `db.session.delete()`, `db.session.commit()`
- **Error handling**: `db.session.rollback()` on exceptions

### Response Patterns
Consistent JSON structure across all endpoints:
```python
# Success
{"success": True, "data": {...}, "message": "..."}

# Error
{"success": False, "error": "error message"}
```

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in environment variables or `.env`
- Test connection: `mysql -u root -p`
- Verify database exists: `SHOW DATABASES;`

### Table Not Found
- Run `python setup_database.py`
- Or restart app (auto-creates tables)

### Port 5000 In Use
- Change port in app.py:257

## Future Enhancements

The current implementation is production-ready for basic use but could be enhanced with:
- User authentication and authorization
- Database connection pooling
- Pagination for large datasets
- Task filtering and search
- Comprehensive unit tests (pytest)
- Migration system (Alembic)
- API rate limiting
- Logging and monitoring
- Docker containerization

## Development Notes

- Debug mode is enabled in app.py:257 (`app.run(debug=True)`)
- Port 5000 is hardcoded in app.py:257
- Database connection is initialized at app startup (app.py:16)
- Tables are auto-created if they don't exist (app.py:43-44)
- UTC timestamps are used for consistency (app.py:27-28)
- CORS is permissive (all origins) - restrict in production (app.py:13)
- Git repository is at the parent level (`../`)
- SQLAlchemy uses PyMySQL connector via `mysql+pymysql://` URI
