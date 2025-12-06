from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database connection handling
    from . import db
    db.init_app(app)
    
    # Register blueprints
    from .routes import buildings_bp, inspections_bp, interventions_bp, dashboard_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(buildings_bp)
    app.register_blueprint(inspections_bp)
    app.register_blueprint(interventions_bp)
    
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

    return app