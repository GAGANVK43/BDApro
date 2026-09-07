/**
 * main.js - Global Frontend Controller & Filter Management
 * Handles API communication, filter states, live status polling, and event dispatching.
 */

const App = {
  filters: {
    min_year: null,
    max_year: null,
    types: "All",
    genres: "All",
    countries: "All",
    ratings: "All",
    q: ""
  },

  init() {
    this.loadFilterMetadata();
    this.pollSystemStatus();
    this.bindFilterEvents();
    // Poll status every 30 seconds
    setInterval(() => this.pollSystemStatus(), 30000);
  },

  buildQueryString() {
    const params = new URLSearchParams();
    if (this.filters.min_year && this.filters.max_year) {
      params.append("min_year", this.filters.min_year);
      params.append("max_year", this.filters.max_year);
    }
    if (this.filters.types && this.filters.types !== "All") params.append("types", this.filters.types);
    if (this.filters.genres && this.filters.genres !== "All") params.append("genres", this.filters.genres);
    if (this.filters.countries && this.filters.countries !== "All") params.append("countries", this.filters.countries);
    if (this.filters.ratings && this.filters.ratings !== "All") params.append("ratings", this.filters.ratings);
    if (this.filters.q && this.filters.q.trim()) params.append("q", this.filters.q.trim());
    return params.toString();
  },

  async loadFilterMetadata() {
    try {
      const res = await fetch("/api/filters");
      const json = await res.json();
      if (json.status === "success" && json.data) {
        const d = json.data;
        
        // Year filter
        const yearSelect = document.getElementById("filter-year");
        if (yearSelect) {
          yearSelect.innerHTML = `<option value="All">All Years (${d.min_year} - ${d.max_year})</option>`;
          for (let y = d.max_year; y >= d.min_year; y--) {
            yearSelect.innerHTML += `<option value="${y}">${y}</option>`;
          }
        }

        // Genre filter
        const genreSelect = document.getElementById("filter-genre");
        if (genreSelect && d.genres) {
          genreSelect.innerHTML = `<option value="All">All Genres (${d.genres.length})</option>`;
          d.genres.forEach(g => {
            genreSelect.innerHTML += `<option value="${g}">${g}</option>`;
          });
        }

        // Country filter
        const countrySelect = document.getElementById("filter-country");
        if (countrySelect && d.countries) {
          countrySelect.innerHTML = `<option value="All">All Countries (${d.countries.length})</option>`;
          d.countries.forEach(c => {
            countrySelect.innerHTML += `<option value="${c}">${c}</option>`;
          });
        }

        // Rating filter
        const ratingSelect = document.getElementById("filter-rating");
        if (ratingSelect && d.ratings) {
          ratingSelect.innerHTML = `<option value="All">All Ratings</option>`;
          d.ratings.forEach(r => {
            ratingSelect.innerHTML += `<option value="${r}">${r}</option>`;
          });
        }
      }
    } catch (e) {
      console.warn("Failed to load filter metadata:", e);
    }
  },

  bindFilterEvents() {
    const applyBtn = document.getElementById("btn-apply-filters");
    const resetBtn = document.getElementById("btn-reset-filters");
    const searchInput = document.getElementById("filter-search");

    if (applyBtn) {
      applyBtn.addEventListener("click", () => {
        this.readFilterValues();
        this.dispatchFilterChange();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        this.resetFilters();
        this.dispatchFilterChange();
      });
    }

    if (searchInput) {
      searchInput.addEventListener("keyup", (e) => {
        if (e.key === "Enter") {
          this.readFilterValues();
          this.dispatchFilterChange();
        }
      });
    }
  },

  readFilterValues() {
    const yearSelect = document.getElementById("filter-year");
    const typeSelect = document.getElementById("filter-type");
    const genreSelect = document.getElementById("filter-genre");
    const countrySelect = document.getElementById("filter-country");
    const ratingSelect = document.getElementById("filter-rating");
    const searchInput = document.getElementById("filter-search");

    if (yearSelect && yearSelect.value !== "All") {
      this.filters.min_year = yearSelect.value;
      this.filters.max_year = yearSelect.value;
    } else {
      this.filters.min_year = null;
      this.filters.max_year = null;
    }

    if (typeSelect) this.filters.types = typeSelect.value;
    if (genreSelect) this.filters.genres = genreSelect.value;
    if (countrySelect) this.filters.countries = countrySelect.value;
    if (ratingSelect) this.filters.ratings = ratingSelect.value;
    if (searchInput) this.filters.q = searchInput.value;
  },

  resetFilters() {
    this.filters = { min_year: null, max_year: null, types: "All", genres: "All", countries: "All", ratings: "All", q: "" };
    const elements = ["filter-year", "filter-type", "filter-genre", "filter-country", "filter-rating"];
    elements.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = "All";
    });
    const searchInput = document.getElementById("filter-search");
    if (searchInput) searchInput.value = "";
  },

  dispatchFilterChange() {
    const event = new CustomEvent("filtersChanged", { detail: { queryString: this.buildQueryString() } });
    document.dispatchEvent(event);
  },

  async pollSystemStatus() {
    try {
      const [dbRes, pipeRes] = await Promise.all([
        fetch("/api/database-status"),
        fetch("/api/pipeline-status")
      ]);
      const dbJson = await dbRes.json();
      const pipeJson = await pipeRes.json();

      // Top bar MongoDB pill
      const mongoPill = document.getElementById("top-mongo-status");
      if (mongoPill && dbJson.status === "success") {
        const isConnected = dbJson.data.connected;
        mongoPill.className = `status-pill ${isConnected ? "status-connected" : "status-disconnected"}`;
        mongoPill.innerHTML = `<span class="status-dot"></span> MongoDB: ${isConnected ? "Connected" : "Local Fallback"}`;
      }

      // Top bar Pipeline pill
      const pipePill = document.getElementById("top-pipeline-status");
      if (pipePill && pipeJson.status === "success") {
        pipePill.className = "status-pill status-connected";
        pipePill.innerHTML = `<span class="status-dot"></span> Pipeline: Ready`;
      }
    } catch (e) {
      console.warn("Status polling error:", e);
    }
  }
};

document.addEventListener("DOMContentLoaded", () => {
  App.init();
});
