from flask import Flask, render_template
from flask_cors import CORS
import os

def create_flask_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    CORS(app, resources={
        r"/*": {
            "origins": "*"
        }
    })

    @app.route("/")
    def home():
        return render_template("index.html")
    
    return app