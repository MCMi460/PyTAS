def roll_cancel():
    script.input(0,('KEY_B',),0,0,0,0)
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

from main import script
script = script()
script.run(main)
