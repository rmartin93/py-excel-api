# Discovery Questions for Python Excel API

Based on your seed document, I understand you want to create a **Python API for Excel report generation** that can use sample data to create reports, read Excel templates, and eventually connect to MS SQL databases. This will be your first Python project, transitioning from a TypeScript/Express version.

Please answer the following questions to help create a comprehensive SRS:

## Problem & Vision

### 1. Who will be the primary users of this API?

-   [x] a) Developers who need to generate reports programmatically
-   [x] b) Business users who want automated report generation
-   [ ] c) Internal applications/services that need Excel output
-   [ ] d) All of the above

**Additional context:**
The users generate reports each year for submission to the government. This api would help automate a lot of that.

### 2. What specific pain points does this solve compared to your current TypeScript version?

-   [ ] a) Performance issues
-   [ ] b) Integration requirements with Python ecosystem
-   [ ] c) Deployment constraints on Windows IIS
-   [x] d) Other technical limitations

**Additional context:**

-   Some limitations with javascript's ability to interact with excel.
-   Speed is a bit of a question mark, not sure if python would be faster.
-   I made a fork of exceljs to fix some of the issues it was having with getting and then adding rows to excel tables, for an example of one limitation I overcame. But just curious about python and if it might be better.

## Core Functionality

### 3. For the Excel templates, what level of complexity do you need to support?

-   [x] a) Simple data filling (cells with placeholders)
-   [ ] b) Charts and graphs generation
-   [x] c) Complex formatting and styling
-   [x] d) Dynamic table sizing
-   [ ] e) All of the above

**Additional context:**
To my knowledge, charts and graphs are not used in the reports they submit, but it could be a flashy thing to add that could "wow them" ... I know they use pivot tables, but not charts and graphs yet.

### 4. What data sources will this API need to handle initially?

-   [x] a) Sample/mock data only
-   [ ] b) JSON data from HTTP requests
-   [ ] c) CSV files
-   [ ] d) Eventually MS SQL databases
-   [ ] e) Multiple formats

**Additional context:**
This version I think is fine to just use sample data. When I port it over to the work computer I'll have it connect to the ms sql db, but I've never done that before, so some notes on how to best do that would be appreciated. Maybe even an example set of utility files that I could just put the hostname, db user, db password, etc. into that I could use as well.

## Technical Context

### 5. For the Windows IIS deployment, do you have specific constraints?

-   [ ] a) Must use specific Python version
-   [x] b) Must work with Windows Authentication
-   [x] c) Must handle CORS for specific domains
-   [x] d) Must integrate with existing IIS applications

**Additional context:**
There are currently existing php and iis node projects in there, so that could be a limiter. The serer at work uses python version 3.13.3.

### 6. What's your preferred Python web framework?

-   [ ] a) FastAPI (modern, automatic docs)
-   [ ] b) Flask (lightweight, flexible)
-   [ ] c) Django (full-featured)
-   [x] d) No preference - recommend best fit

**Additional context:**
My only preference on framework is to use something modern with good docs and good adoption in the community.

## Data & Security

### 7. For the Windows Authentication you mentioned, what user information do you need?

-   [x] a) Username only
-   [ ] b) Username and department/role
-   [ ] c) Full Active Directory details
-   [ ] d) Custom authorization levels

**Additional context:**
We grab the user's id from windows auth and then pretty much use that for everthing.

### 8. How should errors be handled and logged?

-   [x] a) Simple console logging for now
-   [x] b) File-based logging
-   [ ] c) Database logging (like your current crd.error_log_insert)
-   [ ] d) Structured logging with levels

**Additional context:**
I'd like to have both A and B, with sample docs included for how to transition the global error handler into logging into the db as well for when I need to do that.

## Success Metrics

### 9. What would make this project successful in the first phase?

-   [x] a) Successfully generates basic Excel reports from sample data
-   [x] b) Works with at least one Excel template
-   [ ] c) Deploys successfully to your work Windows IIS
-   [ ] d) Matches feature parity with TypeScript version

**Additional context:**
C and D I will have to do on my own when I port it, but if I can get a and b working here that would be a good first step. I was thinking of having the excel templates live in a folder in the project. That way, when the client gives us a report, we can turn it into a template and then have it live in the project and be available to use whenever they'd like.

### 10. How important is type checking for this Python version?

-   [ ] a) Critical - want strict type checking throughout
-   [x] b) Important for data validation only
-   [ ] c) Nice to have but not essential
-   [ ] d) Skip for now, add later

**Additional context:**
The type checking has been really nice whenever the data is being used in a report. Whenever I just need a simple api route that does something like getting a list of users from the db and returning it, there's really no need since the frontend uses zod and does data validation there. I tend to only do data validation in the place where the data is being used, as that is where I find it useful.

---

## Additional Questions

### 11. Are there any specific Excel libraries you prefer or want to avoid?

**Answer:**
I'm brand new, so not yet. I would say to just make sure to use whatever is most popular / has the least number of known bugs. I wound up going with exceljs for my typescript project. It only had one bug that I needed to fork and fix.

### 12. What's the expected volume of reports this API will generate?

-   [ ] a) Low volume (< 10 reports per day)
-   [x] b) Medium volume (10-100 reports per day)
-   [ ] c) High volume (100+ reports per day)
-   [ ] d) Unknown/varies significantly

### 13. Do you need any specific Excel features?

-   [ ] a) Password protection on generated files
-   [x] b) Multiple worksheets in a single file
-   [x] c) Conditional formatting
-   [x] d) Pivot tables
-   [ ] e) None of the above

### 14. How should the API handle large datasets?

-   [ ] a) Load everything into memory (simple approach)
-   [x] b) Stream data to avoid memory issues
-   [ ] c) Paginate large results
-   [ ] d) Return error if dataset too large

\*\*I do not believe we have run into an issue with large datasets from the db yet. We have paginated result sets using tanstack table and paginated queries before, but have not run into the issue yet with producing a report. A solution for this would be a "nice to have" I guess I would say.

### 15. What authentication/authorization do you need beyond Windows Auth?

-   [ ] a) API keys
-   [ ] b) JWT tokens
-   [ ] c) Role-based permissions
-   [x] d) Just Windows Authentication is sufficient

---

**Instructions:**

1. Check all applicable boxes with [x]
2. Fill in additional context where relevant
3. Add any other requirements or concerns not covered above
4. Save this file when complete and let me know - I'll use your answers to create the SRS document.
