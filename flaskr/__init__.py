import os
import PyPDF2
import docx
import csv
import openpyxl
import openai
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

openai.api_key = os.getenv("OPENAI_API_KEY")
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "txt", "csv", "doc", "docx"}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    CORS(app)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

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
                        "content": "You are a helpful assistant that summarizes text.",
                    },
                    {"role": "user", "content": text},
                ],
                temperature=1,
                max_tokens=300,
                top_p=1,
                frequency_penalty=2,
                presence_penalty=2,
            )

            return jsonify(
                {
                    "success": True,
                    "message": "Summary generated successfully.",
                    "data": {
                        # TODO: Return the summary
                        "summary": response["choices"][0]["message"]["content"],
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
            prompt = f'You are a helpful assistant that answers questions based on the words from the text below.\nText: """\n{text}\n"""'
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": query},
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            return jsonify(
                {
                    "success": True,
                    "message": "Text queried successfully.",
                    "data": {
                        # TODO: Return the answer to the query
                        "reply": response["choices"][0]["message"]["content"],
                    },
                }
            )
        except Exception as error:
            print(error)
            abort(500)

    def allowed_file(filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
        return text

    def extract_text_from_docx(docx_path):
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text

    def extract_text_from_csv(csv_path):
        with open(csv_path, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            text = "\n".join(",".join(row) for row in csv_reader)
        return text

    def extract_text_from_txt(txt_path):
        with open(txt_path, "r", encoding="utf-8") as txt_file:
            text = txt_file.read()
        return text

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

                if file.filename.endswith(".pdf"):
                    text = extract_text_from_pdf(file_path)
                elif file.filename.endswith(".docx"):
                    text = extract_text_from_docx(file_path)
                elif file.filename.endswith(".csv"):
                    text = extract_text_from_csv(file_path)
                elif file.filename.endswith((".txt", ".log")):
                    text = extract_text_from_txt(file_path)
                else:
                    text = "Unsupported file format"
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            finally:
                os.remove(file_path)  # Delete the file after use (success or error)

            return jsonify({"text": text}), 200

        return (
            jsonify(
                {"success": False, "status": 422, "message": "File format not allowed."}
            ),
            422,
        )

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
