import threading
from time import sleep
from random import randint

def som(x,y):
    i=0
    while i in range(10):
        wow = str(int(x)*int(y))
        i += 1
        print(wow)

for _ in range(1000000):
    t = threading.Thread(target=som, args=(randint(0, 9), randint(0, 9)))
    t.start()

