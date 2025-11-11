from flask import Flask
from flask_cors import CORS

def create_flask_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    CORS(app)

    from app.routes import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    
    return app