# winProcessMonitor
Python based windows process monitor.  Reports issues via syslog and/or email

## Monitor windows servers and processes

This was program created to monitor solarwinds or to monitor the monitoring system.
One hand washes the other.  It can be used to monitor any windows process.  
You can get notifications via SMTP or syslog(514 UDP only).  We had good luck with
MS Exchange and Graylog, but should work well with any SMTP and syslog server.

## Setup

You will need to clone from github and install 3 python libraries.  If run pip install -r requirements from the cloned dir.  You will need to have pip as a sys path or call it from the dir where it resides.

For example:

git clone https://github.com/cbabs/winProcessMonitor

cd winProcessMonitor

pip install -r requirements.txt

## Configure and run the app

You will need to edit two files.  The settings.ini and servers.ini files.
The settings file is where you put general settings such as creds, email
and syslog settings.  The servers.ini file is where you put in the servers
and processees you want to monitor.  You can also override some settings
based on the individual server, such as credentials. We chose to use an
ini file to make it familiar for Windows admins.

Once you have edited the ini files, you can run the program. 
Depending on you python setup changes how you run the program.  
Open powershell or a terminal window.  Go to the directory where the file is.  
Then run the command to have python execute the py file and make sure the
hosts.txt is present.  I have python installed in c:\python36\ so for me it would look

c:\tools\monitor>c:\python36\python.exe dnsResolver.py

A linux setup may look like this:

cbabcock@ubuntuMon:/usr/share/utils/winProcessMonitor$ /lib/bin/python36 ./dnsResolver.py

## Notes

If you find this app to be crucial you may want to monitor with a monitoring system
like solarWinds(one hand washes the other) or a powershell/bash script that is run
periodically with Windows Scheduler or crontab.

Please feel very welcome to make suggestion and/or reports issues.

Cbabs
