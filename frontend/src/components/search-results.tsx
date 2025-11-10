interface Job {
  title: string;
  company: string;
  location: string;
  salary?: string;
  url: string;
}

interface ResultsProps {
  jobs: Job[];
}

function Results({ jobs }: ResultsProps) {
  if (!jobs || !Array.isArray(jobs) || jobs.length === 0)
    return <p className="no-results">No results yet. Try searching!</p>;

  return (
    <div className="results-container">
      <table className="results-table">
        <thead className="results-table-header">
          <tr>
            <th className="results-table-header-cell">Title</th>
            <th className="results-table-header-cell">Company</th>
            <th className="results-table-header-cell">Location</th>
            <th className="results-table-header-cell">Salary</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job: Job, idx: number) => (
            <tr key={idx} className="results-table-row">
              <td className="results-table-cell">
                <a 
                  href={job.url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="job-link"
                >
                  {job.title}
                </a>
              </td>
              <td className="results-table-cell job-company">{job.company}</td>
              <td className="results-table-cell job-location">{job.location}</td>
              <td className="results-table-cell job-salary">{job.salary || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Results;
