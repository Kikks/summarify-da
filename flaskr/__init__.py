import os
import openai
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

openai.api_key = os.getenv("OPENAI_API_KEY")

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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text."
                    },
                    {
                    "role": "user",
                    "content": text
                    }
                    ],
                temperature=1,
                max_tokens=300,
                top_p=1,
                frequency_penalty=2,
                presence_penalty=2
                )

            return jsonify(
                {
                    "success": True,
                    "message": "Summary generated successfully.",
                    "data": {
                        # TODO: Return the summary
                        "summary": response['choices'][0]['message']['content'],
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

            # TODO: Pass the text and query variables to the model and return the answer
            prompt = f"You are a helpful assistant that answers questions based on the words from the text below.\nText: \"\"\"\n{text}\n\"\"\""
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": prompt
                    },
                    {
                    "role": "user",
                    "content": query
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )

            return jsonify(
                {
                    "success": True,
                    "message": "Text queried successfully.",
                    "data": {
                        # TODO: Return the answer to the query
                        "reply": response['choices'][0]['message']['content'],
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
