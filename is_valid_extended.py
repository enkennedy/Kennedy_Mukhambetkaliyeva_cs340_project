import sys
from time import time

p = 0
r = 0
c = 0
s = 0
studentPrefs = []
professors = []
rooms = []
times = []
classes = []
scheduledClasses = []

class RoomInfo:
  def __init__(self, id, capacity):
    self.id = id
    self.capacity = capacity
    self.times = []

class TimeInfo:
  def __init__(self, start, end, days):
    self.start = start
    self.end = end
    self.days = days

class ClassInfo:
  def __init__(self, id, dept, level, prof, days, time):
    self.id = id
    self.dept = dept
    self.level = level
    self.prof = prof
    self.days = days
    self.time = time

class ProfessorInfo:
  def __init__(self, id):
    self.id = id
    self.classes = []
    self.times = []


def readConstraints(constraints):
    global p, r, c, s, studentPrefs, professors, rooms, classes
    fileC = open(constraints, "r")
    line = fileC.readline() 
      #Get constraint info
    while line:
        l = line.split()
        if l[0] == "Class" and l[1] == "Times":
            t = int(l[2])
            for i in range(0,t):
                line = fileC.readline()
                tinfo = line.split()
                times.append(TimeInfo(int(tinfo[0]),int(tinfo[1]),str(tinfo[2])))
        if l[0] == "Rooms":
            r = int(l[1])
            for i in range(0,r):
                line = fileC.readline()
                rinfo = line.split()
                room = RoomInfo(int(rinfo[0]), int(rinfo[1]))
                rooms.append(room)
        if l[0] == "Classes":
            c = int(l[1])
        if l[0] == "Teachers":
            p = int(l[1])
            for i in range(0,p):
                prof = ProfessorInfo(i + 1)
                professors.append(prof)
            for j in range(0,c):
                line = fileC.readline()
                cinfo = line.split()
                cls = ClassInfo(int(cinfo[0]), int(cinfo[1]), int(cinfo[2]), int(cinfo[3]), int(cinfo[4]), int(cinfo[5]))
                classes.append(cls)
                professors[int(cinfo[1])-1].classes.append(int(cinfo[0]))
        line = fileC.readline()
    fileC.close()

def readStudentPrefs(studentprefs):
    global s, studentPrefs
    fileP = open(studentprefs, "r")
    line = fileP.readline()
    l = line.split()
    s = int(l[1])
    studentPrefs = [[] for _ in range(s)]
    for i in range(0,s):
        line = fileP.readline()
        l = line.split()
        studentPrefs[i] = l[1:]
    fileP.close()

def isValid(schedule):
    global p, r, c, s, studentPrefs, professors, rooms, classes, scheduledClasses

    fileS = open(schedule, "r")
    line = fileS.readline()
    if line != "Course\tRoom\tTeacher\tStart Time\tEnd Time\tDays\tStudents\n":
        print("Invalid schedule header format\n")
        exit(1)

    line = fileS.readline()
    while line:
       line = line.rstrip()
       l = line.split("\t")
       line = fileS.readline()
    
    #Check each course only scheduled once
    classID = int(l[0])
    if classID not in scheduledClasses:
        scheduledClasses.append(classID)
    else:
        print("Class " + str(classID) + " scheduled more than once\n")
        exit(1)

    #Check room has enough capacity for students
    roomID = int(l[1])
    if len(l) < 7:
        enrolled = []
    else:
        enrolled = l[6].split()
    if len(enrolled) > rooms[roomID-1].capacity:
        print("Room " + str(roomID) + " does not have enough capacity for class " + str(classID) +"\n")
        exit(1)
    
    #Check course has the correct professor
    profID = int(l[2])
    if profID != classes[classID-1].prof:
        print("Class " + str(classID) + " does not have the correct professor\n")
        exit(1)

    #Check no professor conflicts
    sTime = int(l[3])
    eTime = int(l[4])
    days = str(l[5])
    for time in professors[profID-1].times:
        strt = time.start
        end = time.end
        if (end >= sTime and end <= eTime) or (strt <= eTime and strt >= sTime) or (strt <= sTime and end >= eTime) or (strt >= sTime and end <= eTime):
            if days in time.days or time.days in days:
                print("Professor " + str(profID) + " is scheduled for multiple classes at the same time\n")
                exit(1)
        else:
            professors[profID-1].times.append(TimeInfo(sTime, eTime, days))

    #Check no room conflicts
    for time in rooms[roomID-1].times:
        strt = time.start
        end = time.end
        if (end >= sTime and end <= eTime) or (strt <= eTime and strt >= sTime) or (strt <= sTime and end >= eTime) or (strt >= sTime and end <= eTime):
            if days in time.days or time.days in days:
                print("Room " + str(roomID) + " has multiple classes scheduled at the same time\n")
                exit(1)
        else:
            rooms[roomID-1].times.append(TimeInfo(sTime, eTime, days))
    
    #Check no student conflicts
    #Check students only enrolled in courses they requested
    studentTimes = [[] for _ in range(s)]
    for stdt in enrolled:
        if str(classID) not in studentPrefs[int(stdt)-1]:
            print("Student " + str(stdt) + " is enrolled in a class they did not request\n")
            exit(1)
        for time in studentTimes[int(stdt)-1]:
            strt = time.start
            end = time.end
            if (end >= sTime and end <= eTime) or (strt <= eTime and strt >= sTime) or (strt <= sTime and end >= eTime) or (strt >= sTime and end <= eTime):
                if days in time.days or time.days in days:
                    print("Student " + str(stdt) + " is scheduled for multiple classes at the same time\n")
                    exit(1)
            else:
                studentTimes[int(stdt)-1].append(TimeInfo(sTime, eTime, days))

    print("Schedule is valid\n")

if len(sys.argv) != 4:
  print ("Usage: " + sys.argv[0] + " <constraints.txt> <student_prefs.txt> <schedule.txt>")
  exit(1)

readConstraints(sys.argv[1])
readStudentPrefs(sys.argv[2])
isValid(sys.argv[3])

