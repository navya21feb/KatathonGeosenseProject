# GeoSense: Area Insights from Movement and Traffic Data

GeoSense is a comprehensive platform that analyzes location-based data such as POIs, routes, traffic, and mobility patterns to generate insights about urban areas. The solution reveals patterns like "busiest between 6–8 PM" or "quiet zones for evening walks" with interactive dashboards, heatmaps, and predictive analytics.

## Key Features

- **Route Comparison**: Show 3 routes - fastest, cheapest, eco-friendly
- **Report Generation**: Generate reports for government, researchers, and civil engineers
- **Interactive Dashboards**: Real-time traffic insights with heatmaps
- **Predictive Analytics**: ML-powered traffic predictions
- **Busiest Hours Analysis**: Charts showing peak traffic times

## Tech Stack

- **Frontend**: React with Vite
- **Backend**: Python Flask
- **Database**: MongoDB
- **ML**: Python (scikit-learn, pandas)

## Project Structure

```
geosense-project/
├── backend/          # Flask backend API
├── frontend/         # React frontend
├── ml_models/        # ML models and training
├── data/             # Raw and processed data
├── scripts/          # Automation scripts
└── docs/             # Documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 4.4+

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

See `.env.example` files in backend and frontend directories for required environment variables.

## License

MIT

