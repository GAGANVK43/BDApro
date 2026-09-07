/**
 * releases.js - Historical Release Trends Controller
 */

let annualTrajectoryChart = null;

async function loadReleaseAnalytics(queryString = "") {
  const query = queryString ? `?${queryString}` : "";
  try {
    const res = await fetch(`/api/releases${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const data = json.data;
      renderAnnualTrajectory(data);
      renderReleaseTable(data);
      updateMilestones(data);
    }
  } catch (e) {
    console.error("Release analytics error:", e);
  }
}

function renderAnnualTrajectory(data) {
  if (annualTrajectoryChart) annualTrajectoryChart.destroy();
  const ctx = document.getElementById("release-trajectory-chart").getContext("2d");
  annualTrajectoryChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.release_year),
      datasets: [
        { label: "Movies", data: data.map(d => d.movies), backgroundColor: "#E50914", borderRadius: 4 },
        { label: "TV Shows", data: data.map(d => d.tv_shows), backgroundColor: "#06B6D4", borderRadius: 4 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { stacked: true, grid: { color: "#334155" }, ticks: { color: "#94A3B8" } }
      },
      plugins: { legend: { labels: { color: "#F8FAFC" } } }
    }
  });
}

function renderReleaseTable(data) {
  const tbody = document.getElementById("release-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  data.forEach(r => {
    tbody.innerHTML += `
      <tr>
        <td style="font-weight:700; color:#fff;">${r.release_year}</td>
        <td style="font-weight:700;">${r.count}</td>
        <td>${r.movies}</td>
        <td>${r.tv_shows}</td>
        <td style="color:#F59E0B; font-weight:600;">${r.cumulative_content}</td>
      </tr>
    `;
  });
}

function updateMilestones(data) {
  if (!data || data.length === 0) return;
  const peak = [...data].sort((a, b) => b.count - a.count)[0];
  const earliest = data[0].release_year;
  const latest = data[data.length - 1].release_year;

  const peakEl = document.getElementById("milestone-peak");
  const spanEl = document.getElementById("milestone-span");

  if (peakEl) peakEl.innerText = `${peak.release_year} (${peak.count} titles)`;
  if (spanEl) spanEl.innerText = `${earliest} - ${latest} (${latest - earliest + 1} years)`;
}

document.addEventListener("DOMContentLoaded", () => {
  loadReleaseAnalytics();
  document.addEventListener("filtersChanged", (e) => loadReleaseAnalytics(e.detail.queryString));
});
