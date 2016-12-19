
from datetime import date, datetime
import sys
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from config import *

def log(text):
    PY_VERSION = sys.version_info[0]

    if PY_VERSION == 2:
        print text

    if PY_VERSION == 3:
        print(text)


def get_response(url):
    PY_VERSION = sys.version_info[0]

    if PY_VERSION == 2:
        try:
            import urllib
            return json.loads(urllib.urlopen(url).read())
        except:
            raise Exception('try -> pip install urllib')

    if PY_VERSION == 3:
        try:
            import requests
            return json.loads(requests.get(url).text)
        except:
            raise Exception("try -> pip install requests")

    
def get_questions():
    log("Retrieving new questions")
    pythonQuestions = []
    phpQuestions = []
    jsQuestions = []
    cssQuestions = []
    questions = []

    today = datetime.now()
    # utc_date = date(today.year,today.month,today.day)
    utc_date = date(2016,12,18)
    timestamp = (utc_date.toordinal() - date(1970, 1, 1).toordinal()) * 24*60*60

    keywords = ['python','php','javascript','css']
    for key in keywords:
        api_url = "http://api.stackexchange.com/2.2/questions?fromdate={timestamp}&order=desc&sort=activity&tagged={tagged}&site=stackoverflow".format(timestamp=timestamp,tagged=key)
        if key == 'python':
            pythonQuestions = sorted(get_response(api_url)['items'] , key= lambda k : k['view_count'])[:5]
            questions.append(pythonQuestions)
        elif key == 'php':
            phpQuestions = sorted(get_response(api_url)['items'], key= lambda k : k['view_count'])[:5]
            questions.append(phpQuestions)
        elif key == 'javascript':
            jsQuestions = sorted(get_response(api_url)['items'], key= lambda k : k['view_count'])[:5]
            questions.append(jsQuestions)
        elif key == 'css':
            cssQuestions = sorted(get_response(api_url)['items'], key= lambda k : k['view_count'])[:5]
            questions.append(cssQuestions)
    
    return questions

def prepareEmailBody(questions):
    body = ""
    for question in questions:
        body += "<div><h3>{0}</h3>".format(question[0]['tags'][0])
        for data in question:
            body += '<div><p><a href="{0}" style="text-decoration:none;font-size:12px;color:#666;font-weight:bold">{1}</a></p>'.format(data['link'],data['link'])
            body += '<p>Total Views : <span style="font-weight:bold">{0}</span></p>'.format(data['view_count'])
            body += '<p>Total Answers : <span style="font-weight:bold">{0}</span></p>'.format(data['answer_count'])
            body += '</div>'
        body += '</div>'
    return body

    
def send_mail(questions):

    body = prepareEmailBody(questions)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Top 10 Questions'
    msg['From'] = SENDER
    msg['To'] = RECEIVERS
    html_body = MIMEText(body, 'html')
    msg.attach(html_body)
    try:
       email = smtplib.SMTP('smtp.gmail.com', 587)
       email.starttls()
       email.login(SENDER, PASSWORD)
       email.sendmail(msg['From'], [msg['To']], msg.as_string())
       email.quit()         
       log("Successfully sent email")
    except:
       log("Error: unable to send email")

def get_top_ten_questions():
    log("Fetching questions")
    questions = get_questions()
    send_mail(questions)    
            
if __name__=='__main__':
    get_top_ten_questions()