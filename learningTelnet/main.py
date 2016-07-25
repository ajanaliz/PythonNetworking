#!/usr/bin/env python
import telnetlib, time


# Open telnet connection to devices
def open_telnet_conn(ip):
    # Change exception message
    try:
        # Define telnet parameters
        username = 'teopy'
        password = 'python'

        cmd_file = input("enter command file name and extension: ")

        TELNET_PORT = 23
        # Specify the connection timeout in seconds for blocking operations, like the connection attempt
        TELNET_CONNECTION_TIMEOUT = 5

        # Specify a timeout in seconds. Read until the string is found or until the timeout has passed
        READ_TIMEOUT = 5
        # Logging into device
        connection = telnetlib.Telnet(ip, TELNET_PORT, TELNET_CONNECTION_TIMEOUT)
        # waiting to be asked for a username
        router_output = connection.read_until("Username:", READ_TIMEOUT)
        # enter the username when asked and a '\n' for enter
        connection.write(username + "\n")
        # waiting to be asked for a password
        router_output = connection.read_until("Password:", READ_TIMEOUT)
        # enter the password when asked and a '\n' for enter
        connection.write(password + "\n")
        # wait so that any delay that the router might generate while verifying the username and password we entered will be taken into account
        time.sleep(1)
        # Setting terminal length for entire output - disabling pagination
        connection.write("terminal length 0\n")
        time.sleep(1)
        # Entering global config mode
        connection.write("\n")
        connection.write("configure terminal\n")
        time.sleep(1)
        # Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
        # Starting from the beginning of the file
        selected_cmd_file.seek(0)
        # Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.write(each_line + '\n')
        time.sleep(1)
        # Closing the file
        selected_cmd_file.close()
        # Test for reading command output
        router_output = connection.read_very_eager()
        print (router_output)
        # Closing the connection
        connection.close()
    except IOError:
        print("Input parameter error! Please check username, password and file name.")


# Calling the Telnet function giving the routers ip address
open_telnet_conn('192.168.2.101')
