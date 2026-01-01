import React, { useEffect, useState } from 'react';
import { getApiUrl } from '../utils/api';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const apiUrl = process.env.REACT_APP_CODESPACE_NAME
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`
    : 'http://localhost:8000/api/workouts/';

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(apiUrl)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log('Workouts API endpoint:', apiUrl);
        console.log('Fetched workouts:', data);
        setWorkouts(data.results ? data.results : data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="card mb-4">
      <div className="card-header bg-secondary text-white">
        <h2 className="card-title">Workouts</h2>
      </div>
      <div className="card-body">
        {loading && <div className="alert alert-info">Loading workouts...</div>}
        {error && <div className="alert alert-danger">Error loading workouts: {error}</div>}
        {!loading && !error && (
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {workouts.map(workout => (
                <tr key={workout.id}>
                  <td>{workout.name}</td>
                  <td>{workout.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Workouts;
