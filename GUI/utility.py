# All code written and reserved by and for Deltaion Lee
# To violate these rights is to break the law
# Use is not prohibited, but claiming as own/redistributing is illegal
# Altering the intellectual property is allowed, but do not claim as your own
# Instead, put your name here:
# I, <your_name>, have made changes to Deltaion Lee's code with or without his
# explicit permission, and will face the consequences if the code is abused.

# Thank you for your cooperation.

import time, os
from sys import platform

def checkdir(path):
    if os.path.isdir(path):
        return True
    os.mkdir(path)
    return False

def open_folder(str = ".",OS = platform):
    if OS.startswith("darwin"):
        str = f"open {str}"
    elif OS.startswith("win"):
        str = f"start {str}"
    else:
        str = f"./{str}"
    os.system(str)

class File():

    default = "Write not specified"

    def __init__(self,file = f"{__name__}.py"):
        self.file = file
        self.buffer = None

    def read(self):
        with open(self.file,"r") as file:
            return file.read()

    def read_bytes(self):
        with open(self.file,"rb") as file:
            return file.read()

    def set_buffer(self,buffer = None):
        if not buffer:
            self.buffer = self.read()
            return self.buffer
        self.buffer = buffer
        return self.buffer

    def read_buffer(self):
        return self.buffer

    def write_bytes(self,content):
        with open(self.file,"wb") as file:
            file.write(content)

    def append_bytes(self,content):
        with open(self.file,"ab") as file:
            file.write(content)

    def overwrite(self,content = default):
        with open(self.file,"w") as file:
            file.write(content)

    def write(self,content = default):
        self.overwrite(content)

    def append(self,content = default):
        with open(self.file,"a") as file:
            file.write(content)

    def char_count(self):
        return len(self.read())

    def word_count(self):
        return len(self.read().split())

    def readlines(self):
        return self.read().split("\n")

    def readline(self,n:int):
        i = 0
        for line in self.readlines():
            i += 1
            if i == n:
                return line
        return None

    def find(self,search:str="None",case_sensitive:bool=False,whole_line:bool=False):
        list = []
        n = 0
        failed = True
        if not case_sensitive:
            _search = search.lower()
        else:
            _search = search
        for line in self.readlines():
            c = 0
            n += 1
            i = 0
            if not case_sensitive:
                _line = line.lower()
            else:
                _line = line
            if _search in _line:
                if whole_line:
                    list.append(line)
                else:
                    for char in _line:
                        c += 1
                        if not failed and i == len(search):
                            list.append(f"Line {n}, column {c - i}")
                            i = 0
                            failed = True
                        else:
                            if char[0] == _search[i]:
                                failed = False
                                i += 1
                            else:
                                i = 0
                                failed = True

        return list

class Timer():
    def __init__(self):
        self.start_time = time.time()
        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True
        return

    def get(self,point = 10):
        if self.running:
            return round(time.time() - self.start_time,point)
        else:
            return False

    def delay(self,limit = 60,Delay=True):
        elapsedTime = self.get(5)
        if elapsedTime < 1 / limit and Delay:
            time.sleep(1/limit-elapsedTime)
        return 1/limit-elapsedTime

    def stop(self):
        self.running = False

# Optionally define a framelimit other than the default of 60 fps with object.delay(fps)
