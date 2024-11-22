import paramiko
from sys import argv
from time import sleep
from pathlib import Path

user= argv[1]
host = argv[2]
port = argv[3]
key = str(Path.home()) +"/.ssh/"+argv[4]
command="whoami"
import paramiko
from time import sleep

##### /CP/ #####
#enter client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, key_filename=key,port=port)
channel = client.invoke_shell()
channel.recv(99999)
channel.send('\n')
sleep(1) 
channel.recv(99999)
supass = input("Enter Password: ")
def ssh(c): ## look over this again, it looks strange..
    #check if root already
    
    su = False
    sudo = False
    channel.send("whoami")
    sleep(0.1) 
    w = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    if "root" in w: 
         su = True
    s = c.replace('\r','').split('\n')
    if su:
        # if sudo in command remove sudo from command
        if s[0] == 'sudo':
            s.pop(0)
            channel.send(s+' \n')
            sleep(0.1)
        else:
            channel.send(c+" \n")
            sleep(0.1)
    # run sudo command if sudo
    if s[0].split(" ")[0] == "sudo":
        sudo = True
    if sudo and not su:
        sup = supass
        channel.send(c)
        m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
        if 'command not found' not in m:
            channel.send('su - \n')
            sleep(0.1)
            channel.send(sup)
            sleep(0.1)
            channel.send('\n')
            sleep(0.1)
            channel.recv(99999)
            channel.send('whoami \n')
            sleep(0.1)
            m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
            if 'root' not in m[1]:
                channel.send('su - \n')
                sleep(0.1)
                channel.send(sup)
                sleep(0.1)
                channel.send('\n')
                sleep(0.1)
                channel.recv(99999)
                channel.send('whoami \n')
                sleep(0.1)
                m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
                su = True
                c = ""
                for i in s:
                    j = i.split(" ")
                    j.pop(0)
                    for k in j:
                        c+=k
                if 'root' not in m[1]:
                    print("ERROR: COULD NOT GAIN ELIVATED PRIVLAGES")
                channel.send(c+' \n')
                sleep(0.1)
                m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    else:
        channel.send(c+' \n')
        sleep(0.1)
        m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    channel.send(c+' \n')
    sleep(0.1)
    m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    return m
##### /CP/ #####
while True:
    x= ssh(command)
    for i in x:
        if i == x[0]:
            pass
        elif i == x[-1]:
            pass
        else:
            print(i)
    command = input(x[-1])
    if command == "exit":
        print(f"Closing connection to {user}@{host}:{port}")
        client.close()
        print("Thanks for playing!")
        exit()
    elif "poweroff" or "shutdown" in command:
        print("Shutting down...")
        try:
            ssh(command)
        except OSError:
            print("Thanks for playing!")
            exit()
    elif "reboot":
        print("Rebooting...")
        try:
            ssh(command)
        except OSError:
            print("Thanks for playing!")
            exit()

    x = ssh(command)