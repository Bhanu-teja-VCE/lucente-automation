import React, { useState, useEffect } from 'react';
import AnalyticsPanel from './components/AnalyticsPanel';
import SearchPanel from './components/SearchPanel';
import FilterBar from './components/FilterBar';
import LeadsTable from './components/LeadsTable';
import ExportButton from './components/ExportButton';

const API_BASE = 'http://localhost:8000';

function App() {
  const [leads, setLeads] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [filters, setFilters] = useState({
    hasEmail: false,
    hasWebsite: false,
    minRating: 0,
    minScore: 0,
    platforms: [],
    search: ''
  });
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const fetchLeads = async () => {
    try {
      const res = await fetch(`${API_BASE}/leads/?page_size=1000`);
      const data = await res.json();
      setLeads(data);
    } catch (e) {
      console.error("Failed to fetch leads", e);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const res = await fetch(`${API_BASE}/analytics/`);
      const data = await res.json();
      setAnalytics(data);
    } catch (e) {
      console.error("Failed to fetch analytics", e);
    }
  };

  useEffect(() => {
    fetchLeads();
    fetchAnalytics();
  }, [refreshTrigger]);

  const handleScrapeComplete = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const filteredLeads = leads.filter(lead => {
    if (filters.hasEmail && !lead.has_email) return false;
    if (filters.hasWebsite && !lead.has_website) return false;
    if (lead.rating < filters.minRating) return false;
    if (lead.lead_score < filters.minScore) return false;
    if (filters.platforms.length > 0 && !filters.platforms.includes(lead.platform)) return false;
    if (filters.search) {
      const q = filters.search.toLowerCase();
      const match = (lead.name?.toLowerCase().includes(q)) || 
                    (lead.email?.toLowerCase().includes(q)) || 
                    (lead.niche?.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo">LUCENTE</div>
        <div className="tagline">Lead Generation Automation</div>
      </header>
      
      <AnalyticsPanel analytics={analytics} />
      
      <div className="main-panel">
        <div className="sidebar">
          <SearchPanel onScrapeComplete={handleScrapeComplete} apiBase={API_BASE} />
          <FilterBar filters={filters} setFilters={setFilters} />
        </div>
        
        <div className="content-area">
          <ExportButton filters={filters} apiBase={API_BASE} />
          <LeadsTable leads={filteredLeads} />
        </div>
      </div>
    </div>
  );
}

export default App;
