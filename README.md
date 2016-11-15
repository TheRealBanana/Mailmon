# Mailmon
Crappy email auto-responder bot

Mailmon will read incoming emails looking for certain commands and execute a specific script based on the command it finds, making a very basic auto-responder bot.


There are two versions here, one older one in bash and a newer one in Python. If you know how to program in python, I highly recommend you use that version. This readme will mostly apply to the python version, as the bash version is very simple and shouldn't require much explanation beyond the comments already inside mailmon.sh.


First off to use either of these scripts requires you make a file called .forward in the home directory of the user receiving the emails. So in our example that user is mailmon, we would make the file:

>/home/mailmon/.forward

And inside we add the following (change the folder paths to your requirements):

>/home/mailmon/data/mail.txt,"|/home/mailmon/mailmon.sh"

Make sure you adjust the path to where the mail.txt is written to in the script options. After that you must open up mailmon.sh or mailmon2.py and adjust the settings inside.

In mailmon.sh there are only two options to adjust, the path to mail.txt and the username who is running the script.

In mailmon2.py there are 5 options to adjust:

FROM_ADDRESS - This is the email address that will be used as the From: address in any return emails mailmon sends.

path - This is the dir path to the folder where mail.txt is being output to. See the section about .forward above for more help.

authorized_emails - This is a list of email addresses that are authorized to use the bot. If you want anyone to be able to use the bot, add ALLOW_ALL to the list.

cmdlist - This is a list of the commands the bot knows. This just affects the help output, the command will still run even if it’s not in the list.

MASTER_RATIO - This affects the matching system used when an unknown command is encountered. Mailmon will attempt to match the unknown command against cmdlist and suggest the proper command if it finds it. This number adjusts the sensitivity of the matcher with higher numbers being more restrictive. A value of 0.75 is the default and works well in most situations.


After adjusting the options make sure you chmod +x the mailmon.sh or mailmon2.py files and you are ready to go! Send out a test email to confirm everything is working.


Future ideas:
*	Update mailmon2 to use smtplib instead of relying on an external mail command.
*	Update the command system to look for scripts in a directory instead of requiring python code. This will allow users to point mailmon2 to a specific folder where mailmon2 will match the file names of scripts against the command sent. It will then execute the script if it matches, returning the script output in the return email. This will give much greater flexibility for users who don't know python.


Enjoy!
