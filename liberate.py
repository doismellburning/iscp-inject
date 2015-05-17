import lxml.html
import os
import pprint
import requests


LOGIN_URL = "https://www.iscp.ac.uk/Default.aspx"

def sign_in(u, p):

    session = requests.session()
    raw = session.get(LOGIN_URL)

    html = lxml.html.fromstring(raw.text)

    viewstate = html.cssselect("input#__VIEWSTATE")[0].value
    viewstate_generator = html.cssselect("input#__VIEWSTATEGENERATOR")[0].value

    payload = {
        "ctl00$cphMain$Logon1$_resolution" : "1440x900",
        "ctl00$cphMain$Logon1$_email" : u,
        "ctl00$cphMain$Logon1$_password": p,
        "ctl00$cphMain$Logon1$_login": "Log in",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstate_generator,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    r = session.post(LOGIN_URL, data=payload, headers=headers)

    assert "unread messages" in r.content

    return session

def get_courses(session):
    r = session.get("https://www.iscp.ac.uk/evidence/courselist.aspx")

    html = lxml.html.fromstring(r.text)

    def extract_course(xlink):
        y = xlink.findall('div')
        if len(y) > 2:
            return y[2].text
        else:
            return None

    return [extract_course(e) for e in html.cssselect(".xlink")]


def upload_course(session, title="Lorem Ipsum", filename="test.jpg", filedata="", filetype="image/png"):
    response = session.get("https://www.iscp.ac.uk/evidence/course.aspx")

    html = lxml.html.fromstring(response.text)

    viewstate = html.cssselect("input#__VIEWSTATE")[0].value
    viewstate_generator = html.cssselect("input#__VIEWSTATEGENERATOR")[0].value
    viewstate_encrypted = html.cssselect("input#__VIEWSTATEENCRYPTED")[0].value
    event_validation = html.cssselect("input#__EVENTVALIDATION")[0].value

    payload = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__EVENTVALIDATION": event_validation,
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEGENERATOR": viewstate_generator,
        "__VIEWSTATEENCRYPTED": viewstate_encrypted,
        "ctl00$cphMain$txtDate": "01/01/1970",
        "ctl00$cphMain$txtEndDate": "",
        "ctl00$cphMain$drpTitles": 6,  # Other
        "ctl00$cphMain$txtOtherTitle": title,
        "ctl00$cphMain$drpTypes": 0,
        "ctl00$cphMain$txtOtherType": "",
        "ctl00$cphMain$txtAwardingBody": "",
        "ctl00$cphMain$txtFeedback": "",
        "ctl00$cphMain$txtLearn": "",
        "ctl00$cphMain$txtImprove": "",
        "ctl00$cphMain$txtActionPlan": "",
        "ctl00$cphMain$topicChooser1$hidScrollTop": "",
        "ctl00$cphMain$topicChooser1$hidTpcExpanded": "True",
        "ctl00$cphMain$topicChooser1$hidSelectedTopics": "",
        "ctl00$cphMain$topicChooser1$hdnPopUpShowing": "",
        "ctl00$cphMain$topicChooser1$hidTab": "",
        "ctl00$cphMain$btnInsert": "Save Course/seminar",
        "ctl00$TraineeReport1$download_token_value_id": "17/05/2015 12:20:46",
        "ctl00$TraineeReport1$txtStartDate": "16/05/2014",
        "ctl00$TraineeReport1$txtEndDate": "16/05/2015",
        "ctl00$txtFeedbackComments": "",
    }

    files = {
        "ctl00$cphMain$fupControl1": (
            filename,
            filedata,
            filetype,  # FIXME
        ),
    }

    r = session.post("https://www.iscp.ac.uk/evidence/course.aspx", data=payload, files=files)

    pprint.pprint(r.text)


if __name__ == "__main__":
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]

    s = sign_in(username, password)

    upload_course(s, filename="EURion.png", filedata=open("/Users/kristian/Downloads/EURion.png", "rb"))
