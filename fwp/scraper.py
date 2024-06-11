import bs4, pyautogui
import requests, sys, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import smtplib, sys
from getpass import getpass
from email.message import EmailMessage
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import utils

class Contact:
    def __init__(self, firstName, lastName, email, company, position):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.company = company
        self.position = position
    def __str__(self):
        return f"{self.firstName} {self.lastName} {self.email} {self.company} {self.position}"

def hyperlink(url, numWords):
    with pyautogui.hold('ctrl'):
        with pyautogui.hold('shift'):
            for i in range(0, numWords):
                pyautogui.press('left')
        pyautogui.press('k')
    pyautogui.write(url)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')

senderEmail = input("enter email: ")
senderPassword = getpass("enter password: ")

browser = webdriver.Chrome()
browser.implicitly_wait(5)
browser.get('https://search.grata.com/lists/MNGY283D/contacts')
input("return when finished logging in and on contacts page")
htmlSource = browser.page_source
browser.quit()
grataScraper = bs4.BeautifulSoup(htmlSource, 'html.parser')
contactCards = grataScraper.select('div.contact-card')
contactList = []
for card in contactCards:
    target = card.select_one('div > div > div > div:nth-of-type(2) > div > span > span')
    if target is None:
        print("incomplete contact")
        continue
    if(target.text.strip().count(' ') != 1):
        print(target.text.strip() + " was skipped")
        continue
    firstName, lastName = target.text.strip().split(' ')
    target = card.select_one('div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')
    if target is None:
        print("incomplete contact")
        continue
    coAndPos = target['data-tooltip-content'].split(' - ')
    if(len(coAndPos) < 2):
        print("incomplete contact")
        continue
    company = coAndPos[0]
    position = coAndPos[1]
    target = card.select_one('div > div > div:nth-of-type(2) > div > div > a > span > span > span')
    if target is None:
        print("incomplete contact")
        continue
    email = target.text
    contact = Contact(firstName, lastName, email, company, position)
    contactList.append(contact)
    print(contact)

sentEmails = set()
companiesAdded = set()
emailFileRead = open("sent-email-list.txt", "r")
while True:
    currContact = emailFileRead.readline().strip()
    if(currContact == ""):
        break
    sentEmails.add(currContact)
emailFileRead.close()
contactFileRead = open("contact-added-list.txt", "r")
while True:
    currContact = contactFileRead.readline().strip()
    if(currContact == ""):
        break
    companiesAdded.add(currContact)
contactFileRead.close()


context = ssl.create_default_context()
with open("sent-email-list.txt", "a") as emailFile:
    with open("contact-added-list.txt", "a") as contactFile:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.ehlo()
            smtp.login(senderEmail, senderPassword)
            pyautogui.alert("switch to hubspot tab to begin program")
            time.sleep(1)
            pyautogui.click(2693, 302)
            for contact in contactList:
                if(contact.company in companiesAdded):
                    print(f"{contact.company} is already a contact")
                    continue
                contactFile.write(f"{contact.company}\n")
                companiesAdded.add(contact.company)
                time.sleep(2.2)
                pyautogui.click(1983, 436)
                pyautogui.write(contact.email)
                pyautogui.press('tab')
                pyautogui.write(contact.firstName)
                pyautogui.press('tab')
                pyautogui.write(contact.lastName)
                conf = pyautogui.confirm("Add contact?", "Check", ["Yes", "No"])
                if(conf == "No"):
                    pyautogui.click(2827, 203)
                    time.sleep(1.5)
                    pyautogui.click(2693, 302)
                    continue
                pyautogui.click(1938, 900)
                pyautogui.write(contact.position)
                pyautogui.press('tab')
                pyautogui.write(contact.company)
                pyautogui.press('tab')
                pyautogui.write("n/a")
                pyautogui.click(1952, 1355)
                pyautogui.write("n/a")
                pyautogui.press('enter')
                pyautogui.click(1968, 1502)
                pyautogui.write("n/a")
                pyautogui.press('enter')
                pyautogui.moveTo(2266, 963)
                pyautogui.scroll(-2000)
                pyautogui.click(2013, 576)
                pyautogui.write("technology")
                pyautogui.press("enter")
                pyautogui.click(1996, 722)
                pyautogui.write("fixed wireless")
                pyautogui.press("enter")
                pyautogui.click(2376, 196)
                pyautogui.click(1991, 857)
                pyautogui.write("n/a")
                pyautogui.press("enter")
                pyautogui.click(2376, 196)
                pyautogui.click(1999, 1011)
                pyautogui.write("tech practice")
                pyautogui.press("enter")
                pyautogui.click(2376, 196)
                time.sleep(0.5)
                pyautogui.moveTo(2276, 1646)
                time.sleep(0.4)
                pyautogui.click()
                if(contact.email in sentEmails):
                    print(f"{contact.email} has already been sent an email")
                    continue
                emailConfirm = pyautogui.confirm(f"Send email to {contact.firstName} {contact.lastName} at {contact.company}? ({contact.email})", "Email Confirmation", ["Yes", "No"])
                if(emailConfirm == "No"):
                    continue
                recipient = contact.email
                subjectLine = "Subject: Investment Opportunity - " + contact.company + "\n"
                subject = "Investment Opportunity - " + contact.company
                html_content = f"""
                <html>
                <body style="font-family: Arial;">
                <p>Hi {contact.firstName},</p>
                <p>I'm Daniel with <a href='https://www.sellsidegroup.com/'>Sellside Group</a>. I work with my two MD's, <a href='https://www.linkedin.com/in/paul-muckleston-11785a3/'>Paul Muckleston</a>, who leads our Tech practice having a 20+ yr executive career with Microsoft and <a href='https://www.linkedin.com/in/diaspinall/'>David Aspinall</a>, former President of AT&T Canada. We work with both PE firms and technology firms, like {contact.company}, to help them add to their portfolio, grow through acquisition, or exit through a sale. It would be great to set up an intro meeting with you, Paul, and/or David to get to know each other and better understand your business and goals.</p>
                <p>What are a few dates and times that work for you over the next two weeks?</p>
                <p>Best,<br>
                Daniel Zhou</p><br>
                <p>--</p><br>
                <div style="display: flex; column-gap: 30px;">
                    <img src="cid:image1" style="width: 135px; aspect-ratio: 1 / 1;">
                    <div style="padding-top: 10px;">
                    <p style="line-height: 1.44; margin: 0; padding-bottom: 5px">
                        <span style="font-size: 12pt; font-weight: 700">Daniel Zhou</span>
                    </p>
                    <p style="line-height: 1.44; margin: 0;">
                        <span style="font-size: 8pt">Business Development Consultant Intern</span>
                    </p>
                    <p style="line-height: 1.44; margin: 0">
                        <a href="mailto:dzhou@sellsidegroup.com" target="_blank" style="font-size: 11pt;">dzhou@sellsidegroup.com</a>
                    </p>
                    <p style="line-height: 1.44; margin: 0">
                        <span style="font-size: 11pt;">(972) 679-9984</span>
                    </p>
                    </div>
                </div>
                </body>
                </html>
                """
                msg = MIMEMultipart('alternative')
                msg['From'] = utils.formataddr(('Daniel Zhou', senderEmail))
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(html_content, 'html'))
                with open("sellside-logo.jpg", 'rb') as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header('Content-ID', '<image1>')
                    msg.attach(mime_img)
                emailFile.write(f"{contact.email}\n")
                smtp.sendmail(senderEmail, recipient, msg.as_string())

pyautogui.alert("program finished successfully")

# dummyList = []
# dummyList.append(Contact("Tyler", "Steinkamp", "operlaston21@gmail.com", "SKT T1 Inc.", "Mid Laner"))
# dummyList.append(Contact("tyler", "1", "operlaston69@gmail.com", "ex company", "ex pos"))
# dummyList.append(Contact("tyler", "1", "matthew.lee2304@gmail.com", "ex company", "ex pos"))


#2880 x 1800
# img width: 135 px height: 135 px
# name size: 16 px line height: 23.04px
# title size: 10.6667px line height: 15.36px
# email size: 14.6667px line height: 21.12px
# phone #: 14.6667px line height: 21.12px

# body text: 13 px