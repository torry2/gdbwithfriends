import gdb
import atexit
import requests
import psutil
import time

#CHANGE PATH FILE THING
path_to_file = '' # e.g /home/torry/time.file (MUST BE "time.file")

name = '<name>'
webhook = 'https://discord.com/api/webhooks/<webhook>'
timer = None

class gdbwithfriends(gdb.Command):
    def __init__(self):
        gdbs = 0
        for process in psutil.process_iter(attrs=['pid', 'name']):
                if process.info['name'] == 'gdb':
                    gdbs += 1
        if gdbs > 1:
            gdb.write("GDBWF: GDB is already running, not attaching... (0)\n")
            exit(0)
        try:
            self.startup()
        except Exception as e:
            exit(-1)
        atexit.register(self.shutdown)
        super(gdbwithfriends, self).__init__("gdbwithfriends", gdb.COMMAND_USER)

    def alsopost(self):
        data = {
    "content" : f"I've opened GDB!",
    "username" : name
}
        requests.post(webhook, json=data)     

    def post(self, session, total):
        data = {
    "content" : f"I've exited GDB!\nElapsed Session: {round(session, 2)} (s) \nElapsed Total: {round(total, 2)} (s)",
    "username" : name
}
        requests.post(webhook, json=data)

    def shutdown(self):
        global timer
        if timer is not None:
            elapsed = time.time() - timer

        with open(path_to_file, "r") as f:
            thetotal = f.read()
            if thetotal == '':
                thetotal = 0
        tt = elapsed + float(thetotal)
        #print(tt)  
        with open(path_to_file, "w") as ff:
            ff.write(str(tt))      
        self.post(elapsed, tt)
        gdb.write(f"GDBWF: gdbwithfriends stopped!\n\tElapsed Session: {round(elapsed, 2)} (s)\n\tElapsed Total: {round(tt, 2)} (s)\n")

    def startup(self):
        global timer
        timer = time.time()
        self.alsopost()
        gdb.write(f"GDBWF: gdbwithfriends started!\n")

    def invoke(self, arg, from_tty):
        args = arg.split()
        
        if len(args) == 0:
            gdb.write("GDBWF: gdbwithfriends <command> [arguments]\n")
        elif args[0] == "help":
            self.help(args[1:])
        elif args[0] == "time":
            self.time(args[1:])
        else:
            gdb.write(f"GDBWF: Unknown command: {args[0]}\n")

    def help(self, args):
        gdb.write("GDBWF: Help \ncommands -  <help>, <time>\n")

    def time(self, args):
        global timer
        tmpelapsed = time.time() - timer
        with open(path_to_file, "r") as f:
            thetotal = f.read()
        total = tmpelapsed + float(thetotal)
        gdb.write(f"GDBWF: Time\n\tElapsed Session: {round(tmpelapsed, 2)} (s)\n\tElapsed Total: {round(total, 2)} (s)\n")

plugin = gdbwithfriends()

