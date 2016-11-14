#!/bin/env python2.7
# Mailmon v2.0 by Kyle Claisse
# This script reads in an email in text form and executes certain functions based on the content of the message.
#
# Current requires a working MTA and the mail command on the box this bot is running (I use Heirloom Mail v12.4)
# Probably should rewrite to use the smtplib python library but I never needed to. Would be trivial to rewrite to
# allow using third-party SMTP servers like gmail. Something for version 2.1 I guess.


import email
import re
from time import strftime
import os
from subprocess import check_output as sp_co
from difflib import SequenceMatcher as sMatcher



#######################
#### OPTIONS START ####
#######################

#This is the email address the autoresponder bot will use for the From: address in its return email.
FROM_ADDRESS = "mailmon@example.com"

#This is the path where the mail.txt is being output to. See readme for details.
path = "/home/mailmon/data"


#Approved email addresses. Only approved addresses can use this bot. Just add your approved emails to this list like in the example.
#If you want to allow anyone to use this bot, just add ALLOW_ALL.
authorized_emails = []
authorized_emails.append("authorized_person@example.com")
authorized_emails.append("another_authorized_person@example.com")


#This is the list of commands. If you don't add your command to this list it won't appear in any help messages.
cmdlist = []
cmdlist.append("uptime")
cmdlist.append("whos-logged-in")


#When an unknown command is received it will try to match the unknown command against the command list.
#This controls the sensitivity of the matcher, a higher number is more restrictive matching.
#0.75 is a good value to keep it at.
_MASTER_RATIO_ = 0.75


#These you don't need to change (unless you know what you are doing)
emf = path + os.sep + "mail.txt"
outfile = path + os.sep + "out.txt"

#####################
#### OPTIONS END ####
#####################






def check_address(addy):
    for x in authorized_emails:
        if x == "ALLOW_ALL":
            return True
        if x == addy:
            return True
    return False


def main():    
    return_message = "UNKNOWN ERROR, RETURN EMAIL NOT SET"
    
    email_file = open(emf, 'r')
    msgobj = email.message_from_file(email_file)
    email_file.close()
    if msgobj.is_multipart() is False:
        message = msgobj.get_payload()
        
    return_addy = msgobj.__getitem__("from")
    
    #We lower the received message to make matching easier
    nmsg = message.lower().strip()
    
    #FOR DEBUGGING!
    pq = open(path + os.sep + "mailmon_use.log", 'a')
    log_message = str(strftime("%A %B %d, %Y - %r %Z")) + " :: " + return_addy + " :: " + nmsg
    pq.write(log_message)
    pq.write("\n")
    pq.close()
    
    if check_address(return_addy) is not True:
        return_message = "You are not authorized to use this service. Your previous and future messages will be logged."
    
    #############################
    #### COMMANDS START HERE ####
    #############################
    
    
    elif "hi" in nmsg or "hello" in nmsg or "hey" in nmsg:
        return_message = "Hello there! The current time here is: " + str(strftime("%A %B %d, %Y - %r %Z"))
   
    elif nmsg == "uptime":
        uptime = sp_co('''uptime | egrep "([0-9][0-9]:?){3}.up.[0-9]{1,4}.days?" -o''', shell=True)
        return_message = "Current system uptime is: " + uptime.strip()
    
    elif nmsg == "whos-logged-in":
        try:
            last_raw = sp_co("last -w -F | grep logged", shell=True).strip()
        except:
            last_raw = ""
        last_list = re.split("\n", last_raw)
        return_message = "There are currently %s users logged in%s"
        num = 0
        for entry in last_list:
            entry = entry.strip()
            line_match = re.match("^(.*?)\s+(.*?)\s+(.*?)\s+.*$", entry)
            if line_match is not None:
                num += 1
                return_message += "\n%s from %s" % (line_match.group(1), line_match.group(3))
        if num == 0:
            return_message = return_message % (str(num), "")
        else:
            return_message = return_message % (str(num), ":")
        
    #############################################
    #### ADD MORE COMMANDS BELOW USING ELIFS ####
    #############################################
   
    elif "help" in nmsg:
        cmdstr = "%s" % (cmdlist[3],)
        for cmd in cmdlist[4:]:
            cmdstr += ", " + cmd
        return_message = "List of commands: %s" % cmdstr
    
    else:
        return_message = "Unknown command, %s." % str(nmsg)
        
        #Try and match the failed command to a known command
        for cmd in cmdlist:
            if sMatcher(None, nmsg.lower(), cmd).ratio() > _MASTER_RATIO_:
                return_message += " Did you mean %s? " % cmd
                break

        return_message += " Reply with 'help' for a list of commands."
    send_email(return_message, return_addy)
    
    
def send_email(message, to_address):
    if len(message) < 1:
        return
    #Remove file first
    
    try:
        os.remove(outfile)
    except:
        pass
    
    ofile = open(outfile, 'w')
    ofile.write(message)
    ofile.close()
    
    #Check if we have a good return email
    if "ERROR" not in to_address:
        #Send email out
        cmd = "mail -r %s %s < %s" % (FROM_ADDRESS, to_address, outfile)
        os.system(cmd)
    else:
        #Write the error to the log
        pq = open(path + os.sep + "mailmon_use.log", 'a')
        log_message = str(strftime("%A %B %d, %Y - %r %Z")) + " :: " + to_address
        pq.write(log_message)
        pq.write("\n")
        pq.close()
    
    
    #Remove both email files
    try:
        os.remove(outfile)
    except:
        pass
    
    try:
        os.remove(emf)
    except:
        pass
    
if __name__ == "__main__":
    main()

