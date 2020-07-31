# bookstore
Book Store service for setting up books, renting books and calculating rental charges
Service deployed to heroku and how this is done
## Environment:
- Python version: 3.7
- Django version: 3.0.6
- Django REST framework version: 3.11.0


## Data:
Example of a book JSON object (v1):
```
{
   "title": "Encounters From Africa",
   "code": "A novel"
}
```
Example of a book JSON object (v2):
```
{
   "title": "Encounters From Africa",
   "code": "A novel",
   "book_type": "regular",
   "daily_rental_charge": 1.5
}
```

Example of a book rental JSON object:
```
{
    "customer": "John Doe",
    "books_data": [
        {
            "id": 1,
            "duration": 10
        },
        {
            "id": 2,
            "duration": 30
        }
    ]
}
```

## Requirements:
The REST service must expose the /rental/ endpoint, which allows for managing the rental service for books in the following way. At posting rental payload, total rental charge is calculated
The REST service must expose the /books/ endpoint, which allows for managing the collection of books in the following way: 

## Books
POST request to `/api/v1/books/`:
- creates a new book data record
- expects a valid book object as its body payload, except that it does not have an id property; you can assume that the given object is always valid
- adds the given object to the collection and assigns a unique integer id to it
- the response code is 201 and the response body is the created record, including its unique id

GET request to `/api/v1/books/`:
- the response code is 200
- the response body is an array of matching records, ordered by their ids in increasing order

GET request to `/api/v1/books/<id>/`:
- returns a record with the given id
- if the matching record exists, the response code is 200 and the response body is the matching object
- if there is no record in the collection with the given id, the response code is 404

DELETE request to `/api/v1/books/<id>/`:
- deletes the record with the given id from the collection
- if matching record existed, the response code is 204
- if there was no record in the collection with the given id, the response code is 404


## Rentals
POST request to `/api/v1/rentals/`:
- creates a new book rental record
- expects a valid book rental object as its body payload, except that it does not have an id property; you can assume that the given object is always valid
- calculates the rental charge for each book in the payload based on the duration of rental and any other parameters and updates the payload
- sums up the rental charge for all the books in the payload
- adds the given object to the collection and assigns a unique integer id to it
- the response code is 201 and the response body is the created record, including its unique id

GET request to `/api/v1/rentals/`:
- the response code is 200
- the response body is an array of matching records, ordered by their ids in increasing order

GET request to `/api/v1/rentals/<id>/`:
- returns a record with the given id
- if the matching record exists, the response code is 200 and the response body is the matching object
- if there is no record in the collection with the given id, the response code is 404

DELETE request to `/api/v1/rentals/<id>/`:
- deletes the record with the given id from the collection
- if matching record existed, the response code is 204
- if there was no record in the collection with the given id, the response code is 404


## Running Locally
Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

```sh
$ source ../env/bin/activate
$ pip3 install -r requirements.txt

# Create model then make migrations
$ python3 manage.py makemigrations books
$ python3 manage.py migrate

# delete previous migrations so as to redo migrations
$ python3 manage.py migrate books zero 

# run app
$ python3 manage.py runserver


# run tests
$ python3 manage.py test

# run on heroku
$ heroku local
```
For python deployment your app should now be running on [127.0.0.1:8000](http://127.0.0.1:8000/) or 
[localhost:8000](http://127.0.0.1:8000/) 
For heroku deployment your app should now be running on [localhost:5000](http://localhost:5000/) or [0.0.0.0:5000](http://localhost:5000/) .

## Deploying to Heroku 

```sh
# version 1, story 1
$ heroku create bookstore-service-v1
# version 2, story 2
$ heroku create bookstore-service-v2
# version 2, story 2
$ heroku create bookstore-service-v3

$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

Heroku deployments created as (version1, story 1):
https://bookstore-service-v1.herokuapp.com

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

https://bookstore-service.herokuapp.com/ | https://git.heroku.com/bookstore-service.git
