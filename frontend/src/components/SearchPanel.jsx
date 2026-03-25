import React, { useState, useEffect } from 'react';

export default function SearchPanel({ onScrapeComplete, apiBase }) {
  const [platform, setPlatform] = useState('google_maps');
  const [pipeline, setPipeline] = useState('client');
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState('');
  const [maxResults, setMaxResults] = useState(20);
  
  const [isScraping, setIsScraping] = useState(false);
  const [statusText, setStatusText] = useState('');
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    if (platform === 'google_maps') setPipeline('client');
    else setPipeline('talent');
  }, [platform]);

  useEffect(() => {
    let interval;
    if (isScraping && sessionId) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`${apiBase}/scrape/status/${sessionId}`);
          const data = await res.json();
          
          if (data.status === 'complete') {
            setIsScraping(false);
            setStatusText(`Complete! ${data.count} found.`);
            clearInterval(interval);
            onScrapeComplete();
            setTimeout(() => setStatusText(''), 3000);
          } else if (data.status === 'error') {
            setIsScraping(false);
            setStatusText('Error occurred.');
            clearInterval(interval);
            setTimeout(() => setStatusText(''), 3000);
          } else {
            setStatusText(`Scraping... ${data.count || 0} found`);
          }
        } catch (e) {
          console.error(e);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isScraping, sessionId, apiBase, onScrapeComplete]);

  const handleScrape = async () => {
    if (!query) return;
    setIsScraping(true);
    setStatusText('Starting...');
    
    try {
      const res = await fetch(`${apiBase}/scrape/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          platform,
          pipeline,
          query,
          location,
          max_results: parseInt(maxResults)
        })
      });
      const data = await res.json();
      setSessionId(data.session_id);
    } catch (e) {
      console.error(e);
      setIsScraping(false);
      setStatusText('Failed to start');
    }
  };

  const needsLocation = platform === 'google_maps';

  return (
    <div className="glass-card">
      <h3>New Scrape</h3>
      
      <div className="form-group">
        <label>Platform</label>
        <select value={platform} onChange={e => setPlatform(e.target.value)}>
          <option value="google_maps">Google Maps</option>
          <option value="instagram">Instagram</option>
          <option value="upwork">Upwork</option>
          <option value="fiverr">Fiverr</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Pipeline</label>
        <select value={pipeline} onChange={e => setPipeline(e.target.value)}>
          <option value="client">Client Acquisition</option>
          <option value="talent">Talent Recruitment</option>
        </select>
      </div>
      
      <div className="form-group">
        <label>Search Query</label>
        <input 
          type="text" 
          placeholder="e.g. video production agency" 
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
      </div>
      
      {needsLocation && (
        <div className="form-group">
          <label>Location</label>
          <input 
            type="text" 
            placeholder="e.g. Austin, TX" 
            value={location}
            onChange={e => setLocation(e.target.value)}
          />
        </div>
      )}
      
      <div className="form-group">
        <label>Max Results</label>
        <input 
          type="number" 
          max="100" 
          value={maxResults}
          onChange={e => setMaxResults(e.target.value)}
        />
      </div>
      
      <button 
        className={`btn-primary ${isScraping ? 'is-scraping' : ''}`}
        onClick={handleScrape}
        disabled={isScraping || !query}
      >
        {isScraping ? statusText : 'Run Scrape'}
      </button>
    </div>
  );
}
