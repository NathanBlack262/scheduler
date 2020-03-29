import csv


TOLERANCE_VALUE = 5

class Class:
    def __init__(self, name, section, days, times):
        self.is_lab = False
        self.name = name
        if self.name[len(self.name)-4:len(self.name)] == "Lab)":
            self.is_lab = True
        self.section = section
        self.days = list(days)
        self.daysString = days
        self.timesString = times
        self.begin_time = int(times[0:2]) * 60 + int(times[2:4])
        self.end_time = int(times[5:7]) * 60 + int(times[7:9])
    def conflicts_with(self, anotherClass):
        if (len(list(set().union(self.days, anotherClass.days))) != (len(self.days) + len(anotherClass.days))) and (anotherClass.end_time + TOLERANCE_VALUE <= self.begin_time or self.end_time + TOLERANCE_VALUE <= anotherClass.begin_time): #for classes with a day conflict, is there a time conflict
            return False
        if len(list(set().union(self.days, anotherClass.days))) == (len(self.days) + len(anotherClass.days)): #is there a day conflict
            return False
        return True
    def __str__(self):
        return self.name[0:9] + "." + self.section + self.name[10:] + " Times: " + self.daysString + " " + self.timesString
        


def takeInFileName():
    goodFile = False
    print("Hello, and thank you for using Nathan Black's College Scheduler!")
    userFileName = ""
    while not goodFile:
        name = input("What is the name of the .csv file you would like to use for scheduling? (do not add .csv or use quotes) ")
        try:
            userFileName = name + ".csv"
            with open(userFileName) as csvfile:
                pass
            goodFile = True
        except:
            print("You have not entered a valid or existing file name. Please check your spelling and try again.")
    print("Using " + userFileName + " for scheduling.")
    return userFileName

def createClasses(data):
    classes = []
    for i in range(len(data)):
        classes.append(Class(data[i][0], data[i][1], data[i][2], data[i][3]))
    return classes

def establishPriority(classes):
    classNames = []
    priorityList = []
    for each in classes:
        if each.name not in classNames:
            classNames.append(each.name)
    classNames.sort()
    while classNames:
        goodKey = False
        for i in range(1, len(classNames) + 1):
            print(str(i) + ". " + classNames[i-1])
        priorityKey = input("Which class do you prioritize most in your schedule? (Use the numbers provided) ")
        try:
            priorityKey = int(priorityKey)
            if priorityKey >= 1 and priorityKey <= len(classNames):
                goodKey = True
                priorityList.append(classNames[priorityKey-1])
                classNames.pop(priorityKey-1)
            else:
                print("Please enter a number within the range of choices provided. Please check your input and try again.")
        except:
            print("A valid numeric key was not entered. Please check your input and try again.")
    return priorityList


def createSearchablePriorities(priorityList, classes):
    searchablePriorities = [[] for i in range(len(priorityList))]
    for i in range(len(priorityList)):
        for each in classes:
            if priorityList[i] == each.name:
                searchablePriorities[i].append(each)
    return searchablePriorities

def findSchedules(searchablePriorities):
    chosenClasses = []
    for i in range(len(searchablePriorities[0])):
        chosenClasses.append(searchablePriorities[0][i])
        chosenClasses = checkForConflicts(searchablePriorities[1:], chosenClasses)
        chosenClasses = []

def checkForConflicts(searchablePriorities, chosenClasses):
    originalLength = len(chosenClasses)
    for each in searchablePriorities[0]:
        noConflicts = True
        for those in chosenClasses:
            if (those.conflicts_with(each)):
                noConflicts = False
        if noConflicts:
            chosenClasses.append(each)
            if len(searchablePriorities) == 1:
                print("Appropriate schedule found.")
                for them in chosenClasses:
                    print(them)
                print()
                chosenClasses.pop(len(chosenClasses)-1)
            else:
                checkForConflicts(searchablePriorities[1:], chosenClasses)
    chosenClasses = chosenClasses[0:originalLength]
    return chosenClasses
        
            
def main():
    with open(takeInFileName(), newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        data = [row for row in reader]
        classes = createClasses(data)
        priorityList = establishPriority(classes)
        searchablePriorities = createSearchablePriorities(priorityList, classes)
        findSchedules(searchablePriorities)
        
        


if __name__ == "__main__":
    main()