/**
 * genres.js - Genre Deep-Dive Analysis Controller
 */

let genreChart = null;
let genreRatingChart = null;

async function loadGenreAnalytics(queryString = "") {
  const query = queryString ? `?${queryString}&top_n=25` : "?top_n=25";
  try {
    const res = await fetch(`/api/genres${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const data = json.data;
      renderGenreBreakdown(data);
      renderGenreRating(data);
      renderGenreTable(data);
    }
  } catch (e) {
    console.error("Genre analytics error:", e);
  }
}

function renderGenreBreakdown(data) {
  if (genreChart) genreChart.destroy();
  const ctx = document.getElementById("genre-breakdown-chart").getContext("2d");
  genreChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.genre),
      datasets: [
        { label: "Movies", data: data.map(d => d.movies), backgroundColor: "#E50914", borderRadius: 4 },
        { label: "TV Shows", data: data.map(d => d.tv_shows), backgroundColor: "#06B6D4", borderRadius: 4 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { color: "#334155" }, ticks: { color: "#94A3B8", maxRotation: 45 } },
        y: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } }
      },
      plugins: { legend: { labels: { color: "#F8FAFC" } } }
    }
  });
}

function renderGenreRating(data) {
  if (genreRatingChart) genreRatingChart.destroy();
  const ctx = document.getElementById("genre-rating-chart").getContext("2d");
  const sortedByRating = [...data].sort((a, b) => b.avg_rating - a.avg_rating);
  genreRatingChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: sortedByRating.map(d => d.genre),
      datasets: [{
        label: "Average Rating Score",
        data: sortedByRating.map(d => d.avg_rating),
        backgroundColor: "#10B981",
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { min: 0, max: 10, grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { grid: { display: false }, ticks: { color: "#F8FAFC" } }
      },
      plugins: { legend: { display: false } }
    }
  });
}

function renderGenreTable(data) {
  const tbody = document.getElementById("genre-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  data.forEach((g, idx) => {
    tbody.innerHTML += `
      <tr>
        <td style="font-weight:700; color:#E50914;">#${idx + 1}</td>
        <td style="font-weight:600; color:#fff;">${g.genre}</td>
        <td style="font-weight:700;">${g.count}</td>
        <td>${g.movies}</td>
        <td>${g.tv_shows}</td>
        <td style="color:#10B981; font-weight:700;">⭐ ${g.avg_rating}</td>
      </tr>
    `;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadGenreAnalytics();
  document.addEventListener("filtersChanged", (e) => loadGenreAnalytics(e.detail.queryString));
});
