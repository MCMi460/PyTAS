import os

class script():
    def __init__(self):
        self.keys = (
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
        self.input_arr = []
        self.curr_frame = 0
        self.path = './output'

    def input(self,FRAME:int,KEYS:list,STICK1_X:int,STICK1_Y:int,STICK2_X:int,STICK2_Y:int):
        if FRAME < 0:
            raise Exception(f'You can\'t have a negative frame! (frame {self.curr_frame} (Input #{len(self.input_arr) + 1}))')
        self.curr_frame += FRAME
        key = ''
        for i in range(len(KEYS)):
            if KEYS[i] not in self.keys:
                raise Exception(f'Key at frame {self.curr_frame} (Input #{len(self.input_arr) + 1}) does not exist.')
            if i > 0:
                key = f'{key};'
            key = f'{key}{KEYS[i]}'
        joystick_err = f'Joystick value at frame {self.curr_frame} (Input #{len(self.input_arr) + 1}) must be between the values -32767 and 32767 and cannot be a decimal.'
        if STICK1_X > 32767 or STICK1_X < -32767 or not isinstance(STICK1_X, int):
            raise Exception(joystick_err)
        if STICK1_Y > 32767 or STICK1_Y < -32767 or not isinstance(STICK1_Y, int):
            raise Exception(joystick_err)
        if STICK2_X > 32767 or STICK2_X < -32767 or not isinstance(STICK2_X, int):
            raise Exception(joystick_err)
        if STICK2_Y > 32767 or STICK2_Y < -32767 or not isinstance(STICK2_Y, int):
            raise Exception(joystick_err)
        self.input_arr.append({
        'Frame':self.curr_frame,
        'Key':key,
        'LeftStick':f'{STICK1_X};{STICK1_Y}',
        'RightStick':f'{STICK2_X};{STICK2_Y}',
        })

    def wait(self,FRAME:int):
        if FRAME < 0:
            raise Exception(f'You can\'t have a negative frame! (frame {self.curr_frame} (Input #{len(self.input_arr) + 1}))')
        self.curr_frame += FRAME

    def justify(self,inputs:list):
        text = ''
        for i in inputs:
            text = f"{text}{i['Frame']} {i['Key']} {i['LeftStick']} {i['RightStick']}\n"
        return text

    def run(self,MAIN):
        try:
            MAIN()
            if not os.path.isdir(self.path):
                os.mkdir(self.path)
            with open(f'{self.path}/script1.txt','w') as file:
                file.write(self.justify(self.input_arr))
        except Exception as e:
            print('A fatal error occurred. Please review the error message.')
            print(e)
