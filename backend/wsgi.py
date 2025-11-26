"""
WSGI entry point for production deployment
Used by Gunicorn or other WSGI servers
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

