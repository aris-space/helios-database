from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    make_response,
)
from werkzeug.utils import secure_filename
from functools import wraps
import os
import datetime
import logging
import secrets

from configure_db import configure_db_main
from read_bag import read_bag_main

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)  # Generate a random 32-character hex string
UPLOAD_FOLDER = "uploads"

# Set the maximum file size to 50 GB
max_upload_size = 50 * 1024 * 1024 * 1024  # 50 GB
app.config["MAX_CONTENT_LENGTH"] = max_upload_size

# Set the username and password for HTTP Basic Authentication
USERNAME = "CHANGE_ME"
PASSWORD = "CHANGE_ME"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def check_auth(username, password):
    """Check if a username/password combination is valid."""
    return username == USERNAME and password == PASSWORD


def authenticate():
    """Send a 401 response that enables basic auth."""
    response = make_response(
        "Incorrect username or password.\n Check the wiki for login credentials",
        401,
    )
    response.headers["WWW-Authenticate"] = 'Basic realm="Login Required"'
    return response


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route("/")
@requires_auth
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
@requires_auth
def upload_file():
    """
    Handle file upload
    Checks for rosbags, config file, and comment. Returns an error if any are missing.
    Saves the uploaded data in a date annotated folder.
    """
    app.logger.info("Received request")

    if "rosbags" not in request.files:
        return jsonify({"error": "Backend: No rosbags provided"}), 400

    if "excel" not in request.files:
        return jsonify({"error": "Backend: No config file provided"}), 400

    if "comment" not in request.form:
        return jsonify({"error": "Backend: No comment provided"}), 400

    if (
        "rosbags" not in request.files
        or "excel" not in request.files
        or "comment" not in request.form
    ):
        return jsonify({"error": "Missing required fields"}), 400

    rosbags = request.files.getlist("rosbags")
    excel = request.files["excel"]
    comment = request.form["comment"]

    # Create a unique folder name based on the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    upload_subfolder = os.path.join(app.config["UPLOAD_FOLDER"], timestamp)
    upload_subfolder_rosbags = os.path.join(upload_subfolder, "rosbags")
    os.makedirs(upload_subfolder)
    os.makedirs(upload_subfolder_rosbags)

    # Save rosbags
    for file in rosbags:
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_subfolder_rosbags, filename)
        file.save(file_path)

    # Save excel file
    excel_filename = secure_filename(excel.filename)
    excel_file_path = os.path.join(upload_subfolder, excel_filename)
    excel.save(excel_file_path)

    # Save comment to a text file
    comment_text = comment.strip()
    comment_file_path = os.path.join(upload_subfolder, "comment.txt")
    with open(comment_file_path, "w") as comment_file:
        comment_file.write(comment_text)

    app.logger.info(f"Uploaded to {upload_subfolder}")

    app.logger.info("Running configure_db")
    configure_db_result = configure_db_main(
        configFilePath=excel_file_path,
        description=comment_text,
        hostip="database",
    )
    if not configure_db_result:
        # Something went wrong, send back an error
        return (
            jsonify({"message": "Failed configuring database, check logs on server."}),
            500,
        )

    app.logger.info("Running read_bags")
    read_bag_result = read_bag_main(
        bagdirectory=upload_subfolder_rosbags,
        database_hostname="database",
    )
    if not read_bag_result:
        # Something went wrong, send back an error
        return (
            jsonify({"message": "Failed reading rosbags, check logs on server."}),
            500,
        )

    app.logger.info("Everything seems to have worked! :D")
    return jsonify({"message": "Files and comment uploaded successfully."}), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413


if __name__ == "__main__":

    # Set up basic logging configuration
    logging.basicConfig(level=logging.INFO)

    # Use waitress if installed (i.e. in production)
    try:
        from waitress import serve
        serve(
            app,
            host="0.0.0.0",
            port=8000,
            max_request_body_size=50 * 1024 * 1024 * 1024,
        )

    # Fall back to debug server in dev
    except ModuleNotFoundError:
        app.run(debug=True)
