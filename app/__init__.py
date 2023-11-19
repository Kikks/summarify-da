import os
import redis

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from rq import Worker, Queue, Connection

from utils.extractor import extract_file
from utils.openai_chat import generate_summary, query_document
from utils.jobs import summarize_and_update_document
from worker import conn

# Start Configurations
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt", "csv", "doc", "docx"}
# End Configurations


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    CORS(app)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    queue = Queue(connection=conn)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # Start of Routes
    @app.route("/summarize", methods=["POST"])
    def summarize_text():
        try:
            body = request.get_json()
            text = body.get("text", None)

            if not text:
                return (
                    jsonify(
                        {
                            "success": False,
                            "status": 422,
                            "message": "Unprocessable. Please provide a text to summarize",
                        }
                    ),
                    422,
                )

            summary = generate_summary(text)

            return jsonify(
                {
                    "success": True,
                    "message": "Summary generated successfully.",
                    "data": {
                        "summary": summary,
                    },
                }
            )
        except Exception as error:
            print(error)
            abort(500)

    @app.route("/query-text", methods=["POST"])
    def query_text():
        try:
            body = request.get_json()
            text = body.get("text", None)
            query = body.get("query", None)

            if not text or not query:
                return (
                    jsonify(
                        {
                            "success": False,
                            "status": 422,
                            "message": "Unprocessable. Please provide a text and a query.",
                        }
                    ),
                    422,
                )

            reply = query_document(text, query)

            return jsonify(
                {
                    "success": True,
                    "message": "Text queried successfully.",
                    "data": {"reply": reply},
                }
            )
        except Exception as error:
            print(error)
            abort(500)

    @app.route("/summarize-job", methods=["POST"])
    def create_summary_job():
        body = request.get_json()
        document_id = body.get("documentId", None)
        text = body.get("text", None)
        user_id = body.get("userId", None)

        if not text or not document_id or not user_id:
            return (
                jsonify(
                    {
                        "success": False,
                        "status": 422,
                        "message": "Unprocessable. Please provide a text, a document ID and a user ID.",
                    }
                ),
                422,
            )

        try:
            queue.enqueue(
                summarize_and_update_document,
                {"document_id": document_id, "text": text, "user_id": user_id},
            )
            return jsonify(
                {
                    "success": True,
                    "message": "Summary generated successfully.",
                    "data": {
                        "queued": True,
                    },
                }
            )
        except Exception as error:
            print(error)
            abort(500)

    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

            try:
                file.save(file_path)
                text = extract_file(file.filename, file_path)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                os.remove(file_path)

            return jsonify({"text": text}), 200

        return (
            jsonify(
                {"success": False, "status": 422, "message": "File format not allowed."}
            ),
            422,
        )

    # End of Routes

    # Start of Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "status": 404, "message": "Not found."}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "status": 400, "message": "Bad Request."}),
            400,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "status": 500, "message": "Server error."}),
            500,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "status": 422, "message": "Unprocessable."}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {"success": False, "status": 405, "message": "Method not allowed."}
            ),
            405,
        )

    # End of Error Handlers

    return app
