# crouton
This is a web scraper for Northwestern University's Course and Teacher Evaluations, known as CTECs (I don't know what that last "C" stands for either), located in Caesar, their student portal.

## Getting Started
Crouton takes in a CSV file as an input where it will export all CTEC information. I recommend just creating one in the root directory of this project (aka the only directory) but this scraper was made in 🇺🇸 `100% FREE COUNTRY USA OF AMERICA STATES` 🇺🇸 so you can do whatever you want I guess. To run crouton from your terminal, simply type

```
python crouton.py crouton.csv
```

where crouton.csv is the CSV file located in the root directory.

This scraper runs on the Selenium WebDriver for Python. [Here](http://selenium-python.readthedocs.org/installation.html) are a few places you can get it if you don't already have it. This is a Firefox WebDriver, so you will have to have that installed as well. Some versions of Firefox may not play nice with Selenium, or so I've heard, so for reference I'm using Firefox v42.0.

For access to CTECs, you need a Northwestern NetID and password (you'll also need to have filled out CTECs for your courses last quarter I believe). For the script to import your credentials, make a file called `credentials.py` also in the root directory that declares just two variables: `netid` and `password`, like this:

```
netid = "net123"
password = "P4$$.w0rd"
```

## How the Data are Structured
Each row spans 95(!!) columns. Yeah, it's a doozy. In a nutshell, each row contains:

```
search_career
search_subject
search_course
academic_quarter
academic_year
academic_subject_code
academic_subject_full
class_number
class_subnum
class_section
class_name
instructor
enrollment_count
response_count
instruction_rating
course_rating
learned_rating
challenging_rating
stimulating_rating
time_rating
school_survey
class_survey
reason_survey
interest_survey
essay_responses
```

All fields suffixed with `_rating` or `_survey` have multiple fields associated with them depending on how they are structured in the actual CTEC, e.g. the `instruction_rating` through `stimulating_rating` fields not only have the average rating of instruction for a class, but also the percentage of people who answered in each rating (1 - 6), as well as the response count for that particular question.

`essay_responses` is just a huge block of text containing all the free responses students gave about the course. Individual comments are separated by a `/`.

The first three columns, `search_career`, `search_subject`, and `search_course` are just used by crouton to help it navigate through CTECs and pick up where it left off, mostly because of a few quirks in the way CTECs are organized that have to do with courses that have had their names or subjects changed. The same courses (and the same CTECs) can appear multiple times depending on whether their academic subject has been changed (e.g. the Hebrew courses used to be in AAL (Asian and African Languages) and are now in their own subject, HEBREW), but crouton will not add CTEC data to the spreadsheet unless the course title contains the search subject, so no duplicate CTECs should show up in the CSV.

## Upcoming Features
As of right now, crouton only knows how to either start from the very beginning and scrape every single undergrad CTEC if it's given an empty CSV to fill in or start from the last record of a given CSV. I hope soon to incorporate all academic careers and make it possible to specify a range of careers, subjects, and even courses to scrape specifically.

## Disclaimer
There are a lot of CTECs (read: A LOT OF CTECs), so this scraper will take a long time to run. It's also very possible (some might even say probable) that your browser will timeout or Selenium will throw a TimeoutException or the world will end or something. Another thing to be aware of is that not every NoSuchElementException is a real exception--sometimes it's just Caesar being slow. Luckily, crouton will automatically stop and restart if it hits one of these errors, and will be able to detect where you left off if your CSV already has some rows filled in.

This is still a work in progress, so if you run into any issues while running this please let me know!
