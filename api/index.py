import sys
import os

# Ensure root directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# WSGI Middleware to normalize PATH_INFO from Vercel serverless rewrite
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        for prefix in ('/api/index.py', '/api/index'):
            if path.startswith(prefix):
                path = path[len(prefix):] or '/'
                break
        environ['PATH_INFO'] = path
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)
