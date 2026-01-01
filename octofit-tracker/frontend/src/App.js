function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <img src={require('./octofitapp-small.png')} alt="OctoFit Logo" className="App-logo" />
          <span className="navbar-brand">OctoFit Tracker</span>
        </header>
        <div className="container">
          <nav className="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item"><Link className="nav-link text-white" to="/activities">Activities</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/leaderboard">Leaderboard</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/teams">Teams</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/users">Users</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/workouts">Workouts</Link></li>
              </ul>
            </div>
          </nav>
          <div className="mb-4">
            <h1 className="display-4 text-center text-primary">Welcome to OctoFit Tracker</h1>
          </div>
          <Routes>
            <Route path="/activities" element={<Activities />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/users" element={<Users />} />
            <Route path="/workouts" element={<Workouts />} />
            <Route path="/" element={<Activities />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
