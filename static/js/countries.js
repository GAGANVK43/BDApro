/**
 * countries.js - Geographic & Country Distribution Controller
 */

let countryChart = null;

async function loadCountryAnalytics(queryString = "") {
  const query = queryString ? `?${queryString}&top_n=20` : "?top_n=20";
  try {
    const res = await fetch(`/api/countries${query}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const data = json.data;
      renderCountryBar(data);
      renderCountryTable(data);
    }
  } catch (e) {
    console.error("Country analytics error:", e);
  }
}

function renderCountryBar(data) {
  if (countryChart) countryChart.destroy();
  const ctx = document.getElementById("country-bar-chart").getContext("2d");
  countryChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map(d => d.country),
      datasets: [
        { label: "Movies", data: data.map(d => d.movies), backgroundColor: "#E50914", borderRadius: 4 },
        { label: "TV Shows", data: data.map(d => d.tv_shows), backgroundColor: "#06B6D4", borderRadius: 4 }
      ]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { color: "#334155" }, ticks: { color: "#94A3B8" } },
        y: { stacked: true, grid: { display: false }, ticks: { color: "#F8FAFC" } }
      },
      plugins: { legend: { labels: { color: "#F8FAFC" } } }
    }
  });
}

function renderCountryTable(data) {
  const tbody = document.getElementById("country-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  data.forEach((c, idx) => {
    tbody.innerHTML += `
      <tr>
        <td style="font-weight:700; color:#06B6D4;">#${idx + 1}</td>
        <td style="font-weight:600; color:#fff;">${c.country}</td>
        <td style="font-weight:700;">${c.count}</td>
        <td>${c.movies}</td>
        <td>${c.tv_shows}</td>
      </tr>
    `;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadCountryAnalytics();
  document.addEventListener("filtersChanged", (e) => loadCountryAnalytics(e.detail.queryString));
});
