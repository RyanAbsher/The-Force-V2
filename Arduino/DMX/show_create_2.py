# This program reads in show definitions from def.txt and outputs def.h to  be used by the Arduino program

# startTime set channel value
# startTime fade channel startValue endValue
# startTime blink channel blinkNumber blinkDuration gapDuration
import operator
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
    elif tokens[0] == "fade":
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

#Sort Everything
commands = sorted(commands, key=operator.itemgetter(2))


outFile = open("showDef.h", "w")
outFile.write("#define NUM_DEF ")
outFile.write(str(len(commands)-1))
outFile.write("\n")

line1 = "const byte fixtureNumber[" + str(len(commands)) + "]= {"
line2 = "const byte sendValue[" + str(len(commands)) + "]= {"
line3 = "const int startTime[" + str(len(commands)) + "]= {"

for item in commands:
    if not item == commands[len(commands)-1]:
       line1 = line1 + item[0] + ", "
       line2 = line2 + str(item[1]) + ", "
       line3 = line3 + str(item[2]) + ", "
    else:
        line1 = line1 + item[0] + "};\n"
        line2 = line2 + str(item[1]) + "};\n"
        line3 = line3 + str(item[2]) + "};\n"
outFile.write(line1)
outFile.write(line2)
outFile.write(line3)

outFile.close()
              
    

