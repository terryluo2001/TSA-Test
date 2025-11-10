import type { TaskStats } from '../services/api';

interface StatsDisplayProps {
  stats: TaskStats | null;
  loading: boolean;
}

export default function StatsDisplay({ stats, loading }: StatsDisplayProps) {
  if (loading) {
    return (
      <div className="stats-display">
        <h2>Task Statistics</h2>
        <p>Loading stats...</p>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="stats-display">
        <h2>Task Statistics</h2>
        <p>Unable to load statistics</p>
      </div>
    );
  }

  return (
    <div className="stats-display">
      <h2>Task Statistics</h2>
      
      <div className="stats-grid">
        <div className="stat-card total">
          <div className="stat-number">{stats.total}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        
        <div className="stat-card pending">
          <div className="stat-number">{stats.pending}</div>
          <div className="stat-label">Pending</div>
        </div>
        
        <div className="stat-card in-progress">
          <div className="stat-number">{stats.in_progress}</div>
          <div className="stat-label">In Progress</div>
        </div>
        
        <div className="stat-card completed">
          <div className="stat-number">{stats.completed}</div>
          <div className="stat-label">Completed</div>
        </div>
      </div>

      <div className="completion-section">
        <div className="completion-percentage">
          <span className="percentage-number">{stats.completion_percentage}%</span>
          <span className="percentage-label">Complete</span>
        </div>
        
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${stats.completion_percentage}%` }}
          />
        </div>
      </div>

      {stats.total > 0 && (
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