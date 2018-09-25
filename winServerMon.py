'''
Program initially written to check on the functionality of Solarwinds servers.

It can be used to check any Windows machine for services running
                                
All config for this program is done in the settings.ini file for 
general settings and in the servers.ini file for server settings
'''

import os
import cmd
import wmi
import time
import shutil
import sys
import socket
import win32wnet
import slogSender

import configparser

from sendEmail import Email
from subprocess import check_output
from socket import *
from test.libregrtest.runtest import FAILED

# Get program vars
config = configparser.ConfigParser()
config.read('settings.ini')

# Get server info from servers.ini
srvsConf = configparser.ConfigParser()
srvsConf.read('servers.ini')

# Sleep time between running frm settings.ini
delayedRun= int(config['general']['frequency'])

# Email variables from settings.ini
recvrStr = config['email']['receivers']
receivers = [n.strip() for n in recvrStr.split(",")]
sender = config['email']['sender'] # Email sender
mailSrv = config['email']['smtpServer'] # Email server

# Primary Service Account
username = config['srvcAcct']['username']
password = config['srvcAcct']['password']

# Syslog server from settings.ini
logServer = config['general']['logServer']

mail = Email() # Instantiate email func


# Ping check.  Takes IP or hostname as arg
def ping(host):
    ''' Try and if status is not 0 then return false '''
    try:
        shellOutput = check_output("ping " + host + " -n 2", shell=True)
    except:
        return False

    # If ping is successful check for 'unreachable' in string. If
    #           'unreachable' exists, do not return true
    
    if shellOutput:
        shellOutput = shellOutput.decode()
        if 'unreachable' not in shellOutput:
            return True



# Checking if servers are live. 
def checkSrvPing(srvNm, srvIp):

    if  ping(srvIp):
        print(srvNm + " is reachable at " + srvIp)
    else:

        noPingText = ('{} at {} is unreachable. Please check on its connectivity.'
                      .format(k, v))
        
        
        mail.mailSender('mxsb.tn.gov', sender, receivers,
                        "Service down", noPingText)

        graylogError = ("Pings Timed Out!! " + noPingText)
        slogSender.sendLogs('Solarwinds error - {} {} DOWN'
                            .format(k, v), graylogError, logServer)


'''
 The function below checks on the status of critical services for each one of
 SolarWinds servers. If the service is down, it's going to generate an alert
 or notify an administrator, reporting the server and service names.

 And if the service account can't remote in for whichever reason, the function
 will generate an email to the administrator giving the exact reason
 preventing a successful login to check on the services' state.
'''


def serviceChk(serverNm, serverIp, usernm, passwd, serviceName):
    print('Connecting to {}'.format(serverNm))

    try:
        pyWMI = wmi.WMI(serverIp, user=usernm, password=passwd)

    # If we can't connect to the server, send a log message of
    # the error preventing to connect to the graylog server;
    #            most likely RDP not available.
    

    except wmi.x_wmi as x:
        wmiError = x.com_error.excepinfo[2]

        errRetrnd = ("Failure: " + wmiError)

        rdpError = ('''Connection to {} {} FAILED!\n\nReason: {}
                    \nPlease make sure that the server is available.'''
                    . format(serverNm, serverIp, wmiError))


        mail.mailSender("mxsb.tn.gov", sender, receivers,
                        "SERVER DOWN", rdpError)

        # Logging the error to graylog server via UDP. 
        graylogError = ("Unable to connect!! " + rdpError)
        slogSender.sendLogs('Solarwinds error - {} {} UNABLE TO CONNECT!!'
                            .format(serverNm, serverIp), graylogError, logServer)
        
        print(errRetrnd)
        return errRetrnd

    # Checking if the service is started and running. 
    for service in pyWMI.Win32_Service(Name=serviceName):
       
        if service.State == 'Running':
            print("Service status: " + service.State)
        else:
           
            # Email message sent to user 
            svcDownText = ('{} on {} {} is {}. \nPlease restart this critical service.'
                           .format(serviceName, serverNm, serverIp, service.State))

            # Call email function
            mail.mailSender("mxsb.tn.gov", sender, receivers, "Service down", svcDownText)

            # Logging the error to graylog server via UDP. 
            graylogError = ("Service DOWN!! " + svcDownText)
            slogSender.sendLogs('''Solarwinds error - Service {} DOWN!!'''
                                .format(serviceName), graylogError, logServer)


def checkAll():
    for serverNm in srvsConf.sections():
    
        #Convert services string to list
        srvcsStr = srvsConf[serverNm]['services']
        chkSrvices = [n.strip() for n in srvcsStr.split(",")]
       
        serverIp = srvsConf[serverNm]['host'] # Get server ip from servers.ini
        
        checkSrvPing(serverNm, serverIp)
        
        # Get server user from servers.ini
        usernm = (srvsConf[serverNm]['username'])
        # Check if username is defined in servers.ini. Else use settings.ini usr 
        if not usernm: usernm = config['srvcAcct']['username']
        
        # Get server password from servers.ini
        passwrd = (srvsConf[serverNm]['password'])
        # Check if username is defined in servers.ini. Else use settings.ini user 
        if not passwrd: password = config['srvcAcct']['password']
        
        # Check each service
        for srvc in chkSrvices:
            print("Checking {} on {}.".format(srvc, serverNm))
            
            # Run service checking function
            print(serverNm, serverIp, username, password, srvc)
            serviceChk(serverNm, serverIp, username, password, srvc)

def main():
    while True:
        
        print("Program begins\n\n")
        # Check servers for ping and services running
        checkAll()
        print("\nProgram sleeping for {}".format(str(delayedRun)))
        # Second between checks 
        time.sleep(delayedRun)

if __name__ == '__main__':
    main()