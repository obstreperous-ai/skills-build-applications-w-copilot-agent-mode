import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const apiUrl = process.env.REACT_APP_CODESPACE_NAME
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`
    : 'http://localhost:8000/api/activities/';

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
        console.log('Activities API endpoint:', apiUrl);
        console.log('Fetched activities:', data);
        setActivities(data.results ? data.results : data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching activities:', err);
        setError(err.message);
        setLoading(false);
      });
  }, [apiUrl]);

  return (
    <div className="card mb-4">
      <div className="card-header bg-primary text-white">
        <h2 className="card-title">Activities</h2>
      </div>
      <div className="card-body">
        {loading && <div className="alert alert-info">Loading activities...</div>}
        {error && <div className="alert alert-danger">Error loading activities: {error}</div>}
        {!loading && !error && (
          <table className="table table-striped">
            <thead>
              <tr>
                <th>Type</th>
                <th>Duration (min)</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {activities.map(activity => (
                <tr key={activity.id}>
                  <td>{activity.type}</td>
                  <td>{activity.duration}</td>
                  <td>{activity.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Activities;
