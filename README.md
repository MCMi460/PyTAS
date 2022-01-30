# PyTAS Documentation
## Features
PyTAS is a Python implementation of [nx-TAS](https://github.com/hamhub7/tas-script/blob/master/lua/lib/nxtas.md) by [hamhub7](https://github.com/hamhub7) intended to make shortcuts easier than before.

To use it, simply type your code in the `main()` function and run [script.py](/script.py).  
Any extra functions you create in [script.py](/script.py) may not work with the GUI extension if they have arguments required.

## Syntax
There are two native functions for inputs: `input()` and `wait()`. All inputs performed in `main()` will be used, so it's best to write your scripts in the `main()` function. Import the `script()` class to call these functions.  
`input()` requires 6 positional arguments, FRAME, KEYS, STICK1_X, STICK1_Y, STICK2_X, and STICK2_Y.  
FRAME is the number of frames since ***the previous frame\****. This value cannot be a negative integer, zero, or a decimal.  
KEYS is a list variable that contains a list of strings each of the [available buttons](#buttons).  
STICK1_X is an integer variable for the horizontal left stick usage. It must be an integer between -32767 and 32767. It cannot be a decimal.  
STICK1_Y is the same as the above, but for vertical left stick usage.  
STICK2_X is the same as the above, but for horizontal right stick usage.  
STICK2_Y is the same as the above, but for vertical right stick usage.

`wait()` is a function that adds a no input frame. It requires one positional argument: FRAME.  
FRAME is an integer and cannot be negative or a decimal point.

There is a third function, `run()`.  
`run()` takes 1 positional argument, MAIN.  
MAIN is your function that contains the inputs to run.

*\*It's important to note that FRAME is the number of frames since the previous frame as it is how functions work properly.*

<h3 id="buttons">Available buttons</h3>
KEY_A, KEY_B, KEY_X, KEY_Y, KEY_LSTICK, KEY_RSTICK, KEY_L, KEY_R, KEY_ZL, KEY_ZR, KEY_PLUS, KEY_MINUS, KEY_DLEFT, KEY_DUP, KEY_DRIGHT, KEY_DDOWN

## Example script
The following script, when run in Super Mario Odyssey, will do a roll cancel directed to the left once every second five times.
```py
def roll_cancel():
    script.input(1,('KEY_B',),0,0,0,0)
    script.input(5,('KEY_ZL',),0,0,0,0)
    script.input(35,('KEY_ZL','KEY_Y',),0,0,0,0)
    script.input(2,('KEY_X','KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)
    script.input(1,('KEY_A',),30000,0,0,0)

# Put your inputs here!
def main():
    for i in range(5):
        roll_cancel()
        script.wait(60)
    # All Python syntax should work!

from core.main import script
script = script()
script.run(main)
```

## Suggestions
Any features I missed or something you'd like to see in the future? Ping me on the [Super Mario Odyssey TAS](https://discord.gg/atKSg9fygq) Discord server. I'm Delta#4444.
