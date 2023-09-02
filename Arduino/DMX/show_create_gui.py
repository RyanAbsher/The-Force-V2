from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import operator
from functools import partial

currentAction = 'FADE'
currentLine = 0

def setSet():
    param1Label.configure(text = 'Value (0-255)')
    param1Entry.configure(state='enabled')
    param2Label.configure(text = '             ')
    param2Entry.configure(state='disabled')
    param3Label.configure(text = '             ')
    param3Entry.configure(state='disabled')

def setFade():
    param1Label.configure(text = 'Duration (mS)')
    param1Entry.configure(state='enabled')
    param2Label.configure(text = 'Start Value (0-255)')
    param2Entry.configure(state='enabled')
    param3Label.configure(text = 'End Value (0-255)')
    param3Entry.configure(state='enabled')

def setBlink():
    param1Label.configure(text = 'Duration (mS)')
    param1Entry.configure(state='enabled')
    param2Label.configure(text = 'Blink Count')
    param2Entry.configure(state='enabled')
    param3Label.configure(text = '             ')
    param3Entry.configure(state='disabled')

def mainListClick(event):
    global currentLine
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        currentLine = index
    editLine()

def actionClick(event):
    global currentAction
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        action = event.widget.get(index)
        if action == 'Set':
            currentAction = 'SET'
            setSet()
        if action == 'Fade':
            currentAction = 'FADE'
            setFade()
        if action == 'Blink':
            currentAction = 'BLINK'
            setBlink()

def validated(com):
    error = 0
    if com == 'SET':
        if channelEntry.get() == '':
            messagebox.showerror('Error', 'Channel Empty')
            error = 1
        if timeEntry.get() == '':
            messagebox.showerror('Error', 'Time Empty')
            error = 1
        if param1Entry.get() == '':
            messagebox.showerror('Error', 'Value Empty')
            error = 1

        if error:
            return 0
        else:
            return 1

    elif com == 'FADE':
        if channelEntry.get() == '':
            messagebox.showerror('Error', 'Channel Empty')
            error = 1
        if timeEntry.get() == '':
            messagebox.showerror('Error', 'Start Time Empty')
            error = 1
        if param1Entry.get() == '':
            messagebox.showerror('Error', 'End Time Empty')
            error = 1
        if param2Entry.get() == '':
            messagebox.showerror('Error', 'Start Value Empty')
            error = 1
        if param2Entry.get() == '':
            messagebox.showerror('Error', 'End Value Empty')
            error = 1

        if error:
            return 0
        else:
            return 1

    elif com == 'BLINK':
        if channelEntry.get() == '':
            messagebox.showerror('Error', 'Channel Empty')
            error = 1
        if timeEntry.get() == '':
            messagebox.showerror('Error', 'Start Time Empty')
            error = 1
        if param1Entry.get() == '':
            messagebox.showerror('Error', 'Blink Duration Empty')
            error = 1
        if param2Entry.get() == '':
            messagebox.showerror('Error', 'Blink Count Empty')
            error = 1

        if error:
            return 0
        else:
            return 1


def addLine(param):
    global currentAction, currentLine
    if currentAction == 'SET':
        actionList.select_set(0)
    elif currentAction == 'FADE':
        actionList.select_set(1)
    elif currentAction == 'BLINK':
        actionList.select_set(2)

    if param == 1:
        selectedAction = actionList.curselection()
        curAction = (actionList.get(selectedAction[0])).upper()
        currentAction = curAction

        if curAction == 'SET':
            if validated('SET'):
                command = "SET " + channelEntry.get() + " " + timeEntry.get() + " " + param1Entry.get()
                listMain.insert(END, command)
        elif curAction == 'FADE':
            if validated('FADE'):
                command = "FADE " + channelEntry.get() + " " + timeEntry.get() + " " + param1Entry.get() + " " + param2Entry.get() + " " + param3Entry.get()
                listMain.insert(END, command)
        elif curAction == 'BLINK':
            if validated('BLINK'):
                command = "BLINK " + channelEntry.get() + " " + timeEntry.get() + " " + param1Entry.get() + " " + param2Entry.get()
                listMain.insert(END, command)
    elif param == 2:

        if currentAction == 'SET':
            if validated('SET'):
                command = "SET " + channelEntry.get() + " " + timeEntry.get() + " " + param1Entry.get()
                listMain.insert(currentLine, command)
        elif currentAction == 'FADE':
            if validated('FADE'):
                command = "FADE " + channelEntry.get() + " " + timeEntry.get() + " " + param1Entry.get() + " " + param2Entry.get() + " " + param3Entry.get()
                listMain.insert(currentLine, command)
        elif currentAction == 'BLINK':
            if validated('BLINK'):
                command = "BLINK " + channelEntry.get() + " " + timeEntry.get() + " " + param1Entry.get() + " " + param2Entry.get()
                listMain.insert(currentLine, command)

def editLine():
    selectedLine = listMain.curselection()
    if selectedLine:
        command = listMain.get(selectedLine[0])
        tokens = command.split()
        if len(tokens) == 0:
            pass
        elif tokens[0] == 'SET':
            setSet()
            actionList.select_set(0)
            channelEntry.delete(0, END)
            channelEntry.insert(0, tokens[1])
            timeEntry.delete(0, END)
            timeEntry.insert(0, tokens[2])
            param1Entry.delete(0, END)
            param1Entry.insert(0, tokens[3])
        elif tokens[0] == 'FADE':
            setFade()
            actionList.select_set(1)
            channelEntry.delete(0, END)
            channelEntry.insert(0, tokens[1])
            timeEntry.delete(0, END)
            timeEntry.insert(0, tokens[2])
            param1Entry.delete(0, END)
            param1Entry.insert(0, tokens[3])
            param2Entry.delete(0, END)
            param2Entry.insert(0, tokens[4])
            param3Entry.delete(0, END)
            param3Entry.insert(0, tokens[5])
        elif tokens[0] == 'BLINK':
            setBlink()
            actionList.select_set(2)
            channelEntry.delete(0, END)
            channelEntry.insert(0, tokens[1])
            timeEntry.delete(0, END)
            timeEntry.insert(0, tokens[2])
            param1Entry.delete(0, END)
            param1Entry.insert(0, tokens[3])
            param2Entry.delete(0, END)
            param2Entry.insert(0, tokens[4])

def generate():
    outfile = open('def.txt', 'w')
    for entry in enumerate(listMain.get(0, END)):
        outfile.write(entry[1])
        outfile.write('\n')

    outfile.close()

    commands = []
    definitions = open("def.txt", "r")
    data = definitions.readlines()
    definitions.close()
    for line in data:
        tokens = line.split()
        if len(tokens) == 0: # Blank Line
            continue
        elif tokens[0] == "#": # Comment
            continue
        elif tokens[0] == "FADE":
            if(int(tokens[5]) > int(tokens[4])): # If we are fading up
                numSteps = (int((int(tokens[3]) / 1000) * 40)) + 1 # Add one just to make sure it gets there, accounted for later
                stepSize = int((int(tokens[5]) - int(tokens[4])) / numSteps)
                value = int(tokens[4])
                step = 0
                while value < int(tokens[5]):
                    value = value + stepSize
                    if value > int(tokens[5]):
                        value = int(tokens[5])
                    command = [tokens[1], value, int(tokens[2]) + (step * stepSize)]
                    commands.append(command)
                    step = step + 1

            if(int(tokens[4]) > int(tokens[5])): # If we are fading down
                numSteps = (int((int(tokens[3]) / 1000) * 40)) + 1 # Add one just to make sure it gets there, accounted for later
                stepSize = int((int(tokens[4]) - int(tokens[5])) / numSteps)
                value = int(tokens[4])
                step = 0
                while value > int(tokens[5]):
                    value = value - stepSize
                    if value < int(tokens[5]):
                        value = int(tokens[5])
                    command = [tokens[1], value, int(tokens[2]) + (step * stepSize)]
                    commands.append(command)
                    step = step + 1
        elif tokens[0] == "SET":
            command = [int(tokens[1]), int(tokens[3]), int(tokens[2])]
            commands.append(command)
        elif tokens[0] == "BLINK":
            numBlinks = int(tokens[4])
            blinkDuration = int(tokens[3])
            onOff = 1 # toggling variable for the next loop, 1 = on, 0 = off, go figure
            for i in range(0, numBlinks*2):
                if onOff == 1:
                    command = [int(tokens[1]), 255, int(tokens[2]) + (blinkDuration * i)]
                    commands.append(command)
                    onOff = not onOff
                elif onOff == 0:
                    command = [int(tokens[1]), 0, int(tokens[2]) + (blinkDuration * i)]
                    commands.append(command)
                    onOff = not onOff


    #Sort Everything
    commands = sorted(commands, key=operator.itemgetter(2))
    outFile = open("showDef.h", "w")
    outFile.write("#define NUM_DEF ")
    outFile.write(str(len(commands)-1))
    outFile.write("\n\n")

    line1 = "const int fixtureNumber" + "[" + str(len(commands)) + "] PROGMEM = {"
    line2 = "const int sendValue" + "[" + str(len(commands)) + "] PROGMEM = {"
    line3 = "const int startTime" + "[" + str(len(commands)) + "] PROGMEM = {"

    for i, item in enumerate(commands):
        if not item == commands[len(commands)-1]:
            line1 = line1 + str(item[0]) + ", "
            line2 = line2 + str(item[1]) + ", "
            line3 = line3 + str(item[2])[:-1] + ", "
        else:
            line1 = line1 + str(item[0]) + "};\n"
            line2 = line2 + str(item[1]) + "};\n"
            line3 = line3 + str(item[2])[:-1] + "};\n"
    outFile.write(line1)
    outFile.write(line2)
    outFile.write(line3)
    outFile.write('\n\n')

    outFile.close()

    messagebox.showinfo("Success", "File Generated Successfully")

def loadFile():
    global currentLine
    listMain.delete(0, END)
    infile = open('def.txt', 'r')
    lines = infile.readlines()
    for line in lines:
        templine = line.strip('\n')
        listMain.insert(END, templine)
    infile.close()

def deleteLine():
    global currentLine
    listMain.delete(currentLine)

def saveLine():
    global currentLine
    listMain.delete(currentLine)
    addLine(2)

def insertLine():
    global currentLine
    afterList = []

    for item in range(currentLine, listMain.size()):
        afterList.append(listMain.get(item))

    listMain.delete(currentLine, END)

    listMain.insert(currentLine + 1, "")

    for i, item in enumerate(afterList, start = currentLine + 1):
        listMain.insert(i, item)



root = Tk()
root.geometry('630x580')
actionLabel = Label(root, text = 'Action')
actionList = Listbox(root, height = 3, width = 5)

channelLabel = Label(root, text = 'Channel')
channelEntry = Entry(root, width = 5)

timeLabel = Label(root, text = 'Start Time (mS)')
timeEntry = Entry(root, width = 10)

param1Label = Label(root, text = 'Duration (mS)')
param1Entry = Entry(root, width = 10)

param2Label = Label(root, text = 'Start Value (0-255)')
param2Entry = Entry(root, width = 10)

param3Label = Label(root, text = 'End Value (0-255)')
param3Entry = Entry(root, width = 10)

actionLabel.grid(row = 0, column = 0, sticky = N, padx = 10, pady = 5)
actionList.grid(row = 1, column = 0, sticky = N, padx = 10, pady = 5)

channelLabel.grid(row = 0, column = 1, sticky = N, padx = 10, pady = 5)
channelEntry.grid(row = 1, column = 1, sticky = N, padx = 10, pady = 5)

timeLabel.grid(row = 0, column = 2, sticky = N, padx = 10, pady = 5)
timeEntry.grid(row = 1, column = 2, sticky = N, padx = 10, pady = 5)

param1Label.grid(row = 0, column = 3, sticky = N, padx = 10, pady = 5)
param1Entry.grid(row = 1, column = 3, sticky = N, padx = 10, pady = 5)

param2Label.grid(row = 0, column = 4, sticky = N, padx = 10, pady = 5)
param2Entry.grid(row = 1, column = 4, sticky = N, padx = 10, pady = 5)

param3Label.grid(row = 0, column = 5, sticky = N, padx = 10, pady = 5)
param3Entry.grid(row = 1, column = 5, sticky = N, padx = 10, pady = 5)

btnAdd = Button(root, text = 'Add Line', command = partial(addLine, 1))
btnAdd.grid(row = 3, column = 0, columnspan = 1, padx = 10, pady = 5)

btnSave = Button(root, text = 'Save Line', command = saveLine)
btnSave.grid(row = 3, column = 1, columnspan = 1, padx = 10, pady = 5)

btnDelete = Button(root, text = 'Delete Line', command = deleteLine)
btnDelete.grid(row = 3, column = 2, columnspan = 1, padx = 10, pady = 5)

btnInsert = Button(root, text = 'Insert Line', command = insertLine)
btnInsert.grid(row = 3, column = 3, columnspan = 1, padx = 10, pady = 5)

btnGen = Button(root, text = 'Generate', command = generate)
btnGen.grid(row = 3, column = 5, columnspan = 1, padx = 10, pady = 5)

btnLoad = Button(root, text = 'Load File', command = loadFile)
btnLoad.grid(row = 3, column = 4, columnspan = 1, padx = 10, pady = 5)

listMain = Listbox(root, height = 25, width = 100)
listMain.grid(row = 4, column = 0, columnspan = 6, padx = 10, pady = 5)

commentLabel = Label(root, text = 'Comment')
commentLabel.grid(row = 2, column = 0, columnspan = 1, padx = 10, pady = 5)

commentEntry = Entry(root, width = 83)
commentEntry.grid(row = 2, column = 1, columnspan = 5, padx = 10, pady = 5)

actionList.insert("end", "Set", "Fade", "Blink")


actionList.select_set(1)

actionList.bind("<<ListboxSelect>>", actionClick)
listMain.bind("<<ListboxSelect>>", mainListClick)

root.mainloop()