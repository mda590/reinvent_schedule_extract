import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from pytz import timezone
from icalendar import Calendar, vText, Event
import json

base_url = "https://www.portal.reinvent.awsevents.com/connect/"
favorites_url = "https://www.portal.reinvent.awsevents.com/connect/interests.ww"
login_url = "https://www.portal.reinvent.awsevents.com/connect/processLogin.do"
scheduling_url = "https://www.portal.reinvent.awsevents.com/connect/dwr/call/plaincall/ConnectAjax.getSchedulingJSON.dwr"
vegas = timezone("US/Pacific")

# Set username and password for reinvent event website
USERNAME = 'YOUR_USERNAME'
PASSWORD = 'YOUR_PASSWORD'

# login and start a session
session = requests.session()
payload = {"password": PASSWORD, "username": USERNAME }
resp = session.post(login_url, data=payload)

# get all the favorites
resp = session.get(favorites_url)
html = resp.content
soup = BeautifulSoup(html, "html.parser")

# find all selected sessions
selected_sessions = soup.findAll("div", {"class": "sessionRow"})

session_data = []

# loop through all sessions, and gather the needed information
for selected_session in selected_sessions:
    # get the link
    link = selected_session.find("a", {"class": "openInPopup"})
    url = link['href']

    # get the session title
    title = link.find("span", {"class": "title"}).text

    # get the abstract
    abstract = selected_session.find("span", {"class": "abstract"}).text
    session_url = "%s%s" % (base_url, url)

    # this contains the session id (int)
    session_id = url.split("=")[-1]

    # get the scheduling information and location from the magic json url
    payload = {
        "callCount":"1",
        "windowName":"",
        "c0-scriptName":"ConnectAjax",
        "c0-methodName":"getSchedulingJSON",
        "c0-id":"0",
        "c0-param0":"string:%s" % session_id,
        "batchId":"4",
        "instanceId":"0",
        "page":"%2Fconnect%2Finterests.ww",
        "scriptSessionId":"OGxWNAOpsVunFAFyWddX2cGpNYl/RTNxNYl-Roe8DFsEq",
    }
    resp = session.post(scheduling_url, data=payload)

    # do some magic and actually get the escaped json
    json_response = resp.content.split("\n")[5].replace('r.handleCallback("4","0","',"").replace('");',"").replace('\\"','"').replace("\\'","'")
    schedule_data = json.loads(json_response)['data'][0]
    print "."


    # Friday, Dec 1, 9:15 AM
    # print schedule_data
    start_dt = datetime.strptime(schedule_data['startTime'], '%A, %b %d, %I:%M %p').replace(year=2017, tzinfo=vegas)
    schedule_data['startDatetime'] = start_dt
    end_dt = datetime.strptime(schedule_data['endTime'], '%I:%M %p').replace(day=start_dt.day, month=start_dt.month, year=2017, tzinfo=vegas)
    schedule_data['endDatetime'] = end_dt

    session_data.append({
        "title": title,
        "abstract": abstract,
        "link": link,
        "schedule": schedule_data
    })

# ok, we have everything we need, now generate an ical file
cal = Calendar()
cal.add('prodid', '-//Re-Invent plan generator product//mxm.dk//')
cal.add('version', '2.0')
for session in session_data:
    event = Event()
    event.add('summary', session['title'].replace("'","\'"))
    event.add('description', session['abstract'])
    event.add('location', session['schedule']['room'])
    event.add('dtstart', session['schedule']['startDatetime'])
    event.add('dtend', session['schedule']['endDatetime'])
    # event.add('url', session['link'])
    event.add('dtstamp', session['schedule']['startDatetime'])
    cal.add_component(event)

# write the ical file
with open("reinvent.ics","w") as f:
    f.write(cal.to_ical())
