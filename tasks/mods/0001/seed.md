## This project will use python to create an api that can do the following:

-   Use sample data to create an excel report
-   Put notes in sample data for how to connect to a ms sql databse and connect once it is a real project
-   Read excel templates into memory and fill them with data
-   This project will use Prettier for formatting

## Things to keep in mind

-   This is my first python project. I've built this project in Typescript with Express already.
-   This project is being made on my personal computer, but the goal is to ultimately port it over to my work computer and run this api on Windows IIS

## Typical Issues

-   CORS issues
-   Grabbing windows authentication information from req headers
-   Might just need to solve those on the other computer, but some notes on it might be handy

## Nice to Haves

-   It would be nice if we could do some type checking occassionally when we are going to actually use the data to make a report. Sometimes the api will just return data from the db, so there's really no need there, as the frontend uses zod.
-   It would be nice to have a global error handler that, eventually, will insert error records into the databse. Our current handler runs crd.error_log_insert and passes the user_id and long_name (error message).
-   It would be nice to have some sort of logging functions made so that we can log what is happening for troubleshooting on the fly
