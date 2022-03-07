import sys

code = open(sys.argv[1]).read().split("\n")
on = 0
expectedIndentation = 0
# the loop stack contains the conditions for every loop that is currently happening
loopStack = []
callStack = []
memory = {}
subrutines = {}
running = True

# TODO: Add comments

def sumlist(array):
    location = 0
    result = ""
    while location<len(array):
        result += array[location]+" "
        location += 1
    return result[:len(result)-1]
while on<len(code):
    line = code[on]
    if line[0] == "@":
        subrutines[line.split("@")[1]] = on
    on += 1
on = 0
while running:
    line = sumlist(code[on].split("\t")[expectedIndentation:])
    if line.split(" ")[0] == "DISPLAY":
        args = line.split(" ")[1:]
        if args[0] == "VARIABLE":
            displayvalue = memory[args[1]]
            if str(type(displayvalue)) == "<class 'str'>":
                displayvalue = displayvalue.replace("#newline","\n")
            print(displayvalue,end="")
        else:
            displayvalue = line.split("\*")[1].replace("#newline","\n")
            print(displayvalue,end="")
        on += 1
    elif line.split(" ")[0] == "ASSIGN":
        args = line.split(" ")[1:]
        if args[1] == "STRING":
            memory[args[0]] = line.split("\*")[1]
        elif args[1] == "INTEGER":
            memory[args[0]] = int(line.split("\'")[1])
        else:
            print("Error: used non existant data type'",args[1],"'on line",on)
            code[on] = "END"
        on += 1
    elif line.split(" ")[0] == "INPUT":
        args = line.split(" ")[1:]
        if args[0] == "STRING":
            userinput = input()
        elif args[0] == "INTEGER":
            userinput = int(input())
        else:
            print("Error: used non existant data type on line",on)
            code[on] = "END"
        memory[args[1]] = userinput
        on += 1
    elif line == "" and sumlist(code[on].split("\t")[expectedIndentation-1:]) == "":
        print("Error: line ",on," is either empty or indented to far")
        print(code[on])
        code[on] == "END"
    elif line.split(" ")[0] == "IF":
        expectedIndentation += 1
        args = line.split(" ")[1:]
        operator = args[1]
        left = 1
        on += 1
        conditionArgs = [args[0],args[2]]
        #converting the values into the correct types
        if (conditionArgs[0][0],conditionArgs[0][1]) == ("\\","*"):
            conditionArgs[0] = conditionArgs[0][2:]
        elif (conditionArgs[0][0],conditionArgs[0][1]) == ("\\","'"):
            conditionArgs[0] = int(conditionArgs[0][2:])
        else:
            conditionArgs[0] = memory[conditionArgs[0]]
        if (conditionArgs[1][0],conditionArgs[1][1]) == ("\\","*"):
            conditionArgs[1] = conditionArgs[1][2:]
        elif (conditionArgs[1][0],conditionArgs[1][1]) == ("\\","'"):
            conditionArgs[1] = int(conditionArgs[1][2:])
        else:
            conditionArgs[1] = memory[conditionArgs[1]]
        if operator == "=":
            condition = conditionArgs[0] == conditionArgs[1]
        elif operator == "<":
            condition = conditionArgs[0] < conditionArgs[1]
        elif operator == ">":
            condition = conditionArgs[0] > conditionArgs[1]
        if condition == False:
            while left > 0:
                line = sumlist(code[on].split("\t")[expectedIndentation:])
                if sumlist(code[on].split("\t")[expectedIndentation-1:]) == "ENDIF":
                    expectedIndentation -= 1
                    left -= 1
                if sumlist(code[on].split("\t")[expectedIndentation-1:]) == "ENDLOOP":
                    expectedIndentation -= 1
                    left -= 1
                if line.split(" ")[0] == "IF":
                    left += 1
                    expectedIndentation += 1
                if line.split(" ")[0] == "LOOP":
                    left += 1
                    expectedIndentation += 1
                on += 1
    elif sumlist(code[on].split("\t")[expectedIndentation-1:]) == "ENDIF":
        expectedIndentation -= 1
        on += 1
    elif line.split(" ")[0] == "CALCULATE":
        args = line.split(" ")[1:]
        calculationArgs = [args[0],args[2]]
        operator = args[1]
        if (calculationArgs[1][0],calculationArgs[1][1]) == ("\\","*"):
            calculationArgs[1] = calculationArgs[1][2:]
        elif (calculationArgs[1][0],calculationArgs[1][1]) == ("\\","'"):
            calculationArgs[1] = int(calculationArgs[1][2:])
        else:
            calculationArgs[1] = memory[calculationArgs[1]]
        if operator == "+":
            memory[calculationArgs[0]] += calculationArgs[1]
        elif operator == "-":
            memory[calculationArgs[0]] -= calculationArgs[1]
        else:
            print("Error: invalid operator on line",on)
        on += 1
    elif line.split(" ")[0] == "LOOP":
        args = line.split(" ")[1:]

        #pushing the conditions to the loop stack
        newStackElement = (args,on)
        loopStack.append(newStackElement)
        
        operator = args[1]
        expectedIndentation += 1
        left = 1
        on += 1
        conditionArgs = [args[0],args[2]]
        #converting the values into the correct types
        if (conditionArgs[0][0],conditionArgs[0][1]) == ("\\","*"):
            conditionArgs[0] = conditionArgs[0][2:]
        elif (conditionArgs[0][0],conditionArgs[0][1]) == ("\\","'"):
            conditionArgs[0] = int(conditionArgs[0][2:])
        else:
            conditionArgs[0] = memory[conditionArgs[0]]
        if (conditionArgs[1][0],conditionArgs[1][1]) == ("\\","*"):
            conditionArgs[1] = conditionArgs[1][2:]
        elif (conditionArgs[1][0],conditionArgs[1][1]) == ("\\","'"):
            conditionArgs[1] = int(conditionArgs[1][2:])
        else:
            conditionArgs[1] = memory[conditionArgs[1]]
        if operator == "=":
            condition = conditionArgs[0] == conditionArgs[1]
        elif operator == "<":
            condition = conditionArgs[0] < conditionArgs[1]
        elif operator == ">":
            condition = conditionArgs[0] > conditionArgs[1]
        if condition == False:
            while left > 0:
                line = sumlist(code[on].split("\t")[expectedIndentation:])
                if sumlist(code[on].split("\t")[expectedIndentation-1:]) == "ENDIF":
                    expectedIndentation -= 1
                    left -= 1
                if sumlist(code[on].split("\t")[expectedIndentation-1:]) == "ENDLOOP":
                    expectedIndentation -= 1
                    left -= 1
                if line.split(" ")[0] == "IF":
                    left += 1
                    expectedIndentation += 1
                if line.split(" ")[0] == "LOOP":
                    left += 1
                    expectedIndentation += 1
                on += 1
    elif sumlist(code[on].split("\t")[expectedIndentation-1:]) == "ENDLOOP":
        conditionArgs=[ loopStack[len(loopStack)-1][0][0], loopStack[len(loopStack)-1][0][2] ]
        operator = loopStack[len(loopStack)-1][0][1]
        #converting the values into the correct types
        if (conditionArgs[0][0],conditionArgs[0][1]) == ("\\","*"):
            conditionArgs[0] = conditionArgs[0][2:]
        elif (conditionArgs[0][0],conditionArgs[0][1]) == ("\\","'"):
            conditionArgs[0] = int(conditionArgs[0][2:])
        else:
            conditionArgs[0] = memory[conditionArgs[0]]
        if (conditionArgs[1][0],conditionArgs[1][1]) == ("\\","*"):
            conditionArgs[1] = conditionArgs[1][2:]
        elif (conditionArgs[1][0],conditionArgs[1][1]) == ("\\","'"):
            conditionArgs[1] = int(conditionArgs[1][2:])
        else:
            conditionArgs[1] = memory[conditionArgs[1]]
        if operator == "=":
            condition = conditionArgs[0] == conditionArgs[1]
        elif operator == "<":
            condition = conditionArgs[0] < conditionArgs[1]
        elif operator == ">":
            condition = conditionArgs[0] > conditionArgs[1]
        if condition:
            on = loopStack[len(loopStack)-1][1]
            on += 1
        else:
            loopStack = loopStack[:len(loopStack)-1]
            expectedIndentation -= 1
            on += 1
    elif line.split(" ")[0] == "GOSUB":
        # the reason that the expected indentation is pushed with the instruction-pointer's location is to know how mutch it will need to be indented when returning
        callStack.append((on,expectedIndentation))
        on = subrutines[line.split(" ")[1]]
        expectedIndentation = 1
        on += 1
    elif sumlist(code[on].split("\t")[expectedIndentation-1:]) == "RETURN":
        on = callStack[len(callStack)-1][0]
        expectedIndentation = callStack[len(callStack)-1][1]
        callStack = callStack[:len(callStack)-1]
        on += 1
    elif line.split(" ")[0] == "//":
        on += 1
    elif code[on] == "END":
        running = False
