# The Chores App
## An app to sow familial peace and harmony

## Why?

If you're a child or former child with children, you have more than likely experienced the arguments, disagreements, miscommunications, failures of memory, and flat out non-truth telling that goes with trying to get chores done. As a former child with children, I have experienced all of the of above from both sides of the proverbial table.

So, rather than continue the cycle of arguing, disagreeing, miscommunication, failing to remember, and living in parallel realities between teendom and adultdom - and because I needed a final project for my Udacity course - I decided to create this app.

## Technical bits: Overview

The app is currently only usable via API without a front end. You can use cURL and/or Postman, for example, to access the API endpoints, and there is a package of Postman collections in the utilities directory. The app can be run locally, and it's also hosted on Heroku at https://chorez-app.herokuapp.com. Note the spelling of "chorez" vs. "chores." It's written in Python, uses Flask when run locally and gunicorn on Heroku, and uses a PostgreSQL backend in both cases.

There are two permissions-based roles - admin and user - using Auth0 for OAuth authentication and authorization. Where this app is currently being posted for a final project, the details on creating an Auth0 account and generating tokens, is currently out of scope for this document. That said, the Java web tokens (JWTs) for both user roles for both local and Heroku deployments are located in the Postman collections included in the **utilities** directory. See the README in that directory for more information.

Please note that I've developed this on a Mac, which comes with PostgreSQL already installed, and I have not tested running this on any other operating system. Other operating systems may require you to explicitly install PostgreSQL first and may have differences in some of its related commands.

### Technical bits: Requirements
#### Variables files
There are two variables files that you will need to create in order to use the app, and there are two sample files in the utilities directory:

- A .env file in the app root directory
- A .flaskenv file in the app root directory

Just modify those two files, as needed; move to the app root directory; and be sure to add a "." to the beginning of the file names, as these are hidden files.

Each of these are used when the app is running locally. Heroku provides config vars which act as environment variables in the local .env file, but in the Heroku space. There is no need for the .flaskenv variables in Heroku.

##### The .env file
This file is used by models.py and has three sections, as discussed below. These values are not used by Heroku. For Heroku, the appropriate values are populated by the config vars in Heroku.

###### Application variables

- APP_STATE - This must be set to 'local' when running locally
- APP_PORT - This is the port used when the app runs locally
- APP_DEBUG - Set to 'True' when running in 'development' mode
- APP_HOST - Set to 'localhost' to indicate that this will be running on your local machine.

###### Database variables

- DB_HOST - Set to 'localhost:5432' for a default, local PostgreSQL instance
- DB_USER - Default is 'udacity', but can be set to whatever you like
- DB_PWD - Can be set to '' to indicate no password when run in 'development' mode
- DB_NAME - Default is 'chores_test' for dev and 'chores' for production

###### Auth variables
The app uses Auth0 for authentication and authorization using Java web tokens (JWTs).

- AUTH0_DOMAIN
- ALGORITHMS
- API_AUDIENCE

##### The .flaskenv file
This file is used by Flask when starting and when run locally:

- FLASK_APP - Set this to app.py
- FLASK_ENV - This can be either 'development' or 'production'
- FLASK_RUN_PORT - The default is 5150. \m/ EVH \m/

You can also set these values manually at run time, should you choose to do so.

> If you change the value of the port, be sure to update {{url}} variable in the utilities/postman_collection_local.json file

## Running the app locally for testing
The script uses a PostgreSQL role called "udacity," which has the 'Create role' and 'Create DB' attributes in my development environment. You can create this role, create a different one, or use an existing one in your PostgreSQL instance. Just be sure to modify the script and .env file to replace "udacity," as needed.
### Stand up the test database
1. Start PostgreSQL: `pg_ctl -D /usr/local/var/postgres start`
  - Create a database role to own this database, as appropriate.
  - Update the .sql script, if needed.
1. Create the test database: `createdb -O udacity chores_test` If you use a different database name in the .env file, use that name here instead of 'chores_test'.
1. Use the SQL script to import the test data: `psql chores_test < demo_db.sql`

You can always start over by deleting the database with `deletedb chores_test` and then repeat steps 2 and 3 to basically reset.

### Start the app locally
1. Create a Python virtual environment: `python3 -m virtualenv env`
2. Activate the virtual environment: `source env/bin/activate`
3. Install the required Python modules (first run only): `pip3 install -r requirements.txt`
4. Start the app: `python3 app.py`

The app will be available on http://localhost:[FLASK_RUN_PORT] using the port you specify in the .flaskenv file. My instance is set up on port 5150, so the URL is http://localhost:5150. This port value is set in the .flaskenv file.

## Running the app locally in production
To run the app locally, it's pretty straightforward.

1. Update the .env file with your production values
2. Start PostgreSQL
3. Create the production database: `createdb chores`
4. Migrate to the app root directory and run `flask db init`
5. Follow steps 1, 2, and 4 as indicated in "Start the app" above

# The API endpoints
## Overview
There are three endpoint types - users, categories, and chores - each of which has four allowed methods - GET, POST, PATCH, and DELETE. Access to these is controlled by the user roles. Admins have access to all endpoints and methods, while users may only use the GET and PATCH methods for the chores endpoints.

## Users endpoints
### GET '/users'
- **Returns** a dictionary of user names and user roles in key:value pairs.

Example:
```
{
  "status_code": 200,
  "success": true,
  "users": {
    "bob": "user",
    "gary": "user",
    "katie": "user",
    "marc": "admin",
    "tom": "admin"
  }
}
```
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

Example:
```
{
  "categories": [
    "Dishes",
    "cleaning",
    "yard work"
  ],
  "status_code": 200,
  "success": true
}
```
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

Example:
```
{
  "chores": {
    "Clean bedroom": "complete",
    "Empty dishwasher": "incomplete"
  },
  "status_code": 200,
  "success": true
}
```

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
