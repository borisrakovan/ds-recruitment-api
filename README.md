# Datasentics Recruitment API 

This project is my solution to the Datasentics backend engineer entry task.

I've used the following technologies:

- [Python 3.9](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite](https://www.sqlite.org/)
- [Marshmallow](https://marshmallow.readthedocs.io/) - validation and (de)serialization


Although it is usually not the best practice, I decided to include the database file in the VCS so that it doesn't
need to be created manually when testing the API. Also, it already contains some testing entities that I've created for 
demonstration purposes.

I'm also aware that there are more robust database engines that should be preferred in production environments,
however, I think than SQLite is good enough for the purpose of this exercise.

## Setup

To run the project, first install the necessary dependencies to your virtual environment by running

```
pip install -r requirements.txt
```

Then, run the following command to start the server


```
$ flask run
```

After that, the API should be up and running at `http://127.0.0.1:5000/`.

## API Documentation


The Flask API contains several endpoints that are described in this section.

`GET /` - basic health check endpoint, returns a string if the API is running

### Candidates

`GET /candidates` - returns a list of all candidates

`GET /candidates/<candidate_id>` - returns a single candidate with the given id

`POST /candidates` - accepts a json body with data of the candidate to create. The body 
should be of the following form

```
{
	"first_name": "Boris",
	"surname": "Rakovan",
	"email": "b.rakovan@gmail.com",
	"expected_salary": 72000,
	"skills": ["python", javascript"]
}
```

It returns the newly created candidate.

`PUT /candidates/<int:candidate_id>` - accepts a json body with data of the candidate to update. On success 
returns the updated candidate.

`DELETE /candidates/<int:candidate_id>` - deletes the candidate with the given id. Returns a 204 status code on success.

### Advertisements

`GET /advertisements` - returns a list of all job advertisements

`GET /advertisements/<int:advertisement_id>` - returns a single job advertisement with the given id

`POST /advertisements` - accepts a json body with data of the job advertisement to create. The body 
should be of the following form

```
{
	"title": "Python software developer",
	"salary_min": 1000,
	"salary_max": 5000,
	"full_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
}
```

It returns the newly created advertisement.

`PUT /advertisements/<int:advertisement_id>` - accepts a json body with data of the job advertisement to 
update. On success returns the updated advertisement.

`DELETE /advertisements/<int:advertisement_id>` - deletes the advertisement with the given id. Returns a 204 status 
code on success.


### Other

`POST /advertisements/<int:advertisement_id>/apply` - accepts a json body containing an id of the candidate
that is applying for the advertisement specified by advertisement_id from the url.

The body should be of the following form

```
{
    "candidate_id": 1
}
```

It creates a new job application for the candidate with the given id and returns the updated advertisement object. 
