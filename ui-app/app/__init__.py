from flask import Flask
from config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize database connection handling
    from . import db
    db.init_app(app)
    
    # Register blueprints
    from .routes import (buildings_bp, inspections_bp, interventions_bp, 
                         dashboard_bp, prestataires_bp, zones_bp,
                         protections_bp, proprietaires_bp, types_bp, documents_bp)
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(buildings_bp)
    app.register_blueprint(inspections_bp)
    app.register_blueprint(interventions_bp)
    app.register_blueprint(prestataires_bp)
    app.register_blueprint(zones_bp)
    app.register_blueprint(protections_bp)
    app.register_blueprint(proprietaires_bp)
    app.register_blueprint(types_bp)
    app.register_blueprint(documents_bp)
    
    @app.route('/test-db')
    def test_db_connection():
        try:
            conn = db.get_db()
            cur = conn.cursor()
            cur.execute('SELECT version();')
            db_version = cur.fetchone()
            cur.close()
            return f"<h1>Database Connection Successful!</h1><p>PostgreSQL version: {db_version[0]}</p>"
        except Exception as e:
            return f"<h1>Database Connection Failed!</h1><p>{e}</p>"

    # Custom Jinja filter for safe date formatting
    @app.template_filter('safe_strftime')
    def safe_strftime(value, format='%d/%m/%Y'):
        """Safely format dates that might be strings or date objects."""
        if value is None:
            return 'N/A'
        if isinstance(value, str):
            return value
        try:
            return value.strftime(format)
        except:
            return str(value)
    
    return app