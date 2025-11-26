# GeoSense Project Structure

```
geosense-project/
│
├── backend/                               # PYTHON + FLASK BACKEND
│   ├── app.py                             # Main Flask app / entry point
│   ├── config.py                          # Loads environment variables
│   ├── requirements.txt                   # Flask + ML dependencies
│   ├── wsgi.py                            # For production servers (Gunicorn)
│   ├── env.example                        # Environment variables template
│   │
│   ├── routes/                            # API Endpoints
│   │   ├── insights.py                    # Traffic insights API
│   │   ├── reports.py                     # PDF/CSV report generation
│   │   └── routing.py                     # Fastest / Cheapest / Eco route
│   │
│   ├── services/                          # Business logic
│   │   ├── data_processor.py             # Aggregation + analytics
│   │   ├── traffic_api.py                 # External traffic API (ex: TomTom)
│   │   ├── routing_engine.py             # Routing logic
│   │   ├── ml_predictor.py               # ML models for prediction
│   │   └── report_generator.py           # Report generation service
│   │
│   ├── models/                            # Database + ORM
│   │   └── models.py                      # MongoEngine models
│   │
│   ├── database/                          
│   │   ├── db.py                          # MongoDB initialization
│   │   └── migrations/                    # Alembic migration files
│   │
│   ├── utils/
│   │   ├── helpers.py                     # Common helper utilities
│   │   └── validators.py                  # Input validation
│   │
│   └── tests/                             # Backend unit tests
│       ├── test_insights.py
│       ├── test_routes.py
│       └── test_ml.py
│
│
├── ml_models/                             # ML Models & Training Notebooks
│   ├── notebooks/                         # Jupyter notebooks
│   │   └── traffic_prediction.ipynb
│   ├── saved_models/                      # .pkl / .joblib models
│   ├── preprocessing/                     # Data cleaning scripts
│   │   └── preprocess.py
│   └── training/                          # Training pipeline
│       └── train_model.py
│
│
├── data/                                  # Raw / processed datasets
│   ├── raw/
│   └── processed/
│
│
├── scripts/                               # Automation + cron jobs
│   └── collect_traffic_data.py            # Data scraper / API collector
│
│
├── frontend/                              # REACT FRONTEND
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── env.example
│   │
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── main.jsx
│       ├── index.css
│       │
│       ├── components/
│       │   ├── MapComponent.jsx           # Interactive map component
│       │   ├── MapComponent.css
│       │   ├── HeatmapLayer.jsx           # Traffic heatmap layer
│       │   ├── BusiestHoursChart.jsx      # Busiest hours visualization
│       │   ├── BusiestHoursChart.css
│       │   ├── RouteComparisonCard.jsx    # Route comparison UI
│       │   ├── RouteComparisonCard.css
│       │   ├── Navbar.jsx                 # Navigation bar
│       │   └── Navbar.css
│       │
│       ├── pages/
│       │   ├── Dashboard.jsx              # Main dashboard page
│       │   ├── Dashboard.css
│       │   ├── InsightsPage.jsx           # Traffic insights page
│       │   ├── InsightsPage.css
│       │   ├── RoutesPage.jsx             # Route comparison page
│       │   ├── RoutesPage.css
│       │   ├── ReportsPage.jsx            # Report generation page
│       │   └── ReportsPage.css
│       │
│       ├── context/
│       │   └── GeoContext.jsx             # React context for geo data
│       │
│       ├── hooks/
│       │   └── useTrafficData.js           # Custom hook for traffic data
│       │
│       ├── utils/
│       │   └── api.js                     # API client utilities
│       │
│       └── assets/                        # Images / Icons
│
│
├── docs/                                  # Documentation
│   ├── api_documentation.md
│   ├── deployment_steps.md
│   ├── requirements_specification.md
│   └── system_design.md
│
│
├── README.md                              # Main project documentation
├── PROJECT_STRUCTURE.md                   # This file
└── .gitignore                            # Git ignore rules
```

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
cp env.example .env
# Edit .env with your API URLs
npm run dev
```

### MongoDB Setup
1. Install and start MongoDB
2. Update `MONGODB_URI` in `backend/.env`

## Key Features Implemented

✅ Complete folder structure
✅ React frontend with Vite
✅ Flask backend with MongoDB
✅ Route comparison (fastest, cheapest, eco-friendly)
✅ Report generation endpoints
✅ Interactive maps with Leaflet
✅ Busiest hours charts with Recharts
✅ Modern UI with Framer Motion animations
✅ Production-ready structure (no Docker required)

## Next Steps

The structure is ready. You can now:
1. Implement the business logic in each service file
2. Connect to MongoDB and set up data models
3. Integrate external APIs (TomTom, Google Maps)
4. Train ML models for traffic prediction
5. Add authentication and authorization
6. Deploy to production

