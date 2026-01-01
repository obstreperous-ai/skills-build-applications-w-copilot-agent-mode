import React, { useEffect, useState } from 'react';
import { getApiUrl } from '../utils/api';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = getApiUrl('teams/');
    
    fetch(apiUrl)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log('Teams API endpoint:', apiUrl);
        console.log('Fetched teams:', data);
        setTeams(data.results ? data.results : data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching teams:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="card mb-4">
      <div className="card-header bg-info text-white">
        <h2 className="card-title">Teams</h2>
      </div>
      <div className="card-body">
        {loading && (
          <div className="alert alert-info">Loading teams...</div>
        )}
        {error && (
          <div className="alert alert-danger">
            <strong>Error:</strong> Failed to load teams. {error}
          </div>
        )}
        {!loading && !error && (
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {teams.map(team => (
                <tr key={team.id}>
                  <td>{team.name}</td>
                  <td>{team.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Teams;
