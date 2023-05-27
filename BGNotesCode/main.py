import tkinter as tk
from tkinter import *
from tkinter import filedialog, colorchooser
from modules.handle_notes import *

#from title_bar import *

from PIL import (ImageTk, Image, ImageDraw, ImageFont)
import shutil
import ctypes
import win32con

from modules.classes import (CustomText)


'''
last_note_path = 'notes/last_note.txt'
'''


root = Tk()

# -------------- Global vars -------------

global previewPath
global wallpaperPath
global saved_wallpaper_path
saved_wallpaper_path = ''
wallpaperPath = ''

global issaved
issaved = False

# -------needed to preview------
global isselected, isBgChecked
isselected = False
isBgChecked = False

global text_x
global text_y
global font_size
global text_color
global text_bg_color
text_x = 20
text_y = 20
font_size = 35
text_color = 'WHITE'
text_bg_color = 'BLACK'

# ------note file opened?------
global isopened
isopened = False

# ------- note path ------------
global filepath
filepath = ''

# default path
previewPath = 'wallpaper/default_preview.jpg'

# -------------- FUNCTIONS --------------


def openNote():

    global issaved
    global isopened
    isopened = False

    global filepath
    filepath = filedialog.askopenfilename(title='open note', filetypes=(('Text files', '*.txt'),
                                                                        ('All files', '*.*')))
    print(filepath)

    try:
        with open(filepath, "r", encoding='utf-8') as file:
            textspace.delete(0.0, END)
            textspace.insert(0.0, file.read())
            file.close()
            isopened = True
            leftframe.config(text='note path: '+filepath)
            issaved = False
    except:
        try:
            with open(filepath, "r", encoding='utf-16') as file:
                textspace.delete(0.0, END)
                textspace.insert(0.0, file.read())
                file.close()
                isopened = True
                leftframe.config(text='note path: '+filepath)
                issaved = False
        except:
            textspace.delete(0.0, END)
            textspace.insert(0.0, 'THE SPECIFIED FILE COULD NOT BE OPENED')

    return None


def saveNote():
    global filepath
    global isopened

    if (isopened == True):

        filecontents = textspace.get(0.0, END)

        with open(filepath, 'w+') as file:
            file.write(filecontents)
            file.close()
    else:
        saveNoteAs()


def saveNoteAs():
    global filepath
    global isopened

    filecontents = textspace.get(0.0, END)

    filepath = filedialog.asksaveasfilename(initialdir='This PC', title='save note',
                                            filetypes=(('Text files', '*.txt'),
                                                       ('All files', '*.*')))
    try:
        with open(filepath, 'w+') as file:

            file.write(filecontents)
            file.close()
            isopened = True
    except:
        print('ha ocurrido un error al intentar guardar la nota')

    return None


def selectWallpaper():
    global issaved
    global isselected
    global previewPath
    global wallpaperPath

    wallpaperPath = filedialog.askopenfilename(title='select wallpaper', filetypes=(('jpg image', '*.jpg'),
                                                                                    ('png image',
                                                                                     '*.png'),
                                                                                    ('All files', '*.*')))
    print(wallpaperPath)

    if (wallpaperPath != ''):

        previewPath = wallpaperPath
        isselected = True
        issaved = False

        toprightframe.config(text='wallpaper path: '+wallpaperPath)

        changeGUI()
        pvWallpaper()

    else:
        return None

    return None


def changeGUI():
    select_button.config(text='Select another image')
    save_button.config(state=NORMAL)
    setBg_button.config(state=NORMAL)


def pvWallpaper():

    global issaved, previewPath, wallpaperPath
    global text_x, text_y, font_size, text_color, text_bg_color

    preview_image = Image.open(wallpaperPath)
    draw = ImageDraw.Draw(preview_image)

    font = ImageFont.truetype("fonts/Poppins-Medium.ttf", font_size)

    filecontents = textspace.get(0.0, END)

    if(isBgChecked == True):

        lines = filecontents.splitlines()
        longline = max(lines, key=len)
        w, h = font.getsize(longline)

        linesNumber = len(lines)
        draw.rectangle((text_x-(h/3), text_y, text_x+w+(h/3), (h/3)+text_y+h*linesNumber),
                       fill=text_bg_color)

    draw.text((text_x, text_y), filecontents, font=font, fill=text_color)

    previewPath = 'wallpaper/wallpaper_preview.jpg'

    preview_image.save(previewPath)

    pvResize()

    issaved = False

    return None


def saveWallpaper():
    global isselected
    global issaved
    global previewPath
    global saved_wallpaper_path

    if (isselected == True):
        saved_wallpaper_path = filedialog.asksaveasfilename(initialdir='This PC', title='save note',
                                                            filetypes=(('image', '*.jpg'), ('All files', '*.*')))
        shutil.copy(previewPath, saved_wallpaper_path)
        issaved = True
    else:
        print('you must select a wallpaper first')
    return None


def setBackground():
    global issaved

    if (issaved != True):
        saveWallpaper()
    if(issaved == True):
        changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        ctypes.windll.user32.SystemParametersInfoW(
            win32con.SPI_SETDESKWALLPAPER, 0, saved_wallpaper_path, changed)


# ------------event trackers--------

# -----main text--------


def detectTextChange(e):
    global isselected
    if(isselected == True):
        pvWallpaper()

# -----text entrys--------


def text_xposChange(text_x_var):
    global text_x, isselected

    try:
        if(int(text_x_var.get()) != 0):
            text_x = int(text_x_var.get())
        else:
            text_xpos.delete(0, END)
            text_xpos.insert(END, '')
    except ValueError:
        if(text_x_var.get() == ''):
            text_x = 0
            text_xpos.delete(0, END)
            text_xpos.insert(END, '')
        else:
            text_xpos.delete(0, END)
            text_xpos.insert(END, str(text_x))

    if(isselected == True):
        pvWallpaper()


def text_yposChange(text_y_var):
    global text_y, isselected

    try:
        if(int(text_y_var.get()) != 0):
            text_y = int(text_y_var.get())
        else:
            text_ypos.delete(0, END)
            text_ypos.insert(END, '')
    except ValueError:
        if(text_y_var.get() == ''):
            text_y = 0
            text_ypos.delete(0, END)
            text_ypos.insert(END, '')
        else:
            text_ypos.delete(0, END)
            text_ypos.insert(END, str(text_y))

    if(isselected == True):
        pvWallpaper()


def fontSizeChange(fontSize_var):
    global font_size, isselected

    try:
        if(int(fontSize_var.get()) != 0):
            font_size = int(fontSize_var.get())
        else:
            fontSize.delete(0, END)
            fontSize.insert(END, '')
    except ValueError:
        if(fontSize_var.get() == ''):
            font_size = 0
            fontSize.delete(0, END)
            fontSize.insert(END, '')
        else:
            fontSize.delete(0, END)
            fontSize.insert(END, str(font_size))

    if(isselected == True):
        pvWallpaper()


def checkButton():
    global isBgChecked
    if(isBgChecked == False):
        isBgChecked = True
        text_bg_check_button.config(text='Yes')
        pvWallpaper()
    else:
        isBgChecked = False
        text_bg_check_button.config(text='No')
        pvWallpaper()


def colorPicker(i):
    global text_color, text_bg_color, isselected

    if(i == 0):
        text_color = colorchooser.askcolor()[1]
        text_color_button.config(bg=text_color)

    elif(i == 1):
        text_bg_color = colorchooser.askcolor()[1]
        text_bg_color_button.config(bg=text_bg_color)

    if(isselected == True):
        pvWallpaper()


# -------------- GUI --------------

tk_title = "Background Notes"

# create two frames
leftframe = LabelFrame(root, text='Take a note...')

rightframe = Frame(root)
toprightframe = LabelFrame(rightframe, text='Preview your wallpaper:')
bottomrightframe = LabelFrame(rightframe, text='options:')


leftframe.grid(column=0, row=0, sticky='nsew')

rightframe.grid(column=1, row=0, sticky='nsew')
toprightframe.grid(column=0, row=0, sticky='nsew')
bottomrightframe.grid(column=0, row=1, sticky='nsew')


# configure grid to be responsive
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)

Grid.rowconfigure(leftframe, 0, weight=1)
Grid.columnconfigure(leftframe, 0, weight=1)

Grid.rowconfigure(rightframe, 0, weight=1)
Grid.rowconfigure(rightframe, 1, weight=1)
Grid.columnconfigure(rightframe, 0, weight=1)

Grid.rowconfigure(toprightframe, 0, weight=1)
Grid.columnconfigure(toprightframe, 0, weight=1)


# create txt space
textspace = CustomText(leftframe)
textspace.grid(column=0, row=0, sticky='nsew')
textspace.bind("<<TextModified>>", detectTextChange)

# scrollbar for text space
yscroll = Scrollbar(leftframe, orient="vertical", command=textspace.yview)
textspace.configure(yscrollcommand=yscroll.set)
yscroll.grid(column=1, row=0, sticky='ns')

# Create a menu bar python
menuBar = Menu(root)
root.config(menu=menuBar)

fileMenu = Menu(menuBar)
menuBar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open note", command=openNote)
fileMenu.add_command(label="Save", command=saveNote)
fileMenu.add_command(label="Save note as...", command=saveNoteAs)

# Create a preview zone
# top right
preview_display = Canvas(toprightframe, bg='#4f4f4f')
preview_display.grid(column=0, row=0, sticky='nsew')

# buttons (bottom right)
select_button = Button(bottomrightframe)
select_button.config(text='Select an image', command=selectWallpaper)
select_button.grid(column=0, row=0, sticky='nsew',
                   columnspan=2, padx=5, pady=5)

save_button = Button(bottomrightframe)
save_button.config(text='Save as...', command=saveWallpaper, state=DISABLED)
save_button.grid(column=2, row=0, sticky='nsew', columnspan=4, padx=5, pady=5)

setBg_button = Button(bottomrightframe)
setBg_button.config(text='Set as background',
                    command=setBackground, state=DISABLED)
setBg_button.grid(column=6, row=0, sticky='nsew', columnspan=2, padx=5, pady=5)

# text entrys

# stringvars

text_x_var = StringVar()
text_x_var.trace("w", lambda name, index, mode,
                 sv=text_x_var: text_xposChange(text_x_var))

text_y_var = StringVar()
text_y_var.trace("w", lambda name, index, mode,
                 sv=text_y_var: text_yposChange(text_y_var))

fontSize_var = StringVar()
fontSize_var.trace("w", lambda name, index, mode,
                   sv=fontSize_var: fontSizeChange(fontSize_var))

# labels
text_xpos_label = Label(bottomrightframe, text="text x:",)
text_ypos_label = Label(bottomrightframe, text="text y:")
fontSize_label = Label(bottomrightframe, text="font size:")
textColor_label = Label(bottomrightframe, text="text color:")
textBgColor_label = Label(bottomrightframe, text="text background:")

text_xpos_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
text_ypos_label.grid(row=1, column=2, sticky='w', padx=5, pady=5)
fontSize_label.grid(row=1, column=6, sticky='w', padx=5, pady=5)
textColor_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
textBgColor_label.grid(row=2, column=2, sticky='w', padx=5, pady=5)

# entrys
text_xpos = Entry(bottomrightframe, textvariable=text_x_var)
text_ypos = Entry(bottomrightframe, textvariable=text_y_var)
fontSize = Entry(bottomrightframe, textvariable=fontSize_var)

text_xpos.grid(row=1, column=1, sticky='w', padx=5, pady=5)
text_ypos.grid(row=1, column=3, sticky='e', columnspan=3, padx=5, pady=5)
fontSize.grid(row=1, column=7, sticky='w', padx=5, pady=5)

text_xpos.insert(END, str(text_x))
text_ypos.insert(END, str(text_y))
fontSize.insert(END, str(font_size))

# color choosers

text_color_button = Button(bottomrightframe)
text_color_button.config(text='     ', bg=text_color,
                         command=lambda: colorPicker(0))
text_color_button.grid(row=2, column=1, sticky='w', padx=5, pady=5)

text_bg_color_button = Button(bottomrightframe)
text_bg_color_button.config(
    text='     ', bg=text_bg_color, command=lambda: colorPicker(1))
text_bg_color_button.grid(row=2, column=4, sticky='w', padx=5, pady=5)

# want bg?
text_bg_check_button = Button(bottomrightframe)
text_bg_check_button.config(
    text='NO', command=checkButton)
text_bg_check_button.grid(row=2, column=3, sticky='w', padx=5, pady=5)


# ---------------- resizers ----------------


def topRightResizer(e):

    global height
    global width

    width = e.width
    height = e.height

    pvResize()


def pvResize():

    global source_image
    global preview
    global resized_preview

    source_image = Image.open(previewPath)

    pvheight = int((width/16)*9)
    pvwidth = width

    if (pvheight > height-30):
        pvheight = height-30
        pvwidth = int(16*((height-30)/9))

    resized_preview = source_image.resize(
        (pvwidth, pvheight), Image.ANTIALIAS)

    preview = ImageTk.PhotoImage(resized_preview)

    y = (height-pvheight)/5
    x = (width-pvwidth)/2

    preview_display.create_image(x, y, image=preview, anchor=NW)


toprightframe.bind('<Configure>', topRightResizer)

root.mainloop()
