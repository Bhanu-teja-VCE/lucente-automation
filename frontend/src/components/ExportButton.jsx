import React from 'react';

export default function ExportButton({ filters, apiBase }) {
  const handleExport = () => {
    const params = new URLSearchParams();
    if (filters.hasEmail) params.append('has_email', 'true');
    if (filters.hasWebsite) params.append('has_website', 'true');
    if (filters.minRating > 0) params.append('min_rating', filters.minRating);
    if (filters.minScore > 0) params.append('min_score', filters.minScore);
    if (filters.search) params.append('search', filters.search);
    filters.platforms.forEach(p => params.append('platform', p));

    const url = `${apiBase}/export/csv?${params.toString()}`;
    window.open(url, '_blank');
  };

  return (
    <button className="export-btn" onClick={handleExport}>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="7 10 12 15 17 10"></polyline>
        <line x1="12" y1="15" x2="12" y2="3"></line>
      </svg>
      Export CSV
    </button>
  );
}
