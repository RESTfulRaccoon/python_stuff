import paramiko
from subprocess import run, PIPE
from sys import argv
from time import sleep
from pathlib import Path
user= argv[1]
host = argv[2]
trop = argv[3] #port
key = str(Path.home()) +"/.ssh/"+str(argv[4])
command=argv[5]
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user,port=trop, key_filename=key)
channel = client.invoke_shell()
channel.recv(99999)
channel.send('\n')
sleep(1)
channel.recv(9999)
def ssh(c):
    su = False
    s = c.split(" ")
    if s[0] == 'sudo':
        sudo = True
    else:
        sudo = False
    if su:
        channel.send(c+' \n')
        sleep(0.1)
        m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    if sudo:
        channel.send('sudo whoami \n')
        sleep(0.1)
        channel.send(supass)
        sleep(0.1)
        channel.send('\n')
        sleep(0.1)
        r = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
        if 'root' not in r[1]:
            channel.send('sudo whoami \n')
            sleep(0.1)
            channel.send(supass)
            sleep(0.1)
            channel.send('\n')
            sleep(0.1)
            r = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
            if 'sudo: command not found' or 'root' not in r[1]:
                s.pop(0)
                c = ""
                for w in s:
                    c+=w+" "
                channel.send('su - \n')
                sleep(0.1)
                channel.send(pw)
                sleep(0.1)
                channel.send('\n')
                sleep(0.1)
                channel.recv(99999)
                channel.send('whoami \n')
                sleep(0.1)
                r = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
                if 'root' not in r[1]:
                    channel.send('su - \n')
                    sleep(0.1)
                    channel.send(pw)
                    sleep(0.1)
                    channel.send('\n')
                    sleep(0.1)
                    channel.recv(99999)
                    channel.send('whoami \n')
                    sleep(0.1)
                    r = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
                    if 'root' not in r[1]:
                        print("ERROR: COULD NOT GAIN ELIVATED PRIVLAGES")
                else: su = True
                channel.send(c+' \n')
                sleep(0.1)
        else:
            channel.send(c+' \n')
            sleep(0.1)
        m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    channel.send(c+' \n')
    sleep(0.1)
    m = channel.recv(99999).decode('utf-8').replace('\r','').split('\n')
    for s in m:
        if s == m[0]:
            pass
        elif s== m[-1]:
            pass
        else:
            print(s)
ssh(command)
client.close()

#figure out how to keep the shell open making it more of a stream.
#probably just need to make something like while (open) do ssh()