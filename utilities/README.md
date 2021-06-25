# Chores app utilities
## File manifest
In this utilities directory are:

1. A sample .env file
1. A sample .flaskenv file
1. Two Postman collections
1. A demo_db.sql script

## env_sample
This file is used to set database variables that are used by models.py to connect to the database. It's currently set to use the values used in my test environment. Modify it, as needed, for your environment.

A couple of key reminders:
1. Be sure to update the values for production, as appropriate.
1. Note that there is no "." in front of the file name here. It _must_ be named '.env' as it's a hidden file.
1. It _must_ be located in the **app root directory**.

## flaskenv_sample
This file is used by Flask and there are several variables that you can declare in this file. There are only three options that I've selected here. Again, modify as you see fit and change the value of FLASK_ENV to 'production' when you're ready to go into production.

 Reminders:
 1. This also _must_ be renamed '.flaskenv' as it, too, is a hidden file.
 1. It _must_ be located in the **app root directory**.

 ## demo_db.sql
 As stated in the main README, use this file to populate either/both your test and production databases. _If_ your test environment uses a different database owner, then you will want to change the value of the database owner ('Owner: udacity') where it appears in the file.

 This doesn't need to be located in any specific directory.

 ## postman_collection_local.json/postman_collection_Heroku.json
These are collections of endpoint tests for both the 'user' and 'admin' roles in conjunction with Auth0 Java web tokens (JWTs). As the names indicate, one is a collection of tests for a local instance of the app and the other is for the instance hosted on Heroku. The JWTs are stored as variables in each of the collections.
