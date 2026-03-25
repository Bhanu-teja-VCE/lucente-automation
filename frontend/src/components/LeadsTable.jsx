import React, { useState, useMemo } from 'react';
import { FixedSizeList as List } from 'react-window';

export default function LeadsTable({ leads }) {
  const [sortConfig, setSortConfig] = useState({ key: 'lead_score', direction: 'desc' });

  const sortedLeads = useMemo(() => {
    let sortableLeads = [...leads];
    if (sortConfig !== null) {
      sortableLeads.sort((a, b) => {
        const aVal = a[sortConfig.key] || '';
        const bVal = b[sortConfig.key] || '';
        if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }
    return sortableLeads;
  }, [leads, sortConfig]);

  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig && sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getScoreClass = (score) => {
    if (score >= 70) return 'score-high';
    if (score >= 40) return 'score-mid';
    return 'score-low';
  };

  const formatRelativeTime = (dateString) => {
    if (!dateString) return '—';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
  };

  if (leads.length === 0) {
    return (
      <div className="table-container">
        <div className="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '16px', opacity: 0.5 }}>
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <p>No leads yet — run a scrape to get started</p>
        </div>
      </div>
    );
  }

  const Row = ({ index, style }) => {
    const lead = sortedLeads[index];
    return (
      <div style={{ ...style, display: 'flex', borderBottom: '1px solid var(--border-subtle)', alignItems: 'center', padding: '0 16px', fontSize: '14px' }} className="table-row">
        <div style={{ width: '80px' }}>
          <span className={`score-badge ${getScoreClass(lead.lead_score)}`}>{lead.lead_score}</span>
        </div>
        <div style={{ width: '200px', fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={lead.name}>{lead.name || '—'}</div>
        <div style={{ width: '120px', textTransform: 'capitalize' }}>{lead.platform.replace('_', ' ')}</div>
        <div style={{ width: '100px' }}>
          <span className="pipeline-badge">{lead.pipeline}</span>
        </div>
        <div style={{ width: '150px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={lead.location}>{lead.location || '—'}</div>
        <div style={{ width: '200px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={lead.email}>
          {lead.email ? <a href={`mailto:${lead.email}`}>{lead.email}</a> : '—'}
        </div>
        <div style={{ width: '150px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} title={lead.website}>
          {lead.website ? <a href={lead.website} target="_blank" rel="noreferrer">{lead.website.replace(/^https?:\/\//, '')}</a> : '—'}
        </div>
        <div style={{ width: '80px' }}>{lead.rating ? `★ ${lead.rating}` : '—'}</div>
        <div style={{ width: '100px' }}>{lead.review_count ? lead.review_count.toLocaleString() : '—'}</div>
        <div style={{ width: '120px', color: 'var(--text-secondary)', fontSize: '12px' }}>{formatRelativeTime(lead.date_scraped)}</div>
      </div>
    );
  };

  return (
    <div className="table-container" style={{ display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', padding: '12px 16px', borderBottom: '1px solid var(--border-subtle)', background: 'var(--bg-secondary)', fontSize: '12px', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
        <div style={{ width: '80px', cursor: 'pointer' }} onClick={() => requestSort('lead_score')}>Score {sortConfig.key === 'lead_score' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '200px', cursor: 'pointer' }} onClick={() => requestSort('name')}>Name {sortConfig.key === 'name' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '120px', cursor: 'pointer' }} onClick={() => requestSort('platform')}>Platform {sortConfig.key === 'platform' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '100px', cursor: 'pointer' }} onClick={() => requestSort('pipeline')}>Pipeline {sortConfig.key === 'pipeline' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '150px', cursor: 'pointer' }} onClick={() => requestSort('location')}>Location {sortConfig.key === 'location' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '200px', cursor: 'pointer' }} onClick={() => requestSort('email')}>Email {sortConfig.key === 'email' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '150px', cursor: 'pointer' }} onClick={() => requestSort('website')}>Website {sortConfig.key === 'website' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '80px', cursor: 'pointer' }} onClick={() => requestSort('rating')}>Rating {sortConfig.key === 'rating' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '100px', cursor: 'pointer' }} onClick={() => requestSort('review_count')}>Reviews {sortConfig.key === 'review_count' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
        <div style={{ width: '120px', cursor: 'pointer' }} onClick={() => requestSort('date_scraped')}>Date {sortConfig.key === 'date_scraped' ? (sortConfig.direction === 'asc' ? '↑' : '↓') : ''}</div>
      </div>
      <div style={{ flex: 1 }}>
        <List
          height={600} // This should ideally be dynamic based on container, but fixed for simplicity
          itemCount={sortedLeads.length}
          itemSize={48}
          width="100%"
          style={{ overflowX: 'hidden' }}
        >
          {Row}
        </List>
      </div>
    </div>
  );
}
