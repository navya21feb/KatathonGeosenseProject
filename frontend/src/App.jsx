import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { GeoProvider } from './context/GeoContext'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import InsightsPage from './pages/InsightsPage'
import RoutesPage from './pages/RoutesPage'
import ReportsPage from './pages/ReportsPage'
import './App.css'

function App() {
  return (
    <GeoProvider>
      <Router>
        <div className="App">
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/insights" element={<InsightsPage />} />
              <Route path="/routes" element={<RoutesPage />} />
              <Route path="/reports" element={<ReportsPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </GeoProvider>
  )
}

export default App

