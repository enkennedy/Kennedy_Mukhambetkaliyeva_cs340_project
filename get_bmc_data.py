import re
import sys
import pandas as pd

class Course:
    def __init__(self, id, prof, dept, level, days, time, school, building):
        self.id = id
        self.prof = prof
        self.dept = dept
        self.level = level
        self.days = days
        self.time = time
        self.school = school
        self.building = building

def getData(csv, constraints, prefs):

    #Read in csv data and assign integer ids
    data = pd.read_csv(csv)

    courses = {}
    depts = {}
    profs = {}
    times = []
    students = {}
    rooms = {}
    buildings = {}

    currStudent = 1
    currCourse = 1
    currDept = 36
    deptRankings = {"MATH":1, "BIOL":2, "PSYC":3, "ECON":4, "SOCL":5, "POLS":6, "CHEM":7, "ENGL":8,
             "INST":9, "CMSC":10, "PHSY":11, "CITY":12, "ANTH":13, "HART":14, "HIST":15, "LING":16,
             "ARTF":17, "ARTS":17, "FREN":18, "EDUC":19, "CSTS":20, "PHIL":21, "RUSS":22, "GEOL":23, "SPAN":24,
             "ARCH":25, "COML":26, "EALC":27, "EAST":27, "ITAL":28, "MUSC":29, "RELG":30, "ASTR":31,
             "ARTW":32, "ENVS":33, "GERM":34, "NEUR":35}
    currProf = 1
    currRoom = 1
    currBuilding = 1
    
    for index, row in data.iterrows():

        school = 1
        if "College" in data.columns:
            college = str(row["College"])
            if college == "H":
                school = 2

        room = str(row["Facil ID 1"])
        building = re.sub(r'\d+', '', room)
        if building not in buildings:
            buildings[building] = currBuilding
            currBuilding += 1
        if room not in rooms:
            rooms[room] = [currRoom, 0, school, buildings[building]]
            currRoom += 1
        rooms[room][1] += 1

        t = str(row["Start_1"])
        t2 = t.split(":")
        if "AM" in t:
            if int(t2[0]) == 12:
                sTime = int(t2[1][0:2])
            else:
                sTime = 60 * int(t2[0]) + int(t2[1][0:2])
        else:
            if int(t2[0]) == 12:
                sTime = 12 * 60 + int(t2[1][0:2])
            else:
                sTime = 60 * (int(t2[0]) + 12) + int(t2[1][0:2])
        t = str(row["End 1"])
        t2 = t.split(":")
        if "AM" in t:
            if int(t2[0]) == 12:
                eTime = int(t2[1][0:2])
            else:
                eTime = 60 * int(t2[0]) + int(t2[1][0:2])
        else:
            if int(t2[0]) == 12:
                eTime = 12 * 60 + int(t2[1][0:2])
            else:
                eTime = 60 * (int(t2[0]) + 12) + int(t2[1][0:2])
        days = str(row["Days 1"]).replace(" ", "")
        if days == "M-F":
            days = "MTWRF"
        if "TH" in days:
            days = days.replace("TH", "R")
        time = [sTime, eTime, days]
        if time not in times:
            times.append(time)

        course = int(row["Course ID"])
        if course not in courses:
            dept = str(row["Subject"])
            if dept not in deptRankings and dept not in depts:
                depts[dept] = currDept
                currDept += 1
            elif dept in deptRankings and dept not in depts:
                depts[dept] = deptRankings[dept]
            if "Catalog" in data.columns:
                level = str(row["Catalog"])[1]
            else:
                level = str(row["Level"])
            prof = str(row["Instructor ID"])
            if prof not in profs:
                profs[prof] = currProf
                currProf += 1
            if days == "nan":
                cTime = 0
            else:
                cTime = len(days)
            c = Course(currCourse, profs[prof], depts[dept], level, cTime, eTime-sTime, school, rooms[room][3])
            courses[course] = c
            currCourse += 1

        if "Student ID" in data.columns:
            student = int(row["Student ID"])
        else:
            student = str(row["Student"])
        if student not in students:
            students[student] = [currStudent]
            currStudent += 1
        students[student].append(courses[course].id)

    #Write data to constraints
    fileC = open(constraints, "w")
    fileC.write("Class Times\t" + str(len(times)) + "\n")
    for slot in times:
        fileC.write(str(slot[0]) + "\t" + str(slot[1]) + "\t" + slot[2] + "\n")
    fileC.write("Rooms\t" + str(len(rooms)) + "\n")
    for r in rooms.values():
        fileC.write(str(r[0]) + "\t" + str(r[1]) + "\t" + str(r[2]) + "\t" + str(r[3]) + "\n")
    fileC.write("Classes\t" + str(len(courses)) + "\n")
    fileC.write("Teachers\t" + str(len(profs)) + "\n")
    for c in courses.values():
        fileC.write(str(c.id) + "\t" + str(c.dept) + "\t" + str(c.level) + "\t" + str(c.prof) + "\t" + str(c.days) + "\t" + str(c.time) + "\t" + str(c.school) + "\t" + str(c.building) + "\n")
    fileC.close()

    #Write data to prefs
    fileP = open(prefs, "w")
    fileP.write("Students\t" + str(len(students)) + "\n")
    for s in students.values():
        fileP.write(str(s[0]) + "\t")
        for cls in s[1:]:
            fileP.write(str(cls) + " ")
        fileP.write("\n")
    fileP.close()


if len(sys.argv) != 4:
  print ("Usage: " + sys.argv[0] + " <enrollment.csv> <student_prefs.txt> <constraints.txt>")
  exit(1)

getData(sys.argv[1], sys.argv[2], sys.argv[3])