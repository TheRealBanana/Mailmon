#!/bin/bash
# Mailmon v1.0 by Kyle Claisse
# This script reads in an email in text form and executes certain functions based on the content of the message.
#
# This bash script was cobbled together quickly with no thought to how anyone else would use it so its not the best.
# I rewrote this in python which is much easier to work with if you know python. See mailmon2.py


#Path to where the mail.txt is being written
dPATH=/home/mailmon/data

#The username receiving the emails
user_name="mailmon"






from=$(cat $dPATH/mail.txt | grep From: | grep -v Message-ID | grep -v Return-Path:| egrep "[a-zA-Z0-9_.-]+@([a-zA-Z0-9-]+\.){1,}([a-zA-Z]){2,4}" -o|grep -v $user_name)

if [ -z "$from" ]
then
	exit 0
fi

for line in `cat $dPATH/mail.txt`
do
	case $line in

		uptime|Uptime ) 
		UP=$(uptime | egrep "([0-9][0-9]:?){3}.up.[0-9]{1,4}.(days)?" -o)
		echo $UP > $dPATH/out.txt
		;;

		hi|Hi|hello|Hello|sup|Sup|hola|Hola|hai|Hai|hey|Hey ) echo "Hai thar!" > $dPATH/out.txt 
		;;
		

		help|Help ) echo -e "The following commands are accepted by StatusBot:\n\n uptime help. Case DOES matter, only first char capitalization is acceptable." > $dPATH/out.txt
		;;

		* ) echo -e "Unknown command, try again.\nFor a list of available commands, send the word \"help\" (no quotes)" > $dPATH/out.txt
		;;

		esac
done


mail $from < $dPATH/out.txt
#echo $from >> $dPATH/debug.txt
rm -f $dPATH/out.txt
rm -f $dPATH/mail.txt
exit 0
