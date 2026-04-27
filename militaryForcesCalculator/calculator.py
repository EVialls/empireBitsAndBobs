import itertools
import sys
import csv
from os import system

forceBounds = {
    "Min": 0,
    "Max": 0
}
nationForces = {
    "Brass Coast": 0,
    "Dawn": 0,
    "Highguard": 0,
    "Imperial Orcs": 0,
    "League": 0,
    "Marches": 0,
    "Navarr": 0,
    "Urizen": 0,
    "Varushka": 0,
    "Wintermark": 0
}

nationNames = nationForces.keys()
nationMenuItems = dict(enumerate(nationNames, start=1))

nationsFiltered = []
nationsGrouped = []


def main():
    optionFunctions = {
        "Input Force Numbers": inputForces,
        "Input Minimum and Maximum Force": inputMinMaxForce,
        "Nations To Separate": nationsToSeparate,
        "Nations To Group": nationsToGroup,
        "Current Data": listData,
        "Calculate": calculate,
        "Quit": done}
    menuItems = dict(enumerate(optionFunctions.keys(), start=1))

    while True:
        displayMenu(menuItems)
        try:
            selection = int(
            input("Please enter your selection number: "))
            selected_value = optionFunctions[menuItems[selection]]
            selected_value()
        except ValueError:
            print("invalid entry")

def done():
    print("Goodbye")
    sys.exit()

def displayMenu(menu):
    for displayName, function in menu.items():
        print(displayName, function)

def inputForces():
    for nation in nationNames:
        forceNumber = -1
        while(True):
            try:
                nationForces[nation] = int(input("Force Number for " + nation + ": "))
                break
            except ValueError:
                print("invalid value")

    print("Force numbers are:")
    for nationName in nationForces:
        print(nationName + ": " + str(nationForces[nationName]))
    print("")

def inputMinMaxForce():
    while(True):
        try:
            forceBounds["Min"] = int(input("Input minimum force required: "))
            break
        except ValueError:
            print("invalid value")
    while(True):
        try:
            forceBounds["Max"] = int(input("Input maximum force required: "))
            if forceBounds["Max"] < forceBounds["Min"]:
                forceBounds["Max"] = 0
                print("max force must be greater than or equal to min force")
            else:
                break
        except ValueError:
            print("invalid value")
    print("Minimum Force: " + str(forceBounds["Min"]))
    print("Maximum Force: " + str(forceBounds["Max"]) + "\n")

def nationsToSeparate():
    if len(nationsFiltered) == 0:
        print("no current filters")
    else:
        print("current nations to be separated:")
        for nationPair in nationsFiltered:
            print(nationPair[0] + " and " + nationPair[1])
    print("")
    print("= add or remove a filter =")
    displayMenu(nationMenuItems)

    while(True):
        try:
            firstNation = int(input("Select the first nation: "))
            break
        except ValueError:
            print("invalid value")
    while(True):
        try:
            secondNation = int(input("Select the second nation: "))
            break
        except ValueError:
            print("invalid value")
    nationPair = [nationMenuItems[firstNation], nationMenuItems[secondNation]]
    nationPair.sort()
    if nationPair in nationsFiltered:
        nationsFiltered.remove(nationPair)
    else:
        nationsFiltered.append(nationPair)
    if len(nationsFiltered) == 0:
        print("no current filters")
    else:
        print("current nations to be separated:")
        for nationPair in nationsFiltered:
            print(nationPair[0] + " and " + nationPair[1])

    print("")



def nationsToGroup():
    if len(nationsGrouped) == 0:
        print("no current filters")
    else:
        print("current nations to be grouped:")
        for nationPair in nationsGrouped:
            print(nationPair[0] + " and " + nationPair[1])
    print("")
    print("= add or remove a filter =")
    displayMenu(nationMenuItems)
    while(True):
        try:
            firstNation = int(input("Select the first nation: "))
            break
        except ValueError:
            print("invalid value")
    while(True):
        try:
            secondNation = int(input("Select the second nation: "))
            break
        except ValueError:
            print("invalid value")
    nationPair = [nationMenuItems[firstNation], nationMenuItems[secondNation]]
    nationPair.sort()
    if nationPair in nationsGrouped:
        nationsGrouped.remove(nationPair)
    else:
        nationsGrouped.append(nationPair)
    if len(nationsGrouped) == 0:
        print("no current filters")
    else:
        print("current nations to be grouped:")
        for nationPair in nationsGrouped:
            print(nationPair[0] + " and " + nationPair[1])

    print("")

def calculate():
    nationNames = list(nationForces.keys())
    forceNumbers = list(nationForces.values())
    allOptions = list(itertools.combinations(nationNames,3))
    allOptions.extend(list(itertools.combinations(nationNames,4)))
    allOptions.extend(list(itertools.combinations(nationNames,5)))

    filteredByForce = []
    filteredBySeparate = []
    options = []

    # is correct force number
    for option in allOptions:
        optionForces = [nationForces[x] for x in option]
        if sum(optionForces) >= forceBounds["Min"] and sum(optionForces) <= forceBounds["Max"]:
            filteredByForce.append(option)

    # has separated the required nations
    for option in filteredByForce:
        for nationPair in nationsFiltered:
            #if both are there then should be filtered. if neither are there then should be filtered
            if (nationPair[0] in option and nationPair[1] in option) or (nationPair[0] not in option and nationPair[1] not in option):
                continue
            else:
                filteredBySeparate.append(option)

    # has grouped the required nations
    for option in filteredBySeparate:
        for nationPair in nationsGrouped:
            #if only one is there then should be filtered
            if (nationPair[0] in option and nationPair[1] not in option) or (nationPair[0] not in option and nationPair[1] in option):
                continue
            else:
                options.append(option)

    if len(options) == 0:
      print "No valid force options for current setup."
      return
      
    print("Valid forces by number:")
    optioncount = 1
    prevOptions = []
    pairedDays = []
    for option in options:
        day1 = option
        day2 = [key for key, val in nationForces.items() if key not in option]
        if tuple(day2) in prevOptions:
            continue
        else:
            print("== option " + str(optioncount) + "==")
            print("day 1: " + ", ".join(day1) + " | force: " + str(sum([nationForces[x] for x in day1])))
            print("day 2: " + ", ".join(day2) + " | force: " + str(sum([nationForces[x] for x in day2])))
            pairedDays.append([day1, day2])
            prevOptions.append(day1)
            optioncount = optioncount+1

    while(True):
        export = input("Export as .CSV? Y/n\n")
        if export == "Y":
            exportOptions(pairedDays)
            break
        if export == "n" or export == "N":
            break

def listData():
    print("Min force: " + str(forceBounds["Min"]))
    print("Max force: " + str(forceBounds["Max"]))
    print("Force numbers are:")
    for nationName in nationForces:
        print(nationName + ": " + str(nationForces[nationName]))
    print("current nations to be separated:")
    for nationPair in nationsFiltered:
        print(nationPair[0] + " and " + nationPair[1])
    print("current nations to be grouped:")
    for nationPair in nationsGrouped:
        print(nationPair[0] + " and " + nationPair[1])

    print("\npress enter to continue\n")

def exportOptions(pairedDays):
    filename = input("Input a file name (without file extension)\n")
    with open(filename+".csv",'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dataWriter.writerow(['Number', 'Day', 'Force Total', 'Nations', 'Nation 1', 'Nation 1 Force', 'Nation 2', 'Nation 2 Force', 'Nation 3', 'Nation 3 Force', 'Nation 4', 'Nation 4 Force', 'Nation 5', 'Nation 5 Force', 'Nation 6', 'Nation 6 Force', 'Nation 7', 'Nation 7 Force'])
        optNumber = 1
        for option in pairedDays:
            day1 = " ".join(option[0])
            day1ForceTotal = sum([nationForces[x] for x in option[0]])
            day2 = " ".join(option[1])
            day2ForceTotal = sum([nationForces[x] for x in option[1]])
            row1 = [optNumber, 1, day1ForceTotal, day1]
            for nation in option[0]:
                row1.append(nation)
                row1.append(nationForces[nation])
            row2 = [optNumber, 2, day2ForceTotal, day2]
            for nation in option[1]:
                row2.append(nation)
                row2.append(nationForces[nation])
            dataWriter.writerow(row1)
            dataWriter.writerow(row2)
            optNumber = optNumber+1

if __name__ == "__main__":
    main()
