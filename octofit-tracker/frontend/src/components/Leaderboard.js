import React, { useEffect, useState } from 'react';
import { getApiUrl } from '../utils/api';

const Leaderboard = () => {
  const [leaderboards, setLeaderboards] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = getApiUrl('leaderboards/');
    
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
        setLoading(false);
        setError(null);
      })
      .catch(err => {
        console.error('Error fetching leaderboards:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="card mb-4">
      <div className="card-header bg-success text-white">
        <h2 className="card-title">Leaderboard</h2>
      </div>
      <div className="card-body">
        {loading && (
          <div className="alert alert-info">Loading leaderboard...</div>
        )}
        {error && (
          <div className="alert alert-danger">
            <strong>Error:</strong> Failed to load leaderboard. {error}
          </div>
        )}
        {!loading && !error && (
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
