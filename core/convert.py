import os, math

keys = (
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

class nxTAS():
    def __init__(self,inputs:list=[]):
        self.input_arr = inputs

    def convert(self,inputs:list=[]):
        if not inputs:
            inputs = self.input_arr
        text = '# This is an auto-generated PyTAS file\ndef main():\n'
        char = '\''
        lastframe = 0
        try:
            if not inputs:
                raise Exception()
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
            raise Exception('Invalid nxTAS file!')
        return text

    def justify(self,inputs:list):
        if not inputs:
            inputs = self.input_arr
        text = ''
        for i in inputs:
            text = f"{text}{i['Frame']} {i['Key']} {i['LeftStick']} {i['RightStick']}\n"
        return text

class tigerlua():
    def __init__(self,inputs:list=[]):
        self.input_arr = inputs

    def convert(self,inputs:list=[]):
        if not inputs:
            inputs = self.input_arr
        text = '# This is an auto-generated PyTAS file\ndef main():\n'
        char = '\''
        try:
            if not inputs:
                raise Exception()
            inputs.remove('')
            pressedIndex = []
            frames = []
            inputs[0] = inputs[0].replace('+','1')
            lstick = [0,0]
            rstick = [0,0]
            endframe = sum([ int(x.split(' ')[0]) for x in inputs ])
            lastframe = 0
            for frame in range(endframe+1):
                i = None
                s = 0
                for x in inputs:
                    s += int(x.split(' ')[0])
                    if frame == s:
                        i = x
                if not i:
                    if lstick != [0,0] or rstick != [0,0] or (pressedIndex != ['NONE',] and pressedIndex):
                        text = f"{text}    script.input({frame - lastframe},({','.join([ f'{char}{h}{char}' for h in pressedIndex ])},),{','.join(str(x) for x in makeStickCartesian(*lstick))},{','.join(str(x) for x in makeStickCartesian(*rstick))})\n"
                        lastframe = frame
                    continue
                i = i.split(' ')
                for n in i[1:]:
                    cmd = n.split('{')[0]
                    n = n[n.find('{')+1:n.find('}')]
                    if n == 'ALL':
                        n = ','.join(keys[1:])
                    if cmd.startswith('ON'):
                        for key in n.split(','):
                            pressedIndex.append(key)
                            while pressedIndex.count(key) > 1:
                                pressedIndex.remove(key)
                    elif cmd.startswith('OFF'):
                        for key in n.split(','):
                            try:
                                pressedIndex.remove(key)
                            except:
                                pass
                    elif cmd.startswith('RAW'):
                        pressedIndex = []
                        [ pressedIndex.append(key) for key in n.split(',') ]
                    elif cmd.startswith('LSTICK'):
                        lstick = [ int(x) for x in n.split(',') ]
                        if not 359 > lstick[0] > -1 or not 32767 > lstick[1] > 0:
                            raise Exception('Invalid LSTICK input for tigerlua')
                    elif cmd.startswith('RSTICK'):
                        rstick = [ int(x) for x in n.split(',') ]
                        if not 359 > rstick[0] > -1 or not 32767 > rstick[1] > 0:
                            raise Exception('Invalid RSTICK input for tigerlua')
                    else:
                        raise Exception('Unexpected input for tigerlua')
                try:pressedIndex.remove('NONE')
                except:pass
                if not pressedIndex:
                    pressedIndex.append('NONE')
                i = {
                'Frame':frame - lastframe,
                'Key':';'.join(pressedIndex),
                'LeftStick':';'.join([ str(x) for x in makeStickCartesian(*lstick) ]),
                'RightStick':';'.join([ str(x) for x in makeStickCartesian(*rstick) ]),
                }
                if i['Key'] != 'NONE' or i['LeftStick'] != '0;0' or i['RightStick'] != '0;0':
                    text = f"{text}    script.input({i['Frame']},({','.join([ f'{char}{h}{char}' for h in i['Key'].split(';') ])},),{','.join(i['LeftStick'].split(';'))},{','.join(i['RightStick'].split(';'))})\n"
                else:
                    text = f"{text}    script.wait({i['Frame']})\n"
                lastframe = frame
        except:
            raise Exception('Invalid tigerlua file!')
        return text

    def justify(self,inputs:list=[]):
        if not inputs:
            inputs = self.input_arr
        text = ''
        pressedIndex = []
        lstick = [0,0]
        rstick = [0,0]
        lastframe = 0
        for i in inputs:
            text = text + str(i['Frame'] - lastframe)
            lastframe = i['Frame']
            pressedIndex = i['Key'].split(';')
            if pressedIndex != ['NONE',]:
                text = text + ' RAW{' + ','.join(pressedIndex) + '}'
            else:
                text = text + ' OFF{ALL}'
            sticks = []
            for stick in (i['LeftStick'],i['RightStick']):
                stick = makeStickPolar(*[ int(x) for x in stick.split(';') ])
                sticks.append(stick)
            if lstick != sticks[0]:
                lstick = sticks[0]
                text = text + ' LSTICK{' + ','.join(str(x) for x in lstick) + '}'
            elif rstick != sticks[1]:
                rstick = sticks[1]
                text = text + ' RSTICK{' + ','.join(str(x) for x in rstick) + '}'
            text = text + '\n'
        text = '+' + text[1:]
        return text

def makeStickCartesian(ang,mag):
    ang = ang * math.pi / 180
    return math.floor(math.sin(ang) * mag), math.floor(math.cos(ang) * mag)

def makeStickPolar(x,y):
    if 0 in (x,y) and x != y:
        if x == 0:
            if y > 0:
                mag = abs(y)
                ang = 0
            elif y < 0:
                mag = abs(y)
                ang = 180
        elif y == 0:
            if x > 0:
                mag = abs(x)
                ang = 90
            elif x < 0:
                mag = abs(x)
                ang = 270
    elif x != 0 and y != 0:
        ang = math.degrees(math.atan(y/x))
        mag = math.floor(math.sqrt(x**2+y**2))
        if x > 0 and y > 0: # positive-positive quadrant
            ang = 90 - ang
        elif x > 0 and y < 0: # positive-negative quadrant
            ang = 90 - ang
        elif x < 0 and y < 0: # negative-positive quadrant
            ang = 90 - ang + 180
        elif x < 0 and y > 0: # negative-negative quadrant
            ang = 270 - ang
    else:
        ang, mag = 0,0
    return [round(ang),mag]

def convertFromInput(inputs:list,type):
    return type(inputs).convert()

def convertFromFile(FILENAME:str):
    if not os.path.isfile(FILENAME):
        raise Exception('Invalid file passed')
    if FILENAME.endswith('.txt'):
        type = nxTAS
    elif FILENAME.endswith('.lua'):
        type = tigerlua
    else:
        raise Exception('Unknown file type')
    with open(FILENAME,'r') as file:
        return convertFromInput(file.read().split('\n'),type)
