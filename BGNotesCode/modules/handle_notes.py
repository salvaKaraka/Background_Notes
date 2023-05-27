from tkinter import *


def saveNote(textspace, path):

    contents = textspace.get(0.0, END)
    with open(path, 'w+') as file:
        file.write(contents)
        file.close()
