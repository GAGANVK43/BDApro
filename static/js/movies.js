/**
 * movies.js - Movie Explorer Controller with Modal & Pagination
 */

let currentPage = 1;
const pageSize = 12;

async function loadMovies(queryString = "", page = 1) {
  currentPage = page;
  const baseQuery = queryString ? `${queryString}&` : "";
  const fullQuery = `?${baseQuery}page=${page}&page_size=${pageSize}`;

  try {
    const res = await fetch(`/api/movies${fullQuery}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      renderMoviesGrid(json.data.movies);
      renderPagination(json.data.page, json.data.total_pages, json.data.total_count);
    }
  } catch (e) {
    console.error("Movie load error:", e);
  }
}

function renderMoviesGrid(movies) {
  const container = document.getElementById("movies-container");
  if (!container) return;
  container.innerHTML = "";

  if (!movies || movies.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align:center; padding: 40px; color:#94A3B8;">
        <h3>🔍 No titles found matching your search or filters.</h3>
        <p>Try clearing filters or searching with different keywords.</p>
      </div>
    `;
    return;
  }

  movies.forEach(m => {
    const badgeClass = m.type === "Movie" ? "badge-movie" : "badge-tv";
    container.innerHTML += `
      <div class="kpi-card" style="cursor:pointer; display:flex; flex-direction:column; justify-content:space-between;" onclick="openMovieDetail('${m.show_id}')">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
            <span class="badge ${badgeClass}">${m.type}</span>
            <span style="color:#F59E0B; font-weight:700; font-size:0.85rem;">⭐ ${m.rating_score || '7.5'}</span>
          </div>
          <h4 style="color:#fff; font-size:1.05rem; font-weight:700; margin-bottom:6px;">${m.title}</h4>
          <p style="font-size:0.78rem; color:#94A3B8; margin-bottom:8px;">
            <span>${m.release_year}</span> &bull; 
            <span>${m.rating}</span> &bull; 
            <span>${m.duration}</span>
          </p>
          <p style="font-size:0.8rem; color:#CBD5E1; line-clamp: 2; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom:12px;">
            ${m.description}
          </p>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #334155; padding-top:10px; font-size:0.75rem; color:#64748B;">
          <span>🎭 ${m.primary_genre}</span>
          <span>🌍 ${m.primary_country}</span>
        </div>
      </div>
    `;
  });
}

function renderPagination(page, totalPages, totalCount) {
  const countEl = document.getElementById("movies-count-info");
  const paginationEl = document.getElementById("movies-pagination");

  if (countEl) countEl.innerText = `Showing page ${page} of ${totalPages} (${totalCount.toLocaleString()} total matching titles)`;
  if (!paginationEl) return;

  paginationEl.innerHTML = `
    <button class="btn btn-secondary" style="height:32px; padding:4px 12px;" ${page <= 1 ? "disabled" : ""} onclick="changePage(${page - 1})">Previous</button>
    <span style="font-size:0.85rem; color:#94A3B8; align-self:center;">Page ${page} / ${totalPages}</span>
    <button class="btn btn-secondary" style="height:32px; padding:4px 12px;" ${page >= totalPages ? "disabled" : ""} onclick="changePage(${page + 1})">Next</button>
  `;
}

function changePage(newPage) {
  const queryString = App ? App.buildQueryString() : "";
  loadMovies(queryString, newPage);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function openMovieDetail(showId) {
  try {
    const res = await fetch(`/api/movie/${showId}`);
    const json = await res.json();
    if (json.status === "success" && json.data) {
      const m = json.data;
      const modal = document.getElementById("movie-modal");
      const modalBody = document.getElementById("modal-body-content");

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

        <div style="background:#0F172A; border-radius:8px; padding:14px; margin-bottom:16px; border:1px solid #334155;">
          <h4 style="font-size:0.85rem; text-transform:uppercase; color:#94A3B8; margin-bottom:6px;">Plot Synopsis</h4>
          <p style="font-size:0.92rem; color:#E2E8F0; line-height:1.5;">${m.description}</p>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:0.85rem;">
          <div>
            <span style="color:#94A3B8;">🎭 Genres:</span><br>
            <strong style="color:#fff;">${m.listed_in}</strong>
          </div>
          <div>
            <span style="color:#94A3B8;">🌍 Production Country:</span><br>
            <strong style="color:#fff;">${m.country}</strong>
          </div>
          <div>
            <span style="color:#94A3B8;">🎬 Director:</span><br>
            <strong style="color:#fff;">${m.director}</strong>
          </div>
          <div>
            <span style="color:#94A3B8;">👥 Cast:</span><br>
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

document.addEventListener("DOMContentLoaded", () => {
  loadMovies();
  document.addEventListener("filtersChanged", (e) => loadMovies(e.detail.queryString, 1));
});
