/**
 * MongoDB Aggregation Queries & Pipelines
 * Database: netflix_analytics
 * Collection: movies
 * 
 * Usage:
 * mongosh "mongodb+srv://..." mongodb/aggregation_queries.js
 */

// Connect / Switch to Database
use('netflix_analytics');

// ==========================================================
// 1. Genre Popularity Aggregation Pipeline
// Unwinds 'genres' array and counts occurrences per genre
// ==========================================================
print("\n--- 1. Genre Aggregation ---");
db.movies.aggregate([
  { $unwind: "$genres" },
  {
    $group: {
      _id: "$genres",
      total_count: { $sum: 1 },
      movie_count: { $sum: { $cond: [{ $eq: ["$type", "Movie"] }, 1, 0] } },
      tv_show_count: { $sum: { $cond: [{ $eq: ["$type", "TV Show"] }, 1, 0] } },
      avg_rating_score: { $avg: "$rating_score" }
    }
  },
  { $sort: { total_count: -1 } },
  { $limit: 15 },
  {
    $project: {
      genre: "$_id",
      total_count: 1,
      movie_count: 1,
      tv_show_count: 1,
      avg_rating_score: { $round: ["$avg_rating_score", 2] },
      _id: 0
    }
  }
]);

// ==========================================================
// 2. Content Growth & Release Trend Aggregation
// Groups by release_year and type
// ==========================================================
print("\n--- 2. Release Trend Aggregation ---");
db.movies.aggregate([
  {
    $group: {
      _id: "$release_year",
      total_releases: { $sum: 1 },
      movies: { $sum: { $cond: [{ $eq: ["$type", "Movie"] }, 1, 0] } },
      tv_shows: { $sum: { $cond: [{ $eq: ["$type", "TV Show"] }, 1, 0] } }
    }
  },
  { $sort: { _id: 1 } },
  {
    $project: {
      year: "$_id",
      total_releases: 1,
      movies: 1,
      tv_shows: 1,
      _id: 0
    }
  }
]);

// ==========================================================
// 3. Country-Wise Content Distribution
// Unwinds 'country' array and counts productions per country
// ==========================================================
print("\n--- 3. Country Aggregation ---");
db.movies.aggregate([
  { $unwind: "$country" },
  { $match: { country: { $ne: "Unknown" } } },
  {
    $group: {
      _id: "$country",
      total_productions: { $sum: 1 },
      movies: { $sum: { $cond: [{ $eq: ["$type", "Movie"] }, 1, 0] } },
      tv_shows: { $sum: { $cond: [{ $eq: ["$type", "TV Show"] }, 1, 0] } }
    }
  },
  { $sort: { total_productions: -1 } },
  { $limit: 12 },
  {
    $project: {
      country: "$_id",
      total_productions: 1,
      movies: 1,
      tv_shows: 1,
      _id: 0
    }
  }
]);

// ==========================================================
// 4. Rating Distribution & Classification
// ==========================================================
print("\n--- 4. Rating Aggregation ---");
db.movies.aggregate([
  {
    $group: {
      _id: "$rating",
      count: { $sum: 1 },
      movies: { $sum: { $cond: [{ $eq: ["$type", "Movie"] }, 1, 0] } },
      tv_shows: { $sum: { $cond: [{ $eq: ["$type", "TV Show"] }, 1, 0] } }
    }
  },
  { $sort: { count: -1 } },
  {
    $project: {
      rating: "$_id",
      count: 1,
      movies: 1,
      tv_shows: 1,
      _id: 0
    }
  }
]);

// ==========================================================
// 5. Top-Rated Movie Catalog
// ==========================================================
print("\n--- 5. Top-Rated Titles ---");
db.movies.find(
  { type: "Movie" },
  { title: 1, release_year: 1, rating: 1, rating_score: 1, primary_genre: 1, primary_country: 1, duration: 1, _id: 0 }
).sort({ rating_score: -1, release_year: -1 }).limit(10);
