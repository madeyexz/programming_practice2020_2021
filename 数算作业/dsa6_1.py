def pascalTriangle(numofrow):
    for i in range(numofrow):
        print(printPascal(i))


def printPascal(testVariable) :
    if testVariable == 0 :
        return [1]
    else :
        line = [1]
        previousLine = printPascal(testVariable - 1)
        for i in range(len(previousLine) - 1):
            line.append(previousLine[i] + previousLine[i + 1])
        line += [1]
    return line

pascalTriangle(10)