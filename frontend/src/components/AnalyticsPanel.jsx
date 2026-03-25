import React from 'react';

export default function AnalyticsPanel({ analytics }) {
  if (!analytics) return <div className="analytics-panel">Loading...</div>;

  const platformColors = {
    google_maps: '#4285F4',
    instagram: '#E1306C',
    upwork: '#14A800',
    fiverr: '#1DBF73'
  };

  const total = analytics.total_leads || 1; // prevent div by zero

  return (
    <div className="analytics-panel">
      <div className="metric-card" style={{ animationDelay: '0ms' }}>
        <div className="metric-label">Total Leads</div>
        <div className="metric-value">{analytics.total_leads}</div>
        <div className="bar-chart">
          {Object.entries(analytics.by_platform).map(([platform, count]) => (
            <div 
              key={platform} 
              className="bar-segment" 
              style={{ 
                width: `${(count / total) * 100}%`, 
                backgroundColor: platformColors[platform] || '#ccc' 
              }}
              title={`${platform}: ${count}`}
            />
          ))}
        </div>
      </div>
      
      <div className="metric-card" style={{ animationDelay: '80ms' }}>
        <div className="metric-label">Leads This Week</div>
        <div className="metric-value">{analytics.leads_this_week}</div>
      </div>
      
      <div className="metric-card" style={{ animationDelay: '160ms' }}>
        <div className="metric-label">Email Discovery Rate</div>
        <div className="metric-value">{(analytics.email_rate * 100).toFixed(0)}%</div>
      </div>
      
      <div className="metric-card" style={{ animationDelay: '240ms' }}>
        <div className="metric-label">Avg Lead Score</div>
        <div className="metric-value">{analytics.avg_lead_score}</div>
      </div>
      
      <div className="metric-card" style={{ animationDelay: '320ms' }}>
        <div className="metric-label">Active Sessions</div>
        <div className="metric-value">{analytics.sessions.length}</div>
      </div>
    </div>
  );
}
