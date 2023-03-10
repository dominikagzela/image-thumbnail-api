# image-thumbnail-api

This is a Django REST Framework API that allows users to upload images in PNG or JPG format. Users can list their uploaded images and different tiers of accounts have different capabilities, such as generating different thumbnail sizes and expiration time to the uploaded images. The admin panel allows administrators to create arbitrary tiers with configurable thumbnail sizes and other settings. The API has tests and validation.


# Installation
To run this project locally, you need to have Python and pip installed on your machine.

Clone the repository to your local machine:

    HTTPS:  git clone https://github.com/dominikagzela/image-thumbnail-api.git

    SSH:    git clone git@github.com:dominikagzela/image-thumbnail-api.git

Create and activate a virtual environment:

    virtualenv -p python venv
    source venv/bin/activate

Install the project dependencies:

    pip install -r requirements.txt

Create a new database in PostgreSQL with the same name as the database in the backup file ('image_thumbnail_db.sql')

Open a terminal and navigate to the directory where the backup file is located.

Run the following command to restore the database from the backup file:

    pg_restore -U username -d databasename image_thumbnail_db

Run the Django migrations to create the database tables:

    python manage.py makemigrations
    python manage.py migrate

Run the Django development server:
    python manage.py runserver


# Authentication

You can log in as an admin using the following credentials:

    admin: admin.anna
    password: admin.anna

You can log in also as an user using the following credentials:

    username: user1
    password: user1

    username: user2
    password: user2

    username: user3
    password: user3

# Tests

To run the tests for this project, run the following command:

    pytest tests.py
