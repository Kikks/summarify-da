import os
import requests
from dotenv import load_dotenv

load_dotenv()

from utils.openai_chat import generate_summary

api_server_url = os.getenv("API_SERVER_URL")


def summarize_and_update_document(params):
    user_id = params["user_id"]
    document_id = params["document_id"]
    text = params["text"]

    try:
        print(f"Summarizing document {document_id} for user {user_id}")
        summary = generate_summary(text)

        response = requests.post(
            f"{api_server_url}/documents/summary/webook/complete",
            json={"summary": summary, "userId": user_id, "documentId": document_id},
        )

    except Exception as error:
        print(error)

        try:
            response = requests.post(
                f"{api_server_url}/documents/summary/webhook/failed",
                json={"userId": user_id, "documentId": document_id},
            )
        except Exception as error:
            print(error)
