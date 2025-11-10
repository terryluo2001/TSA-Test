import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import TaskList from './components/TaskList';
import type { Task, TaskStats } from './services/api';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<TaskStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [tasksResponse, statsResponse] = await Promise.all([
        apiService.getTasks(),
        apiService.getStats(),
      ]);

      if (tasksResponse.success && tasksResponse.data) {
        setTasks(tasksResponse.data);
      } else {
        setError(`Failed to fetch tasks: ${tasksResponse.error}`);
      }

      if (statsResponse.success && statsResponse.data) {
        setStats(statsResponse.data);
      } else {
        setError(`Failed to fetch stats: ${statsResponse.error}`);
      }
    } catch {
      setError('Network error: Unable to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTasksChange = () => {
    fetchData();
  };

  const renderMainContent = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard stats={stats} loading={loading} />;
      case 'tasks':
        return (
          <div className="tasks-page">
            <TaskList tasks={tasks} onTasksChange={handleTasksChange} />
          </div>
        );
      default:
        return (
          <div className="placeholder-page">
            <h1>{currentView.charAt(0).toUpperCase() + currentView.slice(1)}</h1>
            <p>This section is coming soon...</p>
          </div>
        );
    }
  };

  return (
    <div className="app">
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />
      
      <main className="main-content">
        {error && (
          <div className="error-banner">
            <p>⚠️ {error}</p>
            <button onClick={fetchData} className="btn-secondary">
              Retry
            </button>
          </div>
        )}
        
        {renderMainContent()}
      </main>
    </div>
  );
}

export default App;
