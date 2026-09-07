/**
 * dashboard.js - Executive Dashboard Charts & Analytics Engine
 * Renders KPI cards, dynamic narrative insights, and interactive Chart.js visualizations.
 */

let charts = {};

async function loadDashboard(queryString = "") {
  const query = queryString ? `?${queryString}` : "";

  // 1. Fetch Summary & KPIs
  try {
    const res = await fetch(`/api/summary${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const kpis = json.data.kpis;
      const insights = json.data.insights;

      // Update KPI Cards
      document.getElementById("kpi-total").innerText = kpis.total_content.toLocaleString();
      document.getElementById("kpi-movies").innerText = kpis.movies.toLocaleString();
      document.getElementById("kpi-tv").innerText = kpis.tv_shows.toLocaleString();
      document.getElementById("kpi-rating").innerText = kpis.avg_rating.toFixed(1);
      document.getElementById("kpi-countries").innerText = kpis.unique_countries;
      document.getElementById("kpi-genres").innerText = kpis.unique_genres;

      // Update Dynamic Insights
      const bannerText = document.getElementById("insight-text");
      if (bannerText) {
        bannerText.innerHTML = `<strong>Data Insights:</strong> ${insights.genre_insight} &bull; ${insights.type_insight} &bull; ${insights.release_insight}`;
      }
    }
  } catch (e) {
    console.error("Summary load error:", e);
  }

  // 2. Fetch & Render Genre Chart
  try {
    const res = await fetch(`/api/genres${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderGenreChart(json.data.slice(0, 8));
    }
  } catch (e) {
    console.error("Genre chart error:", e);
  }

  // 3. Fetch & Render Release Trend & Growth Charts
  try {
    const res = await fetch(`/api/releases${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderReleaseTrendChart(json.data);
      renderGrowthChart(json.data);
    }
  } catch (e) {
    console.error("Release chart error:", e);
  }

  // 4. Fetch & Render Movie vs TV Donut & Rating Distribution
  try {
    const [rateRes, sumRes] = await Promise.all([
      fetch(`/api/ratings${query}`),
      fetch(`/api/summary${query}`)
    ]);
    const rateJson = await rateRes.json();
    const sumJson = await sumRes.json();

    if (sumJson.status === "success" && sumJson.data) {
      renderDonutChart(sumJson.data.kpis.movies, sumJson.data.kpis.tv_shows);
    }
    if (rateJson.status === "success" && rateJson.data) {
      renderRatingChart(rateJson.data);
    }
  } catch (e) {
    console.error("Rating / Donut error:", e);
  }

  // 5. Fetch & Render Country Chart
  try {
    const res = await fetch(`/api/countries${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderCountryChart(json.data.slice(0, 8));
    }
  } catch (e) {
    console.error("Country chart error:", e);
  }

  // 6. Fetch & Render Top Movies Table
  try {
    const res = await fetch(`/api/top-movies${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderTopMoviesTable(json.data);
    }
  } catch (e) {
    console.error("Top movies error:", e);
  }
}

// Chart.js Chart Helpers
function destroyChart(name) {
  if (charts[name]) {
    charts[name].destroy();
  }
}

function renderGenreChart(data) {
  destroyChart("genre");
  const ctx = document.getElementById("chart-genre").getContext("2d");
  charts["genre"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.genre),
      datasets: [{
        label: "Total Titles",
        data: data.map(d => d.count),
        backgroundColor: "rgba(229, 9, 20, 0.8)",
        borderColor: "#E50914",
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { grid: { display: false }, ticks: { color: "#F8FAFC" } }
      }
    }
  });
}

function renderReleaseTrendChart(data) {
  destroyChart("release");
  const ctx = document.getElementById("chart-release").getContext("2d");
  charts["release"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.map(d => d.release_year),
      datasets: [
        {
          label: "Movies",
          data: data.map(d => d.movies),
          borderColor: "#E50914",
          backgroundColor: "rgba(229, 9, 20, 0.1)",
          tension: 0.3,
          fill: true
        },
        {
          label: "TV Shows",
          data: data.map(d => d.tv_shows),
          borderColor: "#06B6D4",
          backgroundColor: "rgba(6, 182, 212, 0.1)",
          tension: 0.3,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#F8FAFC" } } },
      scales: {
        x: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } }
      }
    }
  });
}

function renderDonutChart(movies, tvShows) {
  destroyChart("donut");
  const ctx = document.getElementById("chart-donut").getContext("2d");
  charts["donut"] = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Movies", "TV Shows"],
      datasets: [{
        data: [movies, tvShows],
        backgroundColor: ["#E50914", "#06B6D4"],
        borderColor: "#1E293B",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom", labels: { color: "#F8FAFC" } } },
      cutout: "65%"
    }
  });
}

function renderRatingChart(data) {
  destroyChart("rating");
  const ctx = document.getElementById("chart-rating").getContext("2d");
  charts["rating"] = new Chart(ctx, {
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
      plugins: { legend: { labels: { color: "#F8FAFC" } } },
      scales: {
        x: { stacked: true, grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { stacked: true, grid: { color: "#334155" }, ticks: { color: "#94A3B8" } }
      }
    }
  });
}

function renderCountryChart(data) {
  destroyChart("country");
  const ctx = document.getElementById("chart-country").getContext("2d");
  charts["country"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.country),
      datasets: [{
        label: "Productions",
        data: data.map(d => d.count),
        backgroundColor: "#06B6D4",
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { grid: { display: false }, ticks: { color: "#F8FAFC" } }
      }
    }
  });
}

function renderGrowthChart(data) {
  destroyChart("growth");
  const ctx = document.getElementById("chart-growth").getContext("2d");
  charts["growth"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.map(d => d.release_year),
      datasets: [{
        label: "Cumulative Catalog Titles",
        data: data.map(d => d.cumulative_content),
        borderColor: "#F59E0B",
        backgroundColor: "rgba(245, 158, 11, 0.15)",
        tension: 0.3,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "#F8FAFC" } } },
      scales: {
        x: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { grid: { color: "#334155" }, ticks: { color: "#94A3B8" } }
      }
    }
  });
}

function renderTopMoviesTable(movies) {
  const tbody = document.getElementById("top-movies-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  movies.forEach(m => {
    const badgeClass = m.type === "Movie" ? "badge-movie" : "badge-tv";
    tbody.innerHTML += `
      <tr>
        <td style="font-weight:600; color:#fff;">${m.title}</td>
        <td><span class="badge ${badgeClass}">${m.type}</span></td>
        <td>${m.release_year}</td>
        <td><span class="badge badge-rating">${m.rating}</span></td>
        <td style="font-weight:700; color:#F59E0B;">⭐ ${m.rating_score || '7.5'}</td>
        <td>${m.primary_genre}</td>
        <td>${m.primary_country}</td>
        <td>${m.duration}</td>
      </tr>
    `;
  });
}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
  document.addEventListener("filtersChanged", (e) => {
    loadDashboard(e.detail.queryString);
  });
});
