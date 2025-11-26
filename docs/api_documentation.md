# GeoSense API Documentation

## Base URL
`http://localhost:5000/api`

## Endpoints

### Health Check
- **GET** `/api/health`
- Returns API health status

### Insights

#### Get Traffic Insights
- **GET** `/api/insights/traffic`
- Parameters: `lat`, `lon`, `radius` (optional)

#### Get Busiest Hours
- **GET** `/api/insights/busiest-hours`
- Parameters: `lat`, `lon`

#### POI Analysis
- **GET** `/api/insights/poi-analysis`
- Parameters: `lat`, `lon`, `radius`

### Routes

#### Compare Routes
- **POST** `/api/routing/compare`
- Body: `{ "origin": { "lat": float, "lon": float }, "destination": { "lat": float, "lon": float } }`

#### Fastest Route
- **POST** `/api/routing/fastest`
- Body: `{ "origin": {...}, "destination": {...} }`

### Reports

#### Generate Report
- **POST** `/api/reports/generate`
- Body: `{ "report_type": string, "stakeholder_type": string, "format": "pdf" | "csv" }`

