import socket
import datetime
import time



monthDict = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
            "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
            "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

#prepare dict in GELF format
def processLogs(shortMesg, fullMesg):
    gelfDict = {
                #"version": "1.1",
                "host": socket.gethostname(), #get hostname of sending host
                "short_message": shortMesg,
                "full_message": fullMesg,
                "timestamp": int(time.time()), 
                }

    return gelfDict

#Sends logs to graylog via UDP
def sendLogs(shortMesg, fullMesg, slogServer):
    
    #Instantiate socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    logMesgProc = processLogs(shortMesg, fullMesg)
    logMesgStr = str(logMesgProc)
        
    logMesg = logMesgStr.replace("'", '"') #Replace ' with " in JSON for GELF
    # print(logMesg) #Print data to being sent to graylog
    
    #Send log via UDP 12201 to graylog using GELF format. Enc to UTF8 first
    #sock.sendto(logMesg.encode('utf-8'), (slogServer, 12201))
    sock.sendto(logMesg.encode('utf-8'), (slogServer, 12201))
    
    
def main():
    sendLogs()


if __name__ == "__main__":
    main()