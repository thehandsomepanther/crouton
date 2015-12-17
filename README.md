# crouton
This is a web scraper for Northwestern University's Course and Teacher Evaluations, known as CTECs (I don't know what that last "C" stands for either), located in Caesar, their student portal.

## Getting Started
Crouton takes in a CSV file as an input, as this is where it will export all CTEC information. I recommend just creating one in the root directory of this project (aka the only directory) but this scraper was made in 🇺🇸 `100% FREE COUNTRY USA OF AMERICA STATES` 🇺🇸 so you can do whatever you want I guess. To run crouton from your terminal, simply type

```
python crouton.py crouton.csv
```

where crouton.csv is a CSV file you've created in the root directory.

This scraper runs on the Selenium WebDriver for Python, so if you don't have that you'll need to get it. [Here](http://selenium-python.readthedocs.org/installation.html) are a few places you can get it if you don't already have it. The WebDriver is for Firefox, so you will have to have that installed as well. Some versions of Firefox may not play nice with Selenium, or so I've heard. For reference, I'm using Firefox v42.0.

To use this scraper, you need a Northwestern NetID and password. For the script to import your credentials, make a file called `credentials.py` that declares just two variables: `netid` and `password`, like this:

```
netid = "net123"
password = "P4$$.w0rd"
```

## How The Data is Structured
Each row spans 96(!!) columns. Yeah, it's a doozy. In a nutshell, each row contains:

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

`essay_responses` is just a huge block of text containing all the free responses students gave about the course. Individual comments are separated by a `\`.

The first three columns, `search_career`, `search_subject`, and `search_course` are just used by crouton to help it navigate through CTECs and pick up where it left off, mostly because of a few quirks in the way CTECs are organize that have to do with courses that have had their names changed. The same courses (and the same CTECs) can also appear multiple times depending on whether their academic subject has been changed (e.g. the Hebrew courses used to be in AAL (Asian and African Languages) and are now in their own subject, HEBREW).

## Disclaimer
There are a lot of CTECs (read: A LOT OF CTECs), so this scraper will take a long time to run. It's also very possible (some might even say probable) that your browser will timeout or Selenium will throw a TimeoutException or the world will end or something. So just be aware of that and know that not every NoSuchElementException is a real exception--sometimes it's just Caesar being slow. Luckily, crouton will be able to detect where you left off if your CSV already has some rows filled in.

This is still a work in progress. If you run into any issues please create a new issue and let me know what's going on and how I can reproduce what happened.
