import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [leaderboards, setLeaderboards] = useState([]);
  const [error, setError] = useState(null);
  
  const apiUrl = process.env.REACT_APP_CODESPACE_NAME
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboards/`
    : 'http://localhost:8000/api/leaderboards/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log('Leaderboard API endpoint:', apiUrl);
        console.log('Fetched leaderboards:', data);
        setLeaderboards(data.results ? data.results : data);
        setError(null);
      })
      .catch(err => {
        console.error('Error fetching leaderboards:', err);
        setError(`Failed to load leaderboards: ${err.message}`);
      });
  }, [apiUrl]);

  return (
    <div className="card mb-4">
      <div className="card-header bg-success text-white">
        <h2 className="card-title">Leaderboard</h2>
      </div>
      <div className="card-body">
        {error ? (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        ) : (
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Team</th>
                <th>Points</th>
              </tr>
            </thead>
            <tbody>
              {leaderboards.map(lb => (
                <tr key={lb.id}>
                  <td>{lb.team?.name || 'Unknown Team'}</td>
                  <td>{lb.points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Leaderboard;
