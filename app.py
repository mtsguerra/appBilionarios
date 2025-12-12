import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
app = Flask(__name__)

# Configure logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Billionaires app startup')

from views import *

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    app.logger.warning(f'Page not found: {error}')
    return render_template('erro.html', message='Page not found. The requested page does not exist.'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    app.logger.error(f'Internal server error: {error}')
    return render_template('erro.html', message='Internal server error. Please try again later.'), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle general exceptions."""
    app.logger.error(f'Unhandled exception: {error}', exc_info=True)
    return render_template('erro.html', message='An unexpected error occurred. Please try again later.'), 500

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    # Only activate debug mode if explicitly defined via environment variable
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
