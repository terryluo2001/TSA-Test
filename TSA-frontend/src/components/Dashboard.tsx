import type { TaskStats } from '../services/api';

interface DashboardProps {
  stats: TaskStats | null;
  loading: boolean;
}

export default function Dashboard({ stats }: DashboardProps) {

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Task Statistics</h1>
      </div>

      <div className="stats-grid">
        <div className="stat-card total">
          <div className="stat-number">{stats?.total || 0}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        
        <div className="stat-card pending">
          <div className="stat-number">{stats?.pending || 0}</div>
          <div className="stat-label">Pending</div>
        </div>
        
        <div className="stat-card in-progress">
          <div className="stat-number">{stats?.in_progress || 0}</div>
          <div className="stat-label">In Progress</div>
        </div>
        
        <div className="stat-card completed">
          <div className="stat-number">{stats?.completed || 0}</div>
          <div className="stat-label">Completed</div>
        </div>
      </div>

      <div className="completion-section">
        <div className="completion-percentage">
          <span className="percentage-number">{stats?.completion_percentage || 0}%</span>
          <span className="percentage-label">Complete</span>
        </div>
        
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${stats?.completion_percentage || 0}%` }}
          />
        </div>
      </div>

      {stats && stats.total > 0 && (
        <div className="stats-summary">
          <p>
            You have {stats.pending + stats.in_progress} tasks remaining 
            out of {stats.total} total tasks.
          </p>
        </div>
      )}
    </div>
  );
}