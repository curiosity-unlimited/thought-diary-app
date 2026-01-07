"""Main application entry point.

This module creates the Flask application instance and runs the development server.
For production, use a WSGI server like Gunicorn instead.
"""

import os
from dotenv import load_dotenv

from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create Flask application instance
app = create_app()


if __name__ == "__main__":
    """Run the Flask development server.
    
    This should only be used for development. For production,
    use a production-ready WSGI server like Gunicorn:
    
        gunicorn -w 4 -b 0.0.0.0:5000 main:app
    """
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
