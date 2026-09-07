/**
 * database.js - MongoDB Atlas & Architecture Controller
 */

async function loadDatabaseInfo() {
  try {
    const res = await fetch("/api/database-status");
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderDatabaseStats(json.data);
    }
  } catch (e) {
    console.error("Database status error:", e);
  }
}

function renderDatabaseStats(data) {
  const connPill = document.getElementById("db-conn-pill");
  const dbNameEl = document.getElementById("db-name-val");
  const totalDocsEl = document.getElementById("db-total-docs");
  const uriEl = document.getElementById("db-uri-val");
  const msgEl = document.getElementById("db-msg-val");
  const tbody = document.getElementById("db-collections-tbody");

  if (connPill) {
    connPill.className = `status-pill ${data.connected ? 'status-connected' : 'status-disconnected'}`;
    connPill.innerHTML = `<span class="status-dot"></span> MongoDB Status: ${data.status}`;
  }
  if (dbNameEl) dbNameEl.innerText = data.db_name;
  if (totalDocsEl) totalDocsEl.innerText = data.total_documents.toLocaleString();
  if (uriEl) uriEl.innerText = data.uri || "mongodb://localhost:27017/ (Local Fallback)";
  if (msgEl) msgEl.innerText = data.message;

  if (tbody) {
    tbody.innerHTML = "";
    const collections = data.collections || {};
    const standardCollections = [
      { name: "movies", desc: "Main catalog documents with nested genre and country arrays" },
      { name: "genre_statistics", desc: "Pre-aggregated genre frequency, Movie & TV show counts" },
      { name: "rating_statistics", desc: "Maturity rating distributions and breakdown" },
      { name: "release_statistics", desc: "Annual release counts and historical milestones" },
      { name: "country_statistics", desc: "Top content-producing country aggregations" },
      { name: "dashboard_summary", desc: "Global KPI metrics document for rapid dashboard rendering" }
    ];

    standardCollections.forEach(col => {
      const count = collections[col.name] !== undefined ? collections[col.name] : (data.connected ? 0 : "Cached");
      tbody.innerHTML += `
        <tr>
          <td style="font-weight:700; color:#10B981;">📁 ${col.name}</td>
          <td style="color:#CBD5E1;">${col.desc}</td>
          <td style="font-weight:700; color:#fff;">${typeof count === 'number' ? count.toLocaleString() : count}</td>
          <td><span class="badge ${count > 0 || count === 'Cached' ? 'badge-tv' : 'badge-movie'}">${count > 0 || count === 'Cached' ? 'ACTIVE' : 'EMPTY'}</span></td>
        </tr>
      `;
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadDatabaseInfo();
});
