import React from 'react'
import { motion } from 'framer-motion'
import MapComponent from '../components/MapComponent'
import BusiestHoursChart from '../components/BusiestHoursChart'
import './Dashboard.css'

const Dashboard = () => {
  return (
    <motion.div
      className="dashboard"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1>GeoSense Dashboard</h1>
      <p className="subtitle">Area Insights from Movement and Traffic Data</p>
      
      <div className="dashboard-grid">
        <div className="dashboard-card map-card">
          <h2>Traffic Heatmap</h2>
          <MapComponent />
        </div>
        
        <div className="dashboard-card">
          <BusiestHoursChart />
        </div>
      </div>
    </motion.div>
  )
}

export default Dashboard

