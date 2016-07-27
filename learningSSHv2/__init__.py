#!/usr/bin/env python

import paramiko
import time
import re
import sys

#Open SSHv2 connection to devices
def open_ssh_conn(ip):
    #change exception message
    try:
        #Defining the credentials file
        user_file = sys.argv[1]
        #Defining the commands file
        cmd_file = sys.argv[2]
        #Define SSH parameters
        selected_user_file = open(user_file, 'r')
        #starting from the beginning of the file
        selected_user_file.seek(0)
        #reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0]
        #starting from the beginning of the file
        selected_user_file.seek(0)
        #reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        #Logging into device
        session = paramiko.SSHClient()

        #for testing purposes, this allows auto-accepting unknown host keys
        #note that this must not be used in production! the default would be RejectPolicy then
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #connect to the device using username and password
        session.connect(ip,username = username, password = password)
        #start an interactive shell session on the router
        connection = session.invoke_shell()
        #setting terminal length for entire output - disable pagination
        connection.send("terminal length 0\n")
        time.sleep(1)
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        #open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
        #starting from the beginning of the file
        selected_cmd_file.seek(0)
        #writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        #closing the user file
        selected_user_file.close()
        #closing the command file
        selected_cmd_file.close()

        #expect to receive a maximum of 65535 bytes of data and store it in a variable
        router_output = connection.recv(65535)

        #checking command output for IOS syntax errors
        if re.search(r"% Invalid input detected at" , router_output):
            print("* there was at least one IOS syntax error on device %s" % ip)
        else:
            print("\nDONE for device %s" % ip)

        #Test for reading command output
            print(router_output + "\n")
            #closing the connection (ssh session)
            session.close()
    except paramiko.AuthenticationException:
        print("* Invalid username or password. \n* Please check the username/password file or the device configuration!")
        print("*Closing program..\n")

#calling the SSH function
open_ssh_conn("192.168.2.101")

