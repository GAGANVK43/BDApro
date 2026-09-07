/**
 * ratings.js - Content & Maturity Rating Patterns Controller
 */

let ratingPieChart = null;
let ratingShareChart = null;

async function loadRatingAnalytics(queryString = "") {
  const query = queryString ? `?${queryString}` : "";
  try {
    const res = await fetch(`/api/ratings${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const data = json.data;
      renderRatingPie(data);
      renderRatingShare(data);
      renderRatingTable(data);
    }
  } catch (e) {
    console.error("Rating analytics error:", e);
  }
}

function renderRatingPie(data) {
  if (ratingPieChart) ratingPieChart.destroy();
  const ctx = document.getElementById("rating-pie-chart").getContext("2d");
  ratingPieChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: data.map(d => d.rating),
      datasets: [{
        data: data.map(d => d.count),
        backgroundColor: ["#E50914", "#06B6D4", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#3B82F6", "#64748B"]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "right", labels: { color: "#F8FAFC" } } }
    }
  });
}

function renderRatingShare(data) {
  if (ratingShareChart) ratingShareChart.destroy();
  const ctx = document.getElementById("rating-share-chart").getContext("2d");
  ratingShareChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.rating),
      datasets: [
        { label: "Movies", data: data.map(d => d.movies), backgroundColor: "#E50914", borderRadius: 4 },
        { label: "TV Shows", data: data.map(d => d.tv_shows), backgroundColor: "#06B6D4", borderRadius: 4 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } }
      },
      plugins: { legend: { labels: { color: "#F8FAFC" } } }
    }
  });
}

function renderRatingTable(data) {
  const tbody = document.getElementById("rating-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  const total = data.reduce((acc, cur) => acc + cur.count, 0);
  data.forEach(r => {
    const pct = total > 0 ? ((r.count / total) * 100).toFixed(1) : 0;
    tbody.innerHTML += `
      <tr>
        <td><span class="badge badge-rating" style="font-size:0.85rem;">${r.rating}</span></td>
        <td style="font-weight:700; color:#fff;">${r.count}</td>
        <td>${r.movies}</td>
        <td>${r.tv_shows}</td>
        <td style="font-weight:600; color:#06B6D4;">${pct}%</td>
      </tr>
    `;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadRatingAnalytics();
  document.addEventListener("filtersChanged", (e) => loadRatingAnalytics(e.detail.queryString));
});
