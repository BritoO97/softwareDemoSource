#!/usr/bin/python3

# NOTE: DESTINATION EMAIL AND SMTP LOGIN CREDENTIALS HAVE BEEN REDACTED FROM THIS SCRIPT FOR PRIVACY AND SECURITY
# 		IT WILL NOT WORK WITHOUT THEM

import sys
import smtplib
import datetime

# destination emails
to =["REDACTED"]

# email subject line (ends up being unused since the smtplib package does not support message subjects)
subject = "Daily Steam Scraper"

# the input file name
filename = "results"
f = open(filename, "r")

# the data that is read from the input file and will eventually be the email body
msg = f.read()

f.close()

# ensuring the data is utf-8 encoded to avoid problems
msg = msg.encode("utf-8")

# i use the gmail smtp server as provided by google, and there are the gmail credentials needed to access the server
gmailSender = "REDACTED"
gmailPass = "REDACTED"

# create a connection to the gmail smtp server
server = smtplib.SMTP("smtp.gmail.com", 587)

server.ehlo()
server.starttls()
server.ehlo()

# login to the gmail account using the credentials established before
server.login(gmailSender, gmailPass)

# open log file
log = open("log", "a")

# loop over the emails in the to list
# while an email can take a list as a destination field, this would allow any receiver to see who else received the email
# by sending out multiple emails this is avoided (though this is only viable when the to list is small)
for email in to:

	# attempt to send an email and log results
    try:
        server.sendmail(gmailSender, [email], msg)
        log.write("success email on: " + str(datetime.datetime.now()) + "\n")
    except:
        log.write("error email  on: " + str(datetime.datetime.now()) + "\n")

# close the log file
log.close()

# close the smtp server connection
server.quit()
