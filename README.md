# The Chores App: An app to sow familial peace and harmony

## Why?

If you're a child or former child with children, you have more than likely experienced the arguments, disagreements, miscommunications, failures of memory, and flat out non-truth telling that goes with trying to get chores done. As a former child with children, I have experienced all of the of above from both sides of the proverbial table.

So, rather than continue the cycle of arguing, disagreeing, miscommunicating, failing to remember, and living in parallel realities between teendom and adultdom - and because I needed a final project for my Udacity course - I decided to create this app.

## Technical bits: Overview

The app is currently only usable via API without a front end. It's written in Python and uses Flask with a PostgreSQL backend.

There are two permissions-based roles - admin and user - using Auth0 for authentication. Where this app is currently being posted for a final project, the details on creating an Auth0 account and generating tokens, is currently out of scope for this document.

Please note that I've developed this on a Mac, which comes with PostgreSQL already installed, and I have not tested running this on any other operating system, which may require you to explicitly install PostgreSQL first and may have differences in some of its related commands.

### Technical bits: Requirements
#### Variables files
There are two variables files that you will need to create in order to use the app:

- A .env file in the backend/src/database directory
- A .flaskenv file in the backend/src directory

##### The .env file
This file is used by models.py for the following database variables:

- DB_HOST
- DB_USER
- DB_PWD
- DB_NAME

By changing these values in the file, it will make it easier for you to change from your test environment to your production. We'll assume that the DB_NAME value for test is 'chores_test' and for production, the name is just 'chores'.

##### The .flaskenv file
This file is used by Flask when starting and uses the following variables:

- FLASK_APP
- FLASK_ENV
- FLASK_RUN_PORT

You can also set these values manually at run time, should you choose to do so.

## Running the app for testing
### Stand up the test database
1. Start PostgreSQL
2. Create the test database: 'createdb chores_test' If you use a different database name in the .env file, use that name here instead of 'chores_test'.
3. Use the SQL script to import the test data: 'psql chores_test < test_db.sql'

You can always start over by deleting the database with 'deletedb chores_test' and then repeating steps 2 and 3.

### Start the app
1. Create a Python virtual environment: 'python3 -m virtualenv env'
2. Activate the virtual environment: 'source env/bin/activate'
3. Install the required Python modules (first run only): 'pip3 install -r requirements.txt'
4. Start Flask: 'flask run'

The app will be available on http://localhost using the port you specify in the .flaskenv file. My instance is set up on port 5150, so the URL is http://localhost:5150. This port value is set in the .flaskenv file.

## Running the app
To run the app locally, it's pretty straightforward.

1. Update the .env file with your production values
2. Start PostgreSQL
3. Create the production database: 'createdb chores'
4. Migrate to the backend/src/ directory and run 'flask db init'
5. Follow steps 1, 2, and 4 as indicated in "Start the app" above

# The API endpoints
## Overview
There are three endpoint types - users, categories, and chores - each of which has four allowed methods - GET, POST, PATCH, and DELETE. Access to these is controlled by the user roles. Admins have access to all endpoints and methods, while users may only use the GET and PATCH methods for the chores endpoints.

## Users endpoints
### GET '/users'
- **Returns** a dictionary of user names and user roles in key:value pairs.
- A **status code** of 200 will be returned when the query returns results.
- A **status code** of 404 will be returned if there are no records found, such as when the database is first created and the users table is not yet populated.

### POST '/users'
- **Creates** a new user account in the database's users table
  - Required fields are:
      - User name
      - User role
        - The role must be either 'admin' or 'user'
- A **status code** of 200 will be returned when the creation is successful.
- A **status code** of 422 will indicate a failure to create the record.

### PATCH '/users/\<id\>'
- **Updates** the user account name and/or the role of an existing user account based upon the account ID.
- A **status code** of 200 indicates a successful update.
- A **status code** of 404 indicates that the user ID could not be found.

### DELETE '/users/\<id\>'
- **Deletes** a user account using the account ID.
- A **status code** of 200 indicates a successful deletion.
- A **status code** of 404 indicates that the user ID could not be found.

## Categories endpoints
Categories are used to help group similar types of chores together such "Meal chores", which could include "Setting the table", "Clearing the table", and so on.
### GET '/categories'
- **Returns** a dictionary of category IDs and category names in a key:value pairs.
- A **status code** of 200 is returned when results are successfully returned;
- A **status code** of 404 is returned when no results are found, typically with a fresh, unpopulated table.

### POST '/categories'
- **Creates** a new category in the categories table
  - The only required field is the category name
- A **status code** of 200 indicates that the category was created successfully.
- A **status code** of 422 indicates that the creation failed.

### PATCH '/categories/\<id\>'
- **Updates** the category name based upon the category ID.
- A **status code** of 200 indicates that the update was successful.
- A **status code** of 404 indicates that the category ID cannot be found.

### DELETE '/categories/\<id\>'
- **Deletes** a category based upon the category ID.
- A **status code** of 200 indicates that the deletion was successful.
- A **status code** of 404 indicates that the category ID cannot be found.

## Chores endpoints
### GET '/chores'
- **Returns** a dictionary of chores and the status of each in key:value pairs.
- A **status code** of 200 indicates that the values were returned successfully.
- A **status code** of 404 indicates that no records were found, which typically indicates that no chores have yet been created.

### POST '/chores'
- **Creates** a chore record in the chores table
  - Required fields
    - Chore name
    - Recurrence ('daily', 'weekly', 'ad-hoc')
    - Category ID (from categories table)
    - User ID (from users table)
    - Status ('incomplete', 'complete', 'n/a')
    - Points (a numeric value)
- A **status code** of 200 indicates that the chore was created successfully.
- A **status code** of 422 indicates that the creation failed.

### PATCH '/chores/\<id\>'
- **Updates** an existing chore based upon the chore ID.
- A **status code** of 200 indicates the update was successful.
- A **status code** of 404 indicates that the chore ID could not be found.

### DELETE '/chores/\<id\>'
- **Deletes** an existing chore based upon the chore ID.
- A **status code** of 200 indicates the deletion was successful.
- A **status code** of 404 indicates that the chore ID could not be found.
