from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO

CORS(app)  # Enable CORS for frontend integration

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Task Model
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default='')
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert Task object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# Create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return jsonify({
        "message": "To-Do List API",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "POST /tasks": "Create a new task",
            "PUT /tasks/<id>": "Update a task",
            "DELETE /tasks/<id>": "Delete a task",
            "GET /tasks/stats": "Get task statistics"
        }
    })


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return jsonify({
            "success": True,
            "data": [task.to_dict() for task in tasks],
            "count": len(tasks)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500


@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    if 'title' not in data or not data['title'].strip():
        return jsonify({
            "success": False,
            "error": "Title is required"
        }), 400

    # Validate status
    valid_statuses = ['pending', 'in_progress', 'completed']
    status = data.get('status', 'pending')
    if status not in valid_statuses:
        return jsonify({
            "success": False,
            "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        }), 400

    try:
        # Create new task
        new_task = Task(
            title=data['title'].strip(),
            description=data.get('description', '').strip(),
            status=status
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": new_task.to_dict(),
            "message": "Task created successfully"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task (e.g., mark as completed)"""
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400

    try:
        # Find the task
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                "success": False,
                "error": f"Task with id {task_id} not found"
            }), 404

        # Update fields
        valid_statuses = ['pending', 'in_progress', 'completed']

        if 'title' in data:
            if not data['title'].strip():
                return jsonify({
                    "success": False,
                    "error": "Title cannot be empty"
                }), 400
            task.title = data['title'].strip()

        if 'description' in data:
            task.description = data['description'].strip()

        if 'status' in data:
            if data['status'] not in valid_statuses:
                return jsonify({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                }), 400
            task.status = data['status']

        task.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "success": True,
            "data": task.to_dict(),
            "message": "Task updated successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        # Find the task
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                "success": False,
                "error": f"Task with id {task_id} not found"
            }), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Task {task_id} deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500


@app.route('/tasks/stats', methods=['GET'])
def get_stats():
    """Get task statistics for the frontend stats display"""
    try:
        total = Task.query.count()

        if total == 0:
            return jsonify({
                "success": True,
                "data": {
                    "total": 0,
                    "pending": 0,
                    "in_progress": 0,
                    "completed": 0,
                    "completion_percentage": 0
                }
            }), 200

        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        completed = Task.query.filter_by(status='completed').count()
        completion_percentage = round((completed / total) * 100, 2)

        return jsonify({
            "success": True,
            "data": {
                "total": total,
                "pending": pending,
                "in_progress": in_progress,
                "completed": completed,
                "completion_percentage": completion_percentage
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
