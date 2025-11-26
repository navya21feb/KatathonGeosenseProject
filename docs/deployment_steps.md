# Deployment Steps

## Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB 4.4+

## Backend Deployment

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run migrations (if using):
```bash
# TODO: Add migration commands
```

4. Start the server:
```bash
# Development
python app.py

# Production (using Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## Frontend Deployment

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URLs
```

3. Build for production:
```bash
npm run build
```

4. Serve the build:
```bash
# Using a static file server or serve package
npx serve -s dist
```

## MongoDB Setup

1. Install MongoDB
2. Start MongoDB service
3. Create database: `geosense`
4. Update `MONGODB_URI` in backend `.env`

## Production Considerations

- Use environment variables for all secrets
- Set up proper CORS origins
- Use HTTPS in production
- Set up monitoring and logging
- Configure rate limiting
- Set up database backups

