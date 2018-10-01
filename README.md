# AWS re:Invent 2018 Schedule Extract Tool

Modified to work with the 2018 schedule
Original codebase  - https://github.com/mda590/reinvent_schedule_extract

-------------------------------------

This tool is meant to make it super easy to export your re:invent schedule into a text file and then import it into whatever tool makes it easier for you to work with.

This tool is given without warranty and probably little maintenance. I whipped it up over the weekend to try to solve my problems (explained below) and thought I would share.

For some reason, when looking at the total # of sessions on the re:Invent Session Catalog, that number is higher than if you look at the totals for each day in the catalog. I have not spent much time investigating why there is this discrepancy.

I didn't see anything in the re:Invent TOS regarding scraping schedule content. If I missed something, I'm happy to remove the tool.

## TL;DR How to use the tool:
1. In the reinvent.py file, update your event website credentials in the USERNAME and PASSWORD vars. These are the credentials you use when logging in on this page: https://www.portal.reinvent.awsevents.com/connect/login.ww. 
2. Download the Chrome web driver for your OS (https://sites.google.com/a/chromium.org/chromedriver/downloads).
3. Change the CHROME_DRIVER var to point to the driver location.
4. Set the REQ_VERIFY to False if you want to ignore SSL cert errors.
5. Run the file in Python. Assuming all goes well, you should end up with a sessions.txt, pipe delimited text file with all of the re:Invent sessions, and a column indicating whether you marked it as a session you'd be interesting in attending.

## Why did I make this?
A couple of reasons:
1. I can always do better with critical thinking and planning when I have something in front of me in a spreadsheet or table that I can manipulate. Yes, the re:Invent website gives an ok experience for browsing, but when given over 1000 sessions and then trying to figure out 1st, 2nd, and 3rd choice, it just is not intuitive for that purpose. Having all of this data available in Excel makes the planning process much easier.
2. The "Get More Results" functionality doesn't work sometimes. I'm not sure if this is just me, or if others experience it, but there will be times when I'm looking at all of the sessions and trying to keep scrolling down, and the "Get More Results" link will not work. I've only been through a few pages of results, when I know there are hundreds more sessions. This got very frustrating.

## Why did I use a combination of Selenium and BeautifulSoup?
One reason: the "Get More Results" button is a JavaScript call, and I could not get that to work in BS for obvious reasons (not an actual browser). I played around with trying to determine if there was an API available for getting actual event information (similar to the event time information I found), but I was not able to find something.