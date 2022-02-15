import os
from ftplib import FTP

class Switch():
    def __init__(self,ipaddr:str='127.0.0.1',port:int=5000,path:str='scripts'):
        self.switch = FTP()
        self.switch.connect(ipaddr,port)
        self.switch.login(user='PyTAS Editor',passwd='Password')
        self.switch.cwd(path)

    def uploadFile(self,name:str,data:str):
        temp = './' + '_temp.' + name
        with open(temp,'w') as file:
            file.write(data)
        with open(temp,'rb') as file:
            self.switch.storbinary('STOR ' + name,file)
        os.remove(temp)

    def retrieveFile(self,name:str):
        temp = './' + '_temp.' + name
        with open(temp,'wb') as file:
            self.switch.retrbinary('RETR ' + name, file.write)
        with open(temp,'r') as file:
            data = file.read()
        os.remove(temp)
        return data
