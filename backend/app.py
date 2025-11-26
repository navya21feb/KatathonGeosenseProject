"""
GeoSense Flask Application
Main entry point for the backend API
"""

from flask import Flask
from flask_cors import CORS
from config import Config
from database.db import init_db, db

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from routes.insights import insights_bp
    from routes.reports import reports_bp
    from routes.routing import routing_bp
    
    app.register_blueprint(insights_bp, url_prefix='/api/insights')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(routing_bp, url_prefix='/api/routing')
    
    @app.route('/api/health')
    def health():
        return {'status': 'healthy', 'service': 'GeoSense API'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

