import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

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

            # TODO: Pass the text variable to the model and return the summary

            return jsonify(
                {
                    "success": True,
                    "message": "Summary generated successfully.",
                    "data": {
                        # TODO: Return the summary
                        "summary": text,
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

            # TODO: Pass the text and query variables to the model and return the answer

            return jsonify(
                {
                    "success": True,
                    "message": "Text queried successfully.",
                    "data": {
                        # TODO: Return the answer to the query
                        "reply": text,
                    },
                }
            )
        except Exception as error:
            print(error)
            abort(500)

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

    return app
