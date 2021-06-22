# Chores app utilities
## File manifest
In this utilities directory are:

1. A sample .env file
1. A sample .flaskenv file
1. A Postman collection
1. A test_db.sql script

## .env file
This file is used to set database variables that are used by models.py to \
connect to the database. It's currently set to use the values used in my test \
environment. Modify it, as needed, for your environment.

A couple of key reminders:
1. Be sure to update the values for production, as appropriate.
1. Note that there is no "." in front of the file name here. It _must_ be named\
 '.env' as it's a hidden file.
1. It _must_ be located in the **backend/src/database/** directory.

## .flaskenv file
This file is used by Flask and there are several variables that you can declare\
 in this file. There are only three options that I've selected here. Again, \
 modify as you see fit and change the value of FLASK_ENV to 'production' when \
 you're ready to go into production.

 Reminders:
 1. This also _must_ be renamed '.flaskenv' as it, too, is a hidden file.
 1. It _must_ be located in the **backend/src/** directory.

 ## test_db.sql
 As stated in the main README, use this file to populate your test database. \
 You will want to change the value of the database owner ('Owner: udacity') \
 where it appears in the file, if your test environment uses a different \
 database owner.

 This doesn't need to be located in any specific directory.

 ## postman_test.json
 This is a collection of endpoint tests for both the 'user' and 'admin' roles \
 in conjunction with Auth0 Java web tokens (JWTs). This collection was created \
 for the Udacity project review and the JWTs are not provided here, but will \
 be provided to the Udacity reviewer(s) directly.

 If you're used to creating JWTs and want to generate your own for usage with \
 this collection, you will need to create two global variables for the admin \
 and user roles. These variables are:

 - Chores_admin_auth
 - Chores_user_auth

 You'll see that these variables are used in all of the endpoint tests.
