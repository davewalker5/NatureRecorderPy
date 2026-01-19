import os
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .home import home_bp
from .sightings import sightings_bp
from .export import export_bp
from .locations import locations_bp
from .categories import categories_bp
from .species import species_bp
from .status import status_bp
from .species_ratings import species_ratings_bp
from .jobs import jobs_bp
from .auth import auth_bp, unauthorised, has_roles
from naturerec_model.logic import get_user


csrf = CSRFProtect()


def create_app(environment="production"):
    """
    Flask Application Factory

    :return: An instance of the Flask application
    """
    app = Flask("Nature Recorder",
                static_folder=os.path.join(os.path.dirname(__file__), "static"),
                template_folder=os.path.join(os.path.dirname(__file__), "templates"))

    config_object = f"naturerec_web.config.{'ProductionConfig' if environment == 'production' else 'DevelopmentConfig'}"
    app.config.from_object(config_object)
    app.config.update(
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_HTTPONLY=True,
        PERMANENT_SESSION_LIFETIME=600
    )

    # Register the blueprints
    app.secret_key = os.environ["SECRET_KEY"]
    app.register_blueprint(home_bp, url_prefix="")
    app.register_blueprint(sightings_bp, url_prefix='/sightings')
    app.register_blueprint(export_bp, url_prefix='/export')
    app.register_blueprint(locations_bp, url_prefix='/locations')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(species_bp, url_prefix='/species')
    app.register_blueprint(status_bp, url_prefix='/status')
    app.register_blueprint(species_ratings_bp, url_prefix='/species_ratings')
    app.register_blueprint(jobs_bp, url_prefix='/jobs')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Register the 401 Unathorised error handler
    app.register_error_handler(401, unauthorised)

    # Create the flask-login user manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Enable CSRF protection
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Method that returns a user given their ID

        :param user_id: ID of the user to retrieve
        :return: Instance of the User class for the specified user
        """
        return get_user(int(user_id))

    @app.context_processor
    def inject_roles():
        """
        Make role membership available to all templates to allow the layout view to configure the menu
        bar based on those permissions
        """
        is_admin = has_roles(["Administrator"])
        is_reporter = has_roles(["Reporter"])
        return dict(is_admin=is_admin, is_reporter=is_reporter)

    @app.after_request
    def add_security_headers(response):
        """
        Enforce security-related response headers

        :param response: Response object
        :return: Response object with headers set
        """
        # response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; form-action 'self'"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    return app


