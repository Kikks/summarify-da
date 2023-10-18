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

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

After that is done, the server should run on [localhost://5000](http://localhost://5000)

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

Below is the documentation for every endpoint exposed by the server.

# `GET '/categories'`

- Request Arguments: None
- Returns: An object with a success boolean value, a corresponding message, a `categories` dictionary, that contains an object of `id: category_string` key: value pairs and finally, the totalnumber of categories.

```json
{
    "success": True,
    "message": "Categories fetched successfully.",
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "total_categories": 6,
}
```

# `GET '/questions'`

- Request Arguments: `page`, `search`. The search argument can be used to filter questions be a query string. The page argument indicates the page of the query to be returned (defaults to 1)
- Returns: A paginated list of unfiltered (or filtered if the search argument is included) questions, the available categories, the current category, a response message, a success boolean value and the total number of questions. (maximum of 10 questions per page)

```json
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": "All",
	"message": "Questions fetched successfully.",
	"questions": [
		{
			"answer": "Testing",
			"category": 1,
			"difficulty": 1,
			"id": 25,
			"question": "Testing"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		},
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		},
		{
			"answer": "Jackson Pollock",
			"category": 2,
			"difficulty": 2,
			"id": 19,
			"question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
		},
		{
			"answer": "One",
			"category": 2,
			"difficulty": 4,
			"id": 18,
			"question": "How many paintings did Van Gogh sell in his lifetime?"
		},
		{
			"answer": "Mona Lisa",
			"category": 2,
			"difficulty": 3,
			"id": 17,
			"question": "La Giaconda is better known as what?"
		},
		{
			"answer": "Agra",
			"category": 3,
			"difficulty": 2,
			"id": 15,
			"question": "The Taj Mahal is located in which Indian city?"
		},
		{
			"answer": "The Palace of Versailles",
			"category": 3,
			"difficulty": 3,
			"id": 14,
			"question": "In which royal palace would you find the Hall of Mirrors?"
		},
		{
			"answer": "Lake Victoria",
			"category": 3,
			"difficulty": 2,
			"id": 13,
			"question": "What is the largest lake in Africa?"
		}
	],
	"success": true,
	"total_questions": 17
}
```

# `DELETE '/questions/{question_id}'`

- Request Arguments: None
- Query Params: `question_id`. This is the id of the question to be deleted.
- Returns: An object with a success boolean value, and a corresponding message.

```json
{
	"success": true,
	"message": "Question with id: 1 deleted successfully."
}
```

# `POST '/questions`

- Request Arguments: None
- Request Body: A question string, an answer string, the difficulty of the question to be created and the category (to be gotten from the `GET /categories` endpoint)

```json
{
	"question": "This is a sample question",
	"answer": "This is the answer to the question",
	"difficulty": 1,
	"category": 1
}
```

- Returns: An object with a success boolean value, and a corresponding message.

```json
{
	"success": true,
	"message": "New question created successfully."
}
```

# `GET '/categories/{category_id}/questions'`

- Request Arguments: `page`. The page argument indicates the page of the query to be returned (defaults to 1)
- Returns: A paginated list of filtered questions based on categories (maximum of 10 questions per page), the available categories, the current category, a response message, a success boolean value and the total number of questions.

```json
{
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	},
	"current_category": "Science",
	"message": "Questions fetched successfully.",
	"questions": [
		{
			"answer": "Testing",
			"category": 1,
			"difficulty": 1,
			"id": 25,
			"question": "Testing"
		},
		{
			"answer": "Blood",
			"category": 1,
			"difficulty": 4,
			"id": 22,
			"question": "Hematology is a branch of medicine involving the study of what?"
		},
		{
			"answer": "Alexander Fleming",
			"category": 1,
			"difficulty": 3,
			"id": 21,
			"question": "Who discovered penicillin?"
		},
		{
			"answer": "The Liver",
			"category": 1,
			"difficulty": 4,
			"id": 20,
			"question": "What is the heaviest organ in the human body?"
		}
	],
	"success": true,
	"total_questions": 4
}
```

# `POST '/quizzes`

- Request Arguments: None
- Request Body: A list of questions previously answered and a quiz category dictionary which includes the id and type of the category to ask questions. Pass `{ "type": "", "id": 0 }` to get random questions from all categories.

```json
{
	"previous_questions": [25],
	"quiz_category": { "type": "Science", "id": 1 }
}
```

- Returns: An object with a success boolean value, a corresponding message and a random question.

```json
{
	"success": true,
	"message": "New question created successfully.",
	"question": {
		"answer": "The Liver",
		"category": 1,
		"difficulty": 4,
		"id": 20,
		"question": "What is the heaviest organ in the human body?"
	}
}
```

## Tests

To deploy the tests, create a seperate database and then run the following:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
