import { useState } from 'react';
import type { Task } from '../services/api';
import { apiService } from '../services/api';

interface TaskListProps {
  tasks: Task[];
  onTasksChange: () => void;
}

export default function TaskList({ tasks, onTasksChange }: TaskListProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [statusFilter, setStatusFilter] = useState<'all' | Task['status']>('all');

  const handleStatusChange = async (taskId: number, newStatus: Task['status']) => {
    const response = await apiService.updateTask(taskId, { status: newStatus });
    if (response.success) {
      onTasksChange();
    } else {
      alert(`Error updating task: ${response.error}`);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (confirm('Are you sure you want to delete this task?')) {
      const response = await apiService.deleteTask(taskId);
      if (response.success) {
        onTasksChange();
      } else {
        alert(`Error deleting task: ${response.error}`);
      }
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;

    const response = await apiService.createTask({
      title: newTask.title.trim(),
      description: newTask.description.trim(),
    });

    if (response.success) {
      setNewTask({ title: '', description: '' });
      setIsCreating(false);
      onTasksChange();
    } else {
      alert(`Error creating task: ${response.error}`);
    }
  };

  const getStatusBadgeClass = (status: Task['status']) => {
    switch (status) {
      case 'pending': return 'status-pending';
      case 'in_progress': return 'status-in-progress';
      case 'completed': return 'status-completed';
      default: return '';
    }
  };

  const filteredTasks = statusFilter === 'all' 
    ? tasks 
    : tasks.filter(task => task.status === statusFilter);

  return (
    <div className="task-list-page">
      <div className="page-header">
        <h1>Task Management</h1>
        <button 
          className="btn-primary"
          onClick={() => setIsCreating(!isCreating)}
        >
          {isCreating ? 'Cancel' : '+ Add Task'}
        </button>
      </div>

      <div className="filter-section">
        <label htmlFor="status-filter" className="filter-label">Filter by status:</label>
        <select 
          id="status-filter"
          value={statusFilter} 
          onChange={(e) => setStatusFilter(e.target.value as 'all' | Task['status'])}
          className="status-filter"
        >
          <option value="all">All Tasks</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <div className="task-list">

      {isCreating && (
        <form onSubmit={handleCreateTask} className="task-form">
          <input
            type="text"
            placeholder="Task title"
            value={newTask.title}
            onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
            required
          />
          <textarea
            placeholder="Task description (optional)"
            value={newTask.description}
            onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
          />
          <div className="form-actions">
            <button type="submit" className="btn-primary">Create Task</button>
            <button type="button" className="btn-secondary" onClick={() => setIsCreating(false)}>
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="tasks">
        {filteredTasks.length === 0 ? (
          <p className="no-tasks">
            {tasks.length === 0 
              ? "No tasks found. Create your first task!" 
              : `No ${statusFilter === 'all' ? '' : statusFilter.replace('_', ' ')} tasks found.`}
          </p>
        ) : (
          filteredTasks.map((task) => (
            <div key={task.id} className="task-item">
              <div className="task-info">
                <div className="task-header">
                  <span className="task-id">#{task.id}</span>
                  <span className={`status-badge ${getStatusBadgeClass(task.status)}`}>
                    {task.status.replace('_', ' ')}
                  </span>
                </div>
                <h3 className="task-title">{task.title}</h3>
                {task.description && <p className="task-description">{task.description}</p>}
                <div className="task-dates">
                  <small>Created: {new Date(task.created_at).toLocaleDateString()}</small>
                  <small>Updated: {new Date(task.updated_at).toLocaleDateString()}</small>
                </div>
              </div>
              <div className="task-actions">
                <select
                  value={task.status}
                  onChange={(e) => handleStatusChange(task.id, e.target.value as Task['status'])}
                  className="status-select"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="btn-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
    </div>
  );
}