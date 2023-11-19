import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_summary(text):
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

    print("Summary completed!!")

    return response["choices"][0]["message"]["content"]


def query_document(text, query):
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

    return response["choices"][0]["message"]["content"]
