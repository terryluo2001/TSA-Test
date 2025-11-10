# TSA-Test Backend API

A REST API for managing a to-do list, built with Flask and MySQL database.

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+ or MariaDB 10.2+
- pip (Python package manager)

## Quick Start

### 1. Install MySQL (if not already installed)

**macOS:**
```bash
brew install mysql
brew services start mysql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

**Windows:**
Download and install from [MySQL Downloads](https://dev.mysql.com/downloads/mysql/)

### 2. Set Up Database Configuration

Create a `.env` file from the example (optional, uses defaults otherwise):
```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=todolist_db
```

Or set environment variables directly:
```bash
export DB_USER=root
export DB_PASSWORD=your_password
```

### 3. Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Create Database and Tables

Run the setup script:
```bash
python setup_database.py
```

This will:
- Create the `todolist_db` database
- Create the `tasks` table
- Verify the setup

### 5. Run the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 6. Test the API

In a new terminal (with the server still running):
```bash
python test_api.py
```

## Alternative Setup (Without Virtual Environment)

```bash
pip3 install --user -r requirements.txt
python3 setup_database.py
python3 app.py
```

## Database Schema

The application uses a single `tasks` table:

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
);
```

## API Endpoints

- `GET /` - API information
- `GET /tasks` - Get all tasks
- `POST /tasks` - Create a new task
- `PUT /tasks/<id>` - Update a task
- `DELETE /tasks/<id>` - Delete a task
- `GET /tasks/stats` - Get task statistics

## Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API documentation with examples.

## Project Structure

```
TSA-backend/
├── app.py                  # Main Flask application with SQLAlchemy
├── config.py               # Database configuration
├── setup_database.py       # Database setup script
├── requirements.txt        # Python dependencies
├── test_api.py            # API test suite
├── .env.example           # Environment variable template
├── API_DOCUMENTATION.md   # Complete API documentation
├── CLAUDE.md              # Developer guide
└── README.md              # This file
```

## Features

- Full CRUD operations for tasks
- MySQL database with SQLAlchemy ORM
- RESTful API design
- CORS enabled for frontend integration
- Input validation and error handling
- Task statistics endpoint
- Automatic table creation
- Transaction rollback on errors

## Task Structure

```json
{
  "id": 1,
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "created_at": "2025-11-10T20:30:00",
  "updated_at": "2025-11-10T20:30:00"
}
```

Valid status values: `pending`, `in_progress`, `completed`

## Configuration

Database configuration can be set via:
1. Environment variables (highest priority)
2. `.env` file
3. Default values in `config.py`

Configuration variables:
- `DB_HOST` - MySQL host (default: localhost)
- `DB_PORT` - MySQL port (default: 3306)
- `DB_USER` - MySQL user (default: root)
- `DB_PASSWORD` - MySQL password (default: empty)
- `DB_NAME` - Database name (default: todolist_db)
- `SQLALCHEMY_ECHO` - Log SQL queries (default: false)

## Testing with cURL

```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'

# Get all tasks
curl http://localhost:5000/tasks

# Update a task (mark as completed)
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/1

# Get statistics
curl http://localhost:5000/tasks/stats
```

## Troubleshooting

### Can't connect to MySQL
- Check if MySQL is running: `mysql.server status` (macOS) or `systemctl status mysql` (Linux)
- Verify credentials in `.env` or environment variables
- Test connection: `mysql -u root -p`

### Database doesn't exist
- Run `python setup_database.py` to create the database

### Permission denied
- Make sure the MySQL user has proper permissions:
```sql
GRANT ALL PRIVILEGES ON todolist_db.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### Port 5000 already in use
- Change the port in `app.py` line 257: `app.run(debug=True, port=5001)`

## Development

The application runs in debug mode by default, which provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

For production deployment:
1. Disable debug mode in `app.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Restrict CORS to your frontend domain
4. Use environment variables for sensitive data
5. Set up proper database backups

## Dependencies

- Flask 3.1.0 - Web framework
- Flask-CORS 5.0.0 - Cross-Origin Resource Sharing support
- Flask-SQLAlchemy 3.1.1 - ORM for database operations
- PyMySQL 1.1.1 - MySQL database connector
- cryptography 44.0.0 - Required by PyMySQL

## License

This project is part of the TSA-Test application.
