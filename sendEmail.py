import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class Email:
    
    def mailSender(self, mailServer, sender, receivers, subjeMsg, msgBody, fileAttchmnt=None, srvPort=25):
        
        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        
        # Create a text/plain message
        # msg = MIMEText("Here's your {} report you requested at {} from {}" .format(reportName, timeStamp, siteUrl))
        
       
        msg = MIMEText(msgBody)
        
        msg['Subject'] = '{} - ATTENTION REQUIRED!!!' .format(subjeMsg)
        msg['From'] = sender
        msg['To'] = ", ".join(receivers)
               
        #=======================================================================
        # Code below is only used if we need to attach something.
        #=======================================================================
        if fileAttchmnt:
            msg = MIMEMultipart()
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(fileAttchmnt, "rb").read())
            encoders.encode_base64(part)
        
            part.add_header('Content-Disposition', 'attachment; filename=' + fileAttchmnt + '')
        
            msg.attach(part)
        
        #===============================================================================
        # State of TN SMTP server
        #===============================================================================
        
        s = smtplib.SMTP(mailServer, port=srvPort)
        s.sendmail(sender, receivers, msg.as_string())
        s.close()

