import { useState } from "react";
import type { FormEvent } from "react";
import axios from "axios";

interface SearchFormProps {
  onResults: (data: any) => void;
}

function SearchForm({ onResults }: SearchFormProps) {
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/scrape`, {
        params: { search, location },
      });
      // API returns {count: number, jobs: array}, extract the jobs array
      const jobs = res.data?.jobs || res.data || [];
      onResults(Array.isArray(jobs) ? jobs : []);
    } catch (err) {
      console.error(err);
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || err.response?.data?.error || err.message || "Failed to fetch jobs. Please try again.");
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  // SVG Icons
  const SearchIcon = () => (
    <svg
      className="search-icon"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
      />
    </svg>
  );

  const LocationIcon = () => (
    <svg
      className="location-icon"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
      />
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
      />
    </svg>
  );

  const LoadingSpinner = () => (
    <svg
      className="loading-spinner"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="loading-spinner-circle"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="loading-spinner-path"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  );

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="search-form-container">
        {/* Error Message */}
        {error && (
          <div className="error-container">
            <svg
              className="error-icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div className="error-content">
              <p className="error-title">Error</p>
              <p className="error-message">{error}</p>
            </div>
            <button
              type="button"
              onClick={() => setError(null)}
              className="error-close-button"
              aria-label="Dismiss error"
            >
              <svg
                className="error-close-icon"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        )}

        {/* Search Input */}
        <div className="search-input-wrapper">
          <div className="search-input-icon-container">
            <SearchIcon />
          </div>
          <input
            type="text"
            placeholder="Job title, skills, or keywords"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
            required
            disabled={loading}
          />
        </div>

        {/* Location Input */}
        <div className="search-input-wrapper">
          <div className="search-input-icon-container">
            <LocationIcon />
          </div>
          <input
            type="text"
            placeholder="City, province, or remote"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="search-input"
            required
            disabled={loading}
          />
        </div>

        {/* Submit Button */}
        <button type="submit" disabled={loading} className="submit-button">
          {loading ? (
            <>
              <LoadingSpinner />
              <span>Searching jobs...</span>
            </>
          ) : (
            <>
              <svg
                className="submit-button-icon"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
              <span>Search Jobs</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
}

export default SearchForm;
