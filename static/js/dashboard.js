/**
 * dashboard.js - Executive Dashboard Charts & Analytics Engine
 * Enterprise Chart.js rendering with gradients, custom tooltips, and interactive actions.
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

      // Update Subtext Shares
      const total = kpis.total_content || 1;
      const mPct = ((kpis.movies / total) * 100).toFixed(1);
      const tPct = ((kpis.tv_shows / total) * 100).toFixed(1);
      const mShareEl = document.getElementById("kpi-movie-share");
      const tShareEl = document.getElementById("kpi-tv-share");
      if (mShareEl) mShareEl.innerText = `${mPct}% Catalog Share`;
      if (tShareEl) tShareEl.innerText = `${tPct}% Episodic Share`;

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

const defaultChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: "#F8FAFC",
        font: { family: "Inter", weight: "600", size: 12 },
        usePointStyle: true,
        padding: 16
      }
    },
    tooltip: {
      backgroundColor: "#0F172A",
      titleColor: "#F8FAFC",
      bodyColor: "#CBD5E1",
      borderColor: "#334155",
      borderWidth: 1,
      padding: 12,
      cornerRadius: 8,
      boxPadding: 4,
      usePointStyle: true
    }
  }
};

function renderGenreChart(data) {
  destroyChart("genre");
  const ctx = document.getElementById("chart-genre").getContext("2d");
  
  const gradient = ctx.createLinearGradient(0, 0, 400, 0);
  gradient.addColorStop(0, "rgba(229, 9, 20, 0.9)");
  gradient.addColorStop(1, "rgba(255, 75, 75, 0.6)");

  charts["genre"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.genre),
      datasets: [{
        label: "Total Titles",
        data: data.map(d => d.count),
        backgroundColor: gradient,
        borderColor: "#E50914",
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      ...defaultChartOptions,
      indexAxis: "y",
      plugins: { ...defaultChartOptions.plugins, legend: { display: false } },
      scales: {
        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } },
        y: { grid: { display: false }, ticks: { color: "#F8FAFC", font: { weight: "600" } } }
      }
    }
  });
}

function renderReleaseTrendChart(data) {
  destroyChart("release");
  const ctx = document.getElementById("chart-release").getContext("2d");
  
  const movieGrad = ctx.createLinearGradient(0, 0, 0, 300);
  movieGrad.addColorStop(0, "rgba(229, 9, 20, 0.25)");
  movieGrad.addColorStop(1, "rgba(229, 9, 20, 0.0)");

  const tvGrad = ctx.createLinearGradient(0, 0, 0, 300);
  tvGrad.addColorStop(0, "rgba(6, 182, 212, 0.25)");
  tvGrad.addColorStop(1, "rgba(6, 182, 212, 0.0)");

  charts["release"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.map(d => d.release_year),
      datasets: [
        {
          label: "Movies",
          data: data.map(d => d.movies),
          borderColor: "#E50914",
          backgroundColor: movieGrad,
          tension: 0.35,
          fill: true,
          pointRadius: 3,
          pointHoverRadius: 6,
          borderWidth: 2.5
        },
        {
          label: "TV Shows",
          data: data.map(d => d.tv_shows),
          borderColor: "#06B6D4",
          backgroundColor: tvGrad,
          tension: 0.35,
          fill: true,
          pointRadius: 3,
          pointHoverRadius: 6,
          borderWidth: 2.5
        }
      ]
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } },
        y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } }
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
        borderColor: "#131B2E",
        borderWidth: 3,
        hoverOffset: 6
      }]
    },
    options: {
      ...defaultChartOptions,
      plugins: {
        ...defaultChartOptions.plugins,
        legend: { position: "bottom", labels: { color: "#F8FAFC", font: { weight: "600" }, padding: 16 } }
      },
      cutout: "68%"
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
      ...defaultChartOptions,
      scales: {
        x: { stacked: true, grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8", font: { weight: "600" } } },
        y: { stacked: true, grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } }
      }
    }
  });
}

function renderCountryChart(data) {
  destroyChart("country");
  const ctx = document.getElementById("chart-country").getContext("2d");
  
  const cGrad = ctx.createLinearGradient(0, 0, 400, 0);
  cGrad.addColorStop(0, "rgba(6, 182, 212, 0.9)");
  cGrad.addColorStop(1, "rgba(56, 189, 248, 0.6)");

  charts["country"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.country),
      datasets: [{
        label: "Productions",
        data: data.map(d => d.count),
        backgroundColor: cGrad,
        borderRadius: 6
      }]
    },
    options: {
      ...defaultChartOptions,
      indexAxis: "y",
      plugins: { ...defaultChartOptions.plugins, legend: { display: false } },
      scales: {
        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } },
        y: { grid: { display: false }, ticks: { color: "#F8FAFC", font: { weight: "600" } } }
      }
    }
  });
}

function renderGrowthChart(data) {
  destroyChart("growth");
  const ctx = document.getElementById("chart-growth").getContext("2d");
  
  const gGrad = ctx.createLinearGradient(0, 0, 0, 300);
  gGrad.addColorStop(0, "rgba(245, 158, 11, 0.35)");
  gGrad.addColorStop(1, "rgba(245, 158, 11, 0.0)");

  charts["growth"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.map(d => d.release_year),
      datasets: [{
        label: "Cumulative Catalog Titles",
        data: data.map(d => d.cumulative_content),
        borderColor: "#F59E0B",
        backgroundColor: gGrad,
        tension: 0.35,
        fill: true,
        borderWidth: 2.5,
        pointRadius: 3
      }]
    },
    options: {
      ...defaultChartOptions,
      scales: {
        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } },
        y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94A3B8" } }
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
        <td style="font-weight:700; color:#fff;">${m.title}</td>
        <td><span class="badge ${badgeClass}">${m.type}</span></td>
        <td style="color:#CBD5E1;">${m.release_year}</td>
        <td><span class="badge badge-rating">${m.rating}</span></td>
        <td style="font-weight:700; color:#F59E0B;">⭐ ${m.rating_score || '7.5'}</td>
        <td><span style="color:#38BDF8; font-weight:500;">${m.primary_genre}</span></td>
        <td style="color:#94A3B8;">${m.primary_country}</td>
        <td style="color:#94A3B8;">${m.duration}</td>
        <td>
          <button class="btn btn-secondary" style="height:28px; padding:2px 10px; font-size:0.75rem;" onclick="openMovieDetail('${m.show_id}')">
            👁️ Inspect
          </button>
        </td>
      </tr>
    `;
  });
}

// Global modal detail loader
async function openMovieDetail(showId) {
  try {
    const res = await fetch(`/api/movie/${showId}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const m = json.data;
      const modal = document.getElementById("movie-modal");
      const modalBody = document.getElementById("modal-body-content");
      if (!modal || !modalBody) return;

      const badgeClass = m.type === "Movie" ? "badge-movie" : "badge-tv";

      modalBody.innerHTML = `
        <div style="margin-bottom:16px;">
          <div style="display:flex; gap:8px; align-items:center; margin-bottom:8px;">
            <span class="badge ${badgeClass}">${m.type}</span>
            <span class="badge badge-rating">${m.rating}</span>
            <span style="color:#F59E0B; font-weight:700;">⭐ ${m.rating_score || '7.5'} / 10</span>
          </div>
          <h2 style="color:#fff; font-size:1.6rem; font-weight:800; margin-bottom:6px;">${m.title}</h2>
          <p style="font-size:0.85rem; color:#94A3B8;">
            Release Year: <strong style="color:#fff;">${m.release_year}</strong> &bull; 
            Duration: <strong style="color:#fff;">${m.duration}</strong>
          </p>
        </div>

        <div style="background:#0A0E1A; border-radius:8px; padding:16px; margin-bottom:16px; border:1px solid rgba(255,255,255,0.08);">
          <h4 style="font-size:0.8rem; text-transform:uppercase; color:#94A3B8; margin-bottom:6px; letter-spacing:0.06em;">Plot Synopsis</h4>
          <p style="font-size:0.92rem; color:#E2E8F0; line-height:1.6;">${m.description}</p>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; font-size:0.85rem;">
          <div>
            <span style="color:#94A3B8; font-size:0.75rem; text-transform:uppercase;">🎭 Genres:</span><br>
            <strong style="color:#fff;">${m.listed_in}</strong>
          </div>
          <div>
            <span style="color:#94A3B8; font-size:0.75rem; text-transform:uppercase;">🌍 Production Country:</span><br>
            <strong style="color:#fff;">${m.country}</strong>
          </div>
          <div>
            <span style="color:#94A3B8; font-size:0.75rem; text-transform:uppercase;">🎬 Director:</span><br>
            <strong style="color:#fff;">${m.director}</strong>
          </div>
          <div>
            <span style="color:#94A3B8; font-size:0.75rem; text-transform:uppercase;">👥 Cast:</span><br>
            <strong style="color:#fff;">${m.cast}</strong>
          </div>
        </div>
      `;

      modal.style.display = "flex";
    }
  } catch (e) {
    console.error("Modal detail load error:", e);
  }
}

function closeModal() {
  const modal = document.getElementById("movie-modal");
  if (modal) modal.style.display = "none";
}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
  document.addEventListener("filtersChanged", (e) => {
    loadDashboard(e.detail.queryString);
  });
});
