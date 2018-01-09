import os

link = os.listdir("C:\\Users\\Daan Renken\\Pictures\\Images")


def picture_title():

    titles = [x[:-4] for x in link]
    lowercase_title = [x.lower() for x in titles]
    lowercase_title
    for t in lowercase_title:
        print(t)


picture_title()
