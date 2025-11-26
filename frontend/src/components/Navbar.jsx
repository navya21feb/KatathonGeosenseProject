import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import './Navbar.css'

const Navbar = () => {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/insights', label: 'Insights' },
    { path: '/routes', label: 'Routes' },
    { path: '/reports', label: 'Reports' }
  ]

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <motion.div
          className="navbar-logo"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Link to="/">GeoSense</Link>
        </motion.div>
        <ul className="navbar-menu">
          {navItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={location.pathname === item.path ? 'active' : ''}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  )
}

export default Navbar

