from pythonping import ping
import time
import smtplib, ssl
from socket import gaierror
from email.mime.text import MIMEText


EMAIL = '...@gmail.com'
APP_PASSWORD = '...'

quitint = 0

def main():

   
    camIpDocument = open("IpAddresses.txt","r")
    hostsList = str(camIpDocument.read())
    hostsList = hostsList.rstrip()
    #split string into list from commas
    HOSTS = list(hostsList.split(","))
    camIpDocument.close()

    
    nameDocument = open("Name.txt","r")
    hostsNames = str(nameDocument.read())
    hostsNames = hostsNames.rstrip()
    #split cam names into list
    cameraNames = list(hostsNames.split(","))
    nameDocument.close()
    ############################################
    emailDocument = open("EmailAddresses.txt","r")
    emailNames = str(emailDocument.read())
    emailNames = emailNames.rstrip()
    
    emailAddressList = list(emailNames.split(","))
    emailDocument.close()
    ############################################

    
    Ping_Test(HOSTS,cameraNames,emailAddressList)
def Ping_Test(hosts,camHostName,recipients):
    
    i = 0
    while i < len(hosts):
        response = ping(hosts[i], verbose=True)
        if 'Request timed out' in str(response):
            #if request times out send email
            Send_Email(hosts[i],camHostName[i],recipients)

        time.sleep(5)
        i+=1
    

def Send_Email(ip,name,receiver):
    global quitint
    quitint +=1
    SUBJECT = "Server down"
    TEXT = ("One of your servers is offline\nName: %s\nIP-address: %s\nB)" 
        % ( name, ip))
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, receiver, msg)
        server.close()

        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')
    
    
def loop():
    global quitint
    main()
    if quitint < 1:
        print('Sleeping for 1/2 hour...')
        time.sleep(3600)
        loop()
    if quitint > 1:
        quitint = 0
        print('Sleeping for a day...')
        time.sleep(86400)
        loop()
        
loop()
