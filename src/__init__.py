import os
from flask import Flask


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    from src.routes import bp
    app.register_blueprint(bp)

    return app
