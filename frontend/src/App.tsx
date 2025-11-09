import { useState } from 'react'
import SearchForm from './components/search-form';
import Results from './components/search-results';
import Footer from './components/footer';
import './index.css'

function App() {
  const [jobs, setJobs] = useState([]);

  const handleResults = (data: any) => setJobs(data);

  return (
    <div className="app-container">
      <div className="app-content">
        <div className="app-wrapper">
          <h1 className="app-title">Job Board Scraper</h1>
          <SearchForm onResults={handleResults} />
          <Results jobs={jobs} />
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default App
