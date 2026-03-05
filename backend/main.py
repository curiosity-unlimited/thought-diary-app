"""Main application entry point.

This module creates the Flask application instance and runs the development server.
For production, use a WSGI server like Gunicorn instead.
"""

import os
import click
from dotenv import load_dotenv

from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create Flask application instance
app = create_app()


@app.cli.command('seed')
@click.option('--clear', is_flag=True, help='Clear existing data before seeding')
def seed_command(clear: bool) -> None:
    """Populate the database with sample data for development.
    
    Args:
        clear: If True, clears all existing data before seeding.
    
    Example:
        flask seed
        flask seed --clear
    """
    from app.utils.seed import seed_all
    
    try:
        seed_all(clear_existing=clear)
        click.echo(click.style('✓ Database seeding completed successfully!', fg='green'))
    except Exception as e:
        click.echo(click.style(f'✗ Error seeding database: {str(e)}', fg='red'))
        raise


if __name__ == "__main__":
    """Run the Flask development server.
    
    This should only be used for development. For production,
    use a production-ready WSGI server like Gunicorn:
    
        gunicorn -w 4 -b 0.0.0.0:5000 main:app
    """
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
