<<<<<<< HEAD
import os

link = os.listdir("C:\\Users\\Daan Renken\\Pictures\\Images")


def picture_title():

    titles = [x[:-4] for x in link]
    lowercase_title = [x.lower() for x in titles]
    lowercase_title
    for t in lowercase_title:
        print(t)


picture_title()
=======
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

>>>>>>> 4408c15f1d737e20d5d83ee48025de9269d631b6
