import time

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
