# crouton
This is a web scraper for Northwestern University's Course and Teacher Evaluations, known as CTECs (I don't know what that last "C" stands for either), located in Caesar, their student portal.

## Getting Started
Crouton takes in a CSV file as an input, as this is where it will export all CTEC information. I recommend just creating one in the root directory of this project (aka the only directory) but this scraper was made in `100% FREE COUNTRY USA OF AMERICA STATES` so you can do whatever you want I guess. To run crouton from your terminal, simply type

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

## Disclaimer
There are a lot of CTECs (read: A LOT OF CTECs), so this scraper will take a long time to run. It's also very possible (some might even say probable) that your browser will timeout or Selenium will throw a TimeoutException or the world will end or something. So just be aware of that and know that not every NoSuchElementException is a real exception--sometimes it's just Caesar being slow. Luckily, crouton will be able to detect where you left off if your CSV already has some rows filled in.

This is still a work in progress. If you run into any issues please create a new issue and let me know what's going on and how I can reproduce what happened.
