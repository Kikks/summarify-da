# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Run the Server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

After that is done, the server should run on [localhost://5000](http://localhost://5000)

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

Below is the documentation for every endpoint exposed by the server.

# `POST '/summarize'`

- Request Arguments:

```json
{
	"text": "...this is the body of text to be summarized"
}
```

- Returns: An object with a success boolean value, a corresponding message, a `data` dictionary, that contains the `summary` of the body of text.

```json
{
    "success": True,
    "message": "Summary generated successfully.",
    "data": {
      "summary": "...this is the summary of the body of text supplied."
    },
}
```

# `POST '/query-text'`

- Request Arguments:

```json
{
	"text": "...this is the body of text to be questioned.",
	"query": "...this is the query string that will be used to ask questions about the body of text supplied."
}
```

- Returns: An object with a success boolean value, a corresponding message, a `data` dictionary, that contains the `reply` to the query.

```json
{
    "success": True,
    "message": "Text queried successfully.",
    "data": {
      "reply": "...this is the reply to the query."
    },
}
```
