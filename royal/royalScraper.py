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
from email.mime.base import MIMEBase
from email import encoders
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

def tab():
    pyautogui.press('tab')

def enter():
    pyautogui.press('enter')

senderEmail = input("enter email: ")
senderPassword = input("enter password: ")
emailFilePath = "royal/sent-email-list.txt"
contactFilePath = "royal/contact-added-list.txt"
inX = 1000
resMultiplier = 0.5

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
    if (len(coAndPos) < 2):
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
emailFileRead = open(emailFilePath, "r")
while True:
    currContact = emailFileRead.readline().strip()
    if(currContact == ""):
        break
    sentEmails.add(currContact)
emailFileRead.close()
contactFileRead = open(contactFilePath, "r")
while True:
    currContact = contactFileRead.readline().strip()
    if(currContact == ""):
        break
    companiesAdded.add(currContact)
contactFileRead.close()


context = ssl.create_default_context()
with open(emailFilePath, "a") as emailFile:
    with open(contactFilePath, "a") as contactFile:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(senderEmail, senderPassword)
            pyautogui.alert("switch to hubspot tab to begin program")
            time.sleep(1)
            pyautogui.click(clicks=2, x=1327, y=197)
            for contact in contactList:
                if(contact.company in companiesAdded):
                    print(f"{contact.company} is already a contact")
                    continue
                
                companiesAdded.add(contact.company)
                time.sleep(2.2)
                pyautogui.click(clicks=2, x=inX, y=269)
                pyautogui.write(contact.email)
                tab()
                pyautogui.write(contact.firstName)
                tab()
                pyautogui.write(contact.lastName)
                # conf = pyautogui.confirm("Add contact?", "Check", ["Yes", "No"])
                conf = input("Add contact?\n")
                conf = conf.strip().lower()
                if(not (conf == 'y' or conf == 'yes')):
                    pyautogui.click(clicks=2, x=1405, y=146)
                    time.sleep(1.5)
                    pyautogui.click(1327, 197)
                    contactFile.write(f"{contact.company}\n")
                    continue
                contactFile.write(f"{contact.company}\n")
                pyautogui.click(clicks=2, x=inX, y=536)
                pyautogui.write(contact.position)
                tab()
                pyautogui.write(contact.company)
                tab()
                # City
                pyautogui.write("n/a")
                tab()
                enter()
                # State
                pyautogui.write("n/a")
                enter()
                tab()
                enter()
                # Country
                pyautogui.write("n/a")
                enter()
                # pyautogui.moveTo(1133, 481)
                # pyautogui.scroll(-2000)
                tab()
                tab()
                enter()
                # Industry
                pyautogui.write("technology")
                enter()
                tab()
                enter()
                # Sub-Industry
                pyautogui.write("it service")
                enter()
                pyautogui.press('esc')
                tab()
                tab()
                enter()
                # Project
                pyautogui.write("royal")
                enter()
                pyautogui.press('esc')
                time.sleep(0.5)
                pyautogui.moveTo(1082, 799)
                time.sleep(0.4)
                pyautogui.click()
                if(contact.email in sentEmails):
                    print(f"{contact.email} has already been sent an email")
                    continue
                # emailConfirm = pyautogui.confirm(f"Send email to {contact.firstName} {contact.lastName} at {contact.company}? ({contact.email})", "Email Confirmation", ["Yes", "No"])
                # emailConfirm = input(f"Send email to {contact.firstName} {contact.lastName} at {contact.company}? ({contact.email})\n")
                # emailConfirm = emailConfirm.strip().lower()
                # if(not (emailConfirm == 'y' or emailConfirm == 'yes')):
                #     continue
                recipient = contact.email
                # subjectLine = "Subject: Interested Buyer for " + contact.company + "\n"
                subject = "Interested Buyer for " + contact.company
                html_content = f"""
                <html>
                <body style="font-family: Arial;">
                <p>Hi {contact.firstName},</p>
                <p><a href='https://www.sellsidegroup.com/'>Sellside Group</a> is representing a buyer interested in investing in B2B software and Tech-enabled services firms. I think {contact.company} may be a great fit.</p>
                <p>It would be great to set up a brief meeting with our tech practice lead, <a href='https://www.linkedin.com/in/paul-muckleston-11785a3/'>Paul Muckleston</a>, former 20+ yr Microsoft Executive, to discuss this opportunity in greater detail.</p>
                <p>Please let me know a few dates and times that work best for you and I will coordinate schedules and get Zoom invites sent out.</p>
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
                with open("royal/sellside-logo.jpg", 'rb') as img:
                    mime_img = MIMEImage(img.read())
                    mime_img.add_header('Content-ID', '<image1>')
                    msg.attach(mime_img)
                part = MIMEBase('application', "octet-stream")
                filename = "royal/Project_Royal_Overview.pdf"
                with open(filename, 'rb') as pdf:
                    part.set_payload(pdf.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

                emailFile.write(f"{contact.email}\n")
                smtp.sendmail(senderEmail, recipient, msg.as_string())
                print(f"Email sent to {contact.email}")

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