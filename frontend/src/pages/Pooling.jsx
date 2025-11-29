import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import { Search, IndianRupee,MapPin, Shield, Calendar, Car, Clock, Leaf } from 'lucide-react'
import DriverRegistration from '../components/DriverRegistration'
import './Pooling.css'

const Pooling = () => {
  const navigate = useNavigate()
  const { isAuthenticated, getAuthHeader } = useAuth()
  const [from, setFrom] = useState('')
  const [to, setTo] = useState('')
  const [date, setDate] = useState('')
  const [searchResult, setSearchResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showDriverModal, setShowDriverModal] = useState(false)

  const handleSearchRides = async (e) => {
    e.preventDefault()
    
    if (!isAuthenticated) {
      navigate('/signin')
      return
    }

    setLoading(true)
    setSearchResult(null)

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Mock response - no rides found
      setSearchResult({
        success: true,
        message: 'Sorry no vehicle poolers for this path',
        route_options: {
          fastest_route: {
            name: 'Fastest Route',
            description: 'Uses real-time traffic analysis to get you there quickly',
            duration: '2 hours 15 mins',
            distance: '145 km',
            traffic_conditions: 'Moderate traffic expected',
            advantages: ['Quickest arrival', 'Real-time traffic updates']
          },
          cheapest_route: {
            name: 'Cheapest Route',
            description: 'Optimized for fuel and toll costs to save you money',
            duration: '2 hours 45 mins',
            distance: '138 km',
            cost_savings: 'Save ~₹250 compared to fastest route',
            advantages: ['Lowest cost', 'Fuel efficient']
          },
          eco_friendly_route: {
            name: 'Eco-Friendly Route',
            description: 'Designed to reduce carbon emissions and environmental impact',
            duration: '2 hours 30 mins',
            distance: '142 km',
            carbon_reduction: '15% less emissions',
            advantages: ['Environmentally friendly', 'Scenic routes']
          }
        }
      })
    } catch (err) {
      setSearchResult({
        success: false,
        message: 'Failed to search rides. Please try again.'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleRegisterDriver = () => {
    if (!isAuthenticated) {
      navigate('/signin')
      return
    }
    setShowDriverModal(true)
  }

  const handleDriverRegistrationSuccess = () => {
    setShowDriverModal(false)
    // You can show a success toast or message here
  }

  const RouteOptionCard = ({ route, icon: Icon, color }) => (
    <motion.div 
      className="route-option-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="route-header">
        <Icon size={24} className="route-icon" style={{ color }} />
        <h3>{route.name}</h3>
      </div>
      <p className="route-description">{route.description}</p>
      <div className="route-details">
        <div className="detail-item">
          <Clock size={16} />
          <span>{route.duration}</span>
        </div>
        <div className="detail-item">
          <MapPin size={16} />
          <span>{route.distance}</span>
        </div>
        {route.cost_savings && (
          <div className="detail-item">
            <IndianRupee size={16} />
            <span>{route.cost_savings}</span>
          </div>
        )}
        {route.carbon_reduction && (
          <div className="detail-item">
            <Leaf size={16} />
            <span>{route.carbon_reduction}</span>
          </div>
        )}
      </div>
      <div className="route-advantages">
        <h4>Advantages:</h4>
        <ul>
          {route.advantages.map((advantage, index) => (
            <li key={index}>{advantage}</li>
          ))}
        </ul>
      </div>
    </motion.div>
  )

  return (
    <div className="pooling-page">
      <div className="container">
        <motion.div
          className="pooling-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="page-title">
            <span className="title-part">Vehicle</span>{' '}
            <span className="title-part gradient">Pooling</span>
          </h1>
          <p className="page-subtitle">
            Share your ride, save money, and reduce carbon emissions
          </p>
        </motion.div>

        {/* Find Your Ride Section */}
        <motion.div
          className="find-ride-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <div className="card-header-pooling">
            <Car size={24} className="card-icon" />
            <h2>Find Your Ride</h2>
          </div>
          <p className="card-description">
            Connect with travelers heading your way
          </p>

          <form onSubmit={handleSearchRides} className="pooling-form">
            <div className="form-row-pooling">
              <div className="form-group-pooling">
                <MapPin size={18} className="input-icon" />
                <input
                  type="text"
                  value={from}
                  onChange={(e) => setFrom(e.target.value)}
                  placeholder="Your location"
                  required
                />
              </div>
              <div className="form-group-pooling">
                <MapPin size={18} className="input-icon" />
                <input
                  type="text"
                  value={to}
                  onChange={(e) => setTo(e.target.value)}
                  placeholder="Destination"
                  required
                />
              </div>
              <div className="form-group-pooling">
                <Calendar size={18} className="input-icon" />
                <input
                  type="text"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  placeholder="dd-mm-yyyy"
                  required
                />
              </div>
            </div>

            <motion.button
              type="submit"
              className="search-rides-button"
              disabled={loading}
              whileHover={{ scale: loading ? 1 : 1.02 }}
              whileTap={{ scale: loading ? 1 : 0.98 }}
            >
              <Search size={20} />
              <span>{loading ? 'Searching...' : 'Search Rides'}</span>
            </motion.button>
          </form>

          {/* Search Results */}
          {searchResult && (
            <div className="search-results">
              {searchResult.success ? (
                <>
                  <div className="no-rides-message">
                    <h3>{searchResult.message}</h3>
                    <p>But we found these great route options for your journey:</p>
                  </div>
                  
                  <div className="route-options">
                    <RouteOptionCard 
                      route={searchResult.route_options.fastest_route}
                      icon={Clock}
                      color="#2196f3"
                    />
                    <RouteOptionCard 
                      route={searchResult.route_options.cheapest_route}
                      icon={IndianRupee}
                      color="#4caf50"
                    />
                    <RouteOptionCard 
                      route={searchResult.route_options.eco_friendly_route}
                      icon={Leaf}
                      color="#ff9800"
                    />
                  </div>
                </>
              ) : (
                <div className="error-message">
                  {searchResult.message}
                </div>
              )}
            </div>
          )}
        </motion.div>

        {/* Benefits Cards */}
        <div className="benefits-cards-pooling">
          {[
            {
              icon: IndianRupee,
              title: 'Save Money',
              description: 'Split fuel costs and save up to 60% on travel expenses.',
            },
            {
              icon: MapPin,
              title: 'Live Location Tracking',
              description: 'Feel safe and relaxed with real-time live location tracking.',
            },
            {
              icon: Shield,
              title: 'Safe & Verified',
              description: 'All drivers are verified with ratings and reviews.',
            },
          ].map((benefit, index) => (
            <motion.div
              key={benefit.title}
              className="benefit-card-pooling"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
              whileHover={{ scale: 1.05, boxShadow: '0 8px 24px rgba(0,0,0,0.12)' }}
            >
              <benefit.icon size={32} className="benefit-icon-pooling" />
              <h3>{benefit.title}</h3>
              <p>{benefit.description}</p>
            </motion.div>
          ))}
        </div>

        {/* Driver Registration Section */}
        <motion.div
          className="driver-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h2>Are You a Driver?</h2>
          <p>
            Earn money by sharing your daily commute. Cover your fuel costs and meet new people!
          </p>
          <motion.button
            className="register-driver-button"
            onClick={handleRegisterDriver}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Register as Driver
          </motion.button>
        </motion.div>

        {/* Driver Registration Modal */}
        <DriverRegistration 
          isOpen={showDriverModal}
          onClose={() => setShowDriverModal(false)}
          onSuccess={handleDriverRegistrationSuccess}
        />
      </div>
    </div>
  )
}

export default Pooling