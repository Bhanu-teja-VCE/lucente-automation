import React from 'react';

export default function FilterBar({ filters, setFilters }) {
  const togglePlatform = (p) => {
    setFilters(prev => {
      const platforms = prev.platforms.includes(p) 
        ? prev.platforms.filter(x => x !== p)
        : [...prev.platforms, p];
      return { ...prev, platforms };
    });
  };

  const clearFilters = () => {
    setFilters({
      hasEmail: false,
      hasWebsite: false,
      minRating: 0,
      minScore: 0,
      platforms: [],
      search: ''
    });
  };

  return (
    <div className="glass-card">
      <h3>Filters</h3>
      
      <div className="form-group">
        <input 
          type="text" 
          placeholder="Search name, email, niche..." 
          value={filters.search}
          onChange={e => setFilters({...filters, search: e.target.value})}
        />
      </div>
      
      <div className="filter-chips">
        <div 
          className={`chip ${filters.hasEmail ? 'active' : ''}`}
          onClick={() => setFilters({...filters, hasEmail: !filters.hasEmail})}
        >
          Has Email
        </div>
        <div 
          className={`chip ${filters.hasWebsite ? 'active' : ''}`}
          onClick={() => setFilters({...filters, hasWebsite: !filters.hasWebsite})}
        >
          Has Website
        </div>
      </div>
      
      <div className="form-group">
        <label>Min Rating: {filters.minRating}</label>
        <input 
          type="range" 
          min="0" max="5" step="0.5" 
          value={filters.minRating}
          onChange={e => setFilters({...filters, minRating: parseFloat(e.target.value)})}
        />
      </div>
      
      <div className="form-group">
        <label>Min Score: {filters.minScore}</label>
        <input 
          type="range" 
          min="0" max="100" step="5" 
          value={filters.minScore}
          onChange={e => setFilters({...filters, minScore: parseInt(e.target.value)})}
        />
      </div>
      
      <div className="form-group">
        <label>Platforms</label>
        <div className="filter-chips">
          {['google_maps', 'instagram', 'upwork', 'fiverr'].map(p => (
            <div 
              key={p}
              className={`chip ${filters.platforms.includes(p) ? 'active' : ''}`}
              onClick={() => togglePlatform(p)}
            >
              {p.replace('_', ' ')}
            </div>
          ))}
        </div>
      </div>
      
      <div className="clear-filters" onClick={clearFilters}>
        Clear all filters
      </div>
    </div>
  );
}
