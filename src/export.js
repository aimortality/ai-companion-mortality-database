// Data Export Utilities for AI Mortality Database
// Can be integrated into the main index.html or used standalone

const mortalityData = {
  metadata: {
    version: "3.0.0",
    last_updated: "2026-03-06",
    total_fatalities: 25,
    total_incidents: 16,
    ai_users_deceased: 15,
    third_party_victims: 10,
    total_attempts: 1,
    taxonomy_version: "1.0.0",
    crisis_support: "988"
  },
  platforms: [
    {
      name: "Character.AI",
      deaths: 2,
      attempts: 1,
      cases: [
        { name: "Sewell Setzer III", age: 14, date: "2024-02-28", location: "Florida, USA" },
        { name: "Juliana Peralta", age: 13, date: "2023-11-08", location: "Colorado, USA" },
        { name: "Nina", age: 16, date: "2024-11", outcome: "Survived", location: "New York, USA" }
      ]
    },
    {
      name: "ChatGPT/OpenAI",
      deaths: 10,
      fatalities_total: 20,
      attempts: 0,
      cases: [
        { name: "Joshua Enneking", age: 26, date: "2024-08-03", location: "Florida, USA", mechanism: "relational" },
        { name: "Sophie Rottenberg", age: 29, date: "2025-02", location: "USA", mechanism: "relational" },
        { name: "Margaux Whittemore", age: 32, date: "2025-02-19", location: "Maine, USA", mechanism: "cognitive", type: "third_party_victim" },
        { name: "Adam Raine", age: 16, date: "2025-04-11", location: "California, USA", mechanism: "relational" },
        { name: "Alex Taylor", age: 35, date: "2025-04-25", location: "USA", mechanism: "cognitive" },
        { name: "Sam Nelson", age: 19, date: "2025-05-31", location: "California, USA", mechanism: "relational" },
        { name: "Amaurie Lacey", age: 17, date: "2025-06-02", location: "Georgia, USA", mechanism: "relational" },
        { name: "Joe Ceccanti", age: 48, date: "2025", location: "Oregon, USA", mechanism: "cognitive" },
        { name: "Zane Shamblin", age: 23, date: "2025-07-25", location: "Texas, USA", mechanism: "relational" },
        { name: "Suzanne Adams", age: 83, date: "2025-08-01", location: "Connecticut, USA", mechanism: "cognitive", type: "third_party_victim" },
        { name: "Stein-Erik Soelberg", age: 56, date: "2025-08-01", location: "Connecticut, USA", mechanism: "cognitive" },
        { name: "Jesse van Rootselaar", age: 18, date: "2026-02-10", location: "British Columbia, Canada", mechanism: "instrumental", notes: "8 third-party victims" }
      ]
    },
    {
      name: "Chai AI",
      deaths: 1,
      attempts: 0,
      cases: [
        { name: "Pierre", age: 30, date: "2023-03", location: "Belgium" }
      ]
    },
    {
      name: "Meta AI",
      deaths: 1,
      attempts: 0,
      cases: [
        { name: "Thongbue Wongbandue", age: 78, date: "2025-03-31", location: "New Jersey, USA" }
      ]
    },
    {
      name: "Gemini",
      deaths: 1,
      attempts: 0,
      cases: [
        { name: "Jonathan Gavalas", age: 36, date: "2025-10-02", location: "Florida, USA", mechanism: "cognitive/relational" }
      ]
    },
    {
      name: "Anthropic/Claude",
      deaths: 0,
      attempts: 0,
      cases: []
    },
    {
      name: "Replika",
      deaths: 0,
      attempts: 0,
      cases: []
    }
  ]
};

// Export functions
const DataExporter = {
  // Export as JSON
  toJSON: function() {
    return JSON.stringify(mortalityData, null, 2);
  },

  // Export as CSV
  toCSV: function() {
    const headers = ['Platform', 'Victim Name', 'Age', 'Date', 'Location', 'Outcome'];
    const rows = [headers.join(',')];

    mortalityData.platforms.forEach(platform => {
      platform.cases.forEach(victim => {
        const row = [
          platform.name,
          victim.name,
          victim.age,
          victim.date,
          victim.location,
          victim.outcome || 'Death'
        ];
        rows.push(row.map(cell => `"${cell}"`).join(','));
      });
    });

    return rows.join('\n');
  },

  // Export summary statistics
  toStatistics: function() {
    const stats = {
      total_fatalities: mortalityData.metadata.total_fatalities,
      ai_users_deceased: mortalityData.metadata.ai_users_deceased,
      third_party_victims: mortalityData.metadata.third_party_victims,
      total_attempts: mortalityData.metadata.total_attempts,
      platforms_with_deaths: mortalityData.platforms.filter(p => p.deaths > 0).length,
      deaths_by_platform: {},
      age_statistics: {
        youngest: 11,
        oldest: 83,
        average: 29.0,
        minors: 10,
        adults: 15
      },
      deaths_by_year: {
        "2023": 2,
        "2024": 2,
        "2025": 11,
        "2026": 1
      }
    };

    mortalityData.platforms.forEach(platform => {
      stats.deaths_by_platform[platform.name] = platform.deaths;
    });

    return JSON.stringify(stats, null, 2);
  },

  // Download function
  download: function(data, filename, type) {
    const blob = new Blob([data], { type: type });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  // Convenience methods for direct download
  downloadJSON: function() {
    this.download(
      this.toJSON(),
      'ai-mortality-data.json',
      'application/json'
    );
  },

  downloadCSV: function() {
    this.download(
      this.toCSV(),
      'ai-mortality-data.csv',
      'text/csv'
    );
  },

  downloadStats: function() {
    this.download(
      this.toStatistics(),
      'ai-mortality-statistics.json',
      'application/json'
    );
  }
};

// Add export buttons to page (can be integrated into main app)
function addExportButtons(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const exportSection = document.createElement('div');
  exportSection.style.cssText = `
    padding: 20px;
    background: var(--bg-secondary);
    border-radius: 12px;
    margin: 20px 0;
    text-align: center;
  `;

  exportSection.innerHTML = `
    <h3 style="margin-bottom: 16px; color: var(--text-primary);">
      Export Data
    </h3>
    <p style="margin-bottom: 16px; color: var(--text-secondary); font-size: 0.9rem;">
      Download the complete dataset for research or analysis
    </p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <button
        onclick="DataExporter.downloadJSON()"
        style="
          padding: 10px 20px;
          background: var(--accent-info);
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: all 200ms ease;
        "
        onmouseover="this.style.transform='translateY(-2px)'"
        onmouseout="this.style.transform='translateY(0)'"
      >
        📊 Download JSON
      </button>
      <button
        onclick="DataExporter.downloadCSV()"
        style="
          padding: 10px 20px;
          background: var(--accent-success);
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: all 200ms ease;
        "
        onmouseover="this.style.transform='translateY(-2px)'"
        onmouseout="this.style.transform='translateY(0)'"
      >
        📈 Download CSV
      </button>
      <button
        onclick="DataExporter.downloadStats()"
        style="
          padding: 10px 20px;
          background: var(--accent-warning);
          color: var(--text-inverse);
          border: none;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: all 200ms ease;
        "
        onmouseover="this.style.transform='translateY(-2px)'"
        onmouseout="this.style.transform='translateY(0)'"
      >
        📉 Download Statistics
      </button>
    </div>
    <p style="margin-top: 16px; font-size: 0.8rem; color: var(--text-muted);">
      All data is verified through court documents, news sources, or government acknowledgment.<br>
      For contributing new cases, visit our <a href="https://github.com/[username]/ai-mortality-database" style="color: var(--accent-info);">GitHub repository</a>.
    </p>
  `;

  container.appendChild(exportSection);
}

// Copy to clipboard function for sharing
function copyDataLink() {
  const link = window.location.href;
  navigator.clipboard.writeText(link).then(() => {
    alert('Database link copied to clipboard!');
  });
}

// Generate embeddable widget code
function generateEmbedCode() {
  const embedCode = `
<!-- AI Mortality Database Widget -->
<iframe
  src="${window.location.href}?embed=true"
  width="100%"
  height="400"
  frameborder="0"
  style="border: 1px solid #ddd; border-radius: 8px;">
</iframe>
<p style="font-size: 12px; text-align: center;">
  <a href="${window.location.href}" target="_blank">
    View Full AI Mortality Database
  </a>
</p>`;

  return embedCode;
}

// API endpoint generator (for researchers)
const API = {
  endpoints: {
    allData: '/api/v1/data',
    platforms: '/api/v1/platforms',
    statistics: '/api/v1/statistics',
    timeline: '/api/v1/timeline',
    recent: '/api/v1/recent'
  },

  // Mock API response generator
  generateResponse: function(endpoint) {
    switch(endpoint) {
      case 'platforms':
        return mortalityData.platforms;
      case 'statistics':
        return {
          total_fatalities: 25,
          ai_users_deceased: 15,
          third_party_victims: 10,
          total_attempts: 1,
          minors_percentage: 40.0,
          platforms_affected: 5
        };
      case 'timeline':
        return mortalityData.platforms
          .flatMap(p => p.cases.map(c => ({...c, platform: p.name})))
          .sort((a, b) => new Date(a.date) - new Date(b.date));
      case 'recent':
        return mortalityData.platforms
          .flatMap(p => p.cases.map(c => ({...c, platform: p.name})))
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .slice(0, 5);
      default:
        return mortalityData;
    }
  }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { DataExporter, API };
}

// Make available globally
window.DataExporter = DataExporter;
window.MortalityAPI = API;