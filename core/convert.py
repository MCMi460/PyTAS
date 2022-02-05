import os

class convert():
    def __init__(self):
        self.keys = (
        'NONE',
        'KEY_A',
        'KEY_B',
        'KEY_X',
        'KEY_Y',
        'KEY_L',
        'KEY_R',
        'KEY_ZL',
        'KEY_ZR',
        'KEY_PLUS',
        'KEY_MINUS',
        'KEY_DLEFT',
        'KEY_DUP',
        'KEY_DRIGHT',
        'KEY_DDOWN',
        'KEY_LSTICK',
        'KEY_RSTICK',
        )

    def justify(self,inputs:list):
        text = '# This is an auto-generated PyTAS file\ndef main():\n'
        char = '\''
        lastframe = 0
        try:
            for i in inputs:
                if not i:
                    continue
                i = i.split(' ')
                i = {
                'Frame':int(i[0]),
                'Key':i[1],
                'LeftStick':i[2],
                'RightStick':i[3],
                }
                if i['Key'] != 'NONE' or i['LeftStick'] != '0;0' or i['RightStick'] != '0;0':
                    text = f"{text}    script.input({i['Frame'] - lastframe},({','.join([ f'{char}{h}{char}' for h in i['Key'].split(';') ])},),{','.join(i['LeftStick'].split(';'))},{','.join(i['RightStick'].split(';'))})\n"
                else:
                    text = f"{text}    script.wait({i['Frame'] - lastframe})\n"
                lastframe = i['Frame']
        except:
            raise Exception('Invalid PyTAS file!')
        return text

    def convertFromFile(self,FILENAME:str):
        if not os.path.isfile(FILENAME):
            raise Exception('Invalid file passed')
        with open(FILENAME,'r') as file:
            return self.justify(file.read().split('\n'))
