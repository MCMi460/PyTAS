def roll_cancel():
    input(0,('KEY_B',),0,0,0,0)
    input(5,('KEY_ZL',),0,0,0,0)
    input(35,('KEY_ZL','KEY_Y',),0,0,0,0)
    input(2,('KEY_X','KEY_A',),30000,0,0,0)
    input(1,('KEY_A',),30000,0,0,0)
    input(1,('KEY_A',),30000,0,0,0)
    input(1,('KEY_A',),30000,0,0,0)
    input(1,('KEY_A',),30000,0,0,0)

# Put your inputs here!
def main():
    roll_cancel()
    for i in range(5):
        wait(60)
        roll_cancel()
    # All Python syntax should work!





































# Technical stuff below that makes this work
import os

keys = (
'NONE',
'KEY_A',
'KEY_B',
'KEY_X',
'KEY_Y',
'KEY_LSTICK',
'KEY_RSTICK',
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
)

input_arr = []
curr_frame = 0
path = './output'

def input(FRAME:int,KEYS:list,STICK1_X:int,STICK1_Y:int,STICK2_X:int,STICK2_Y:int):
    global curr_frame
    if FRAME < 0:
        raise Exception(f'You can\'t have a negative frame! (frame {curr_frame} (Input #{len(input_arr) + 1}))')
    curr_frame += FRAME
    key = ''
    for i in range(len(KEYS)):
        if KEYS[i] not in keys:
            raise Exception(f'Key at frame {curr_frame} (Input #{len(input_arr) + 1}) does not exist.')
        if i > 0:
            key = f'{key};'
        key = f'{key}{KEYS[i]}'
    joystick_err = f'Joystick value at frame {curr_frame} (Input #{len(input_arr) + 1}) must be between the values -32767 and 32767 and cannot be a decimal.'
    if STICK1_X > 32767 or STICK1_X < -32767 or not isinstance(STICK1_X, int):
        raise Exception(joystick_err)
    if STICK1_Y > 32767 or STICK1_Y < -32767 or not isinstance(STICK1_Y, int):
        raise Exception(joystick_err)
    if STICK2_X > 32767 or STICK2_X < -32767 or not isinstance(STICK2_X, int):
        raise Exception(joystick_err)
    if STICK2_Y > 32767 or STICK2_Y < -32767 or not isinstance(STICK2_Y, int):
        raise Exception(joystick_err)
    input_arr.append({
    'Frame':curr_frame,
    'Key':key,
    'LeftStick':f'{STICK1_X};{STICK1_Y}',
    'RightStick':f'{STICK2_X};{STICK2_Y}',
    })

def wait(FRAME:int):
    global curr_frame
    if FRAME < 0:
        raise Exception(f'You can\'t have a negative frame! (frame {curr_frame} (Input #{len(input_arr) + 1}))')
    curr_frame += FRAME

def justify(inputs:list):
    text = ''
    for i in inputs:
        text = f"{text}{i['Frame']} {i['Key']} {i['LeftStick']} {i['RightStick']}\n"
    return text

try:
    main()
    if not os.path.isdir(path):
        os.mkdir(path)
    with open(f'{path}/script1.txt','w') as file:
        file.write(justify(input_arr))
except Exception as e:
    print('A fatal error occurred. Please review the error message.')
    print(e)
