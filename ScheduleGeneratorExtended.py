import sys
import time

class RoomInfo:
  def __init__(self, id, capacity, school):
    self.id = id
    self.capacity = capacity
    self.times = []
    self.school = school

class TimeInfo:
  def __init__(self, start, end, days):
    self.start = start
    self.end = end
    self.days = days
    self.overlap = []

class ClassInfo:
  def __init__(self, id, dept, level, prof, days, time, school):
    self.id = id
    self.dept = dept
    self.level = level
    self.prof = prof
    self.days = days
    self.time = time
    self.school = school

class ProfessorInfo:
  def __init__(self, id):
    self.id = id
    self.classes = []
    self.times = []

class ScheduledClass:
  def __init__(self, id, time, room, capacity, prof, school):
    self.id = id
    self.time = time
    self.room = room
    self.capacity = capacity
    self.prof = prof
    self.numEnrolled = 0
    self.students = []
    self.school = school

def createSchedule(constraints, studentprefs, finalschedule):
  start = time.perf_counter()

  fileC = open(constraints, "r")
  fileP = open(studentprefs, "r")
  s = 0
  c = 0
  r = 0
  t = 0
  p = 0
  rooms = []
  times = []
  classPopularity = []
  professors = []
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
        room = RoomInfo(int(rinfo[0]), int(rinfo[1]), int(rinfo[2]))
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
        cls = ClassInfo(int(cinfo[0]), int(cinfo[1]), int(cinfo[2]), int(cinfo[3]), int(cinfo[4]), int(cinfo[5]), int(cinfo[6]))
        classPopularity.append(cls)
        professors[int(cinfo[1])-1].classes.append(int(cinfo[0]))
    line = fileC.readline()
  fileC.close()

  #Get preference info
  optPrefVal = 0
  line = fileP.readline()
  l = line.split()
  s = int(l[1])
  studentPreferences = []
  for i in range(0,s):
    line = fileP.readline()
    l = line.split()
    studentPreferences.append(l[1:])
    optPrefVal += len(l) - 1
  fileP.close()

  times.sort(key = lambda x: x.start)
  for i in range(0,t):
    for j in range(0,t):
      if (times[j].end >= times[i].start and times[j].end <= times[i].end) or (times[j].start <= times[i].end and times[j].start >= times[i].start) or (times[j].start <= times[i].start and times[j].end >= times[i].end) or (times[j].start >= times[i].start and times[j].end <= times[i].end):
        if times[i].days in times[j].days or times[j].days in times[i].days:
          times[i].overlap.append(times[j])

  roomsSorted = sorted(rooms, key = lambda x: x.capacity, reverse = True)
  classPopularity.sort(key = lambda x: x.level)
  #classPopularity.sort(key = lambda x: x.dept)
  #times.sort(key = lambda x: len(x.overlap))

  schedule = [None] * c
  # currT = 0
  # length = c
  # for i in range(0,c):
  #  slot = times[currT]
  #  room = None
  #  for rm in roomsSorted:
  #    if slot not in rm.times:
  #      room = rm
  #      break
  #  cls = classPopularity[-1]
  #  professor = professors[cls.prof-1]
  #  idx = -1
  #  while slot in professor.times and idx > -length:
  #    idx -= 1
  #    temp = classPopularity[idx]
  #    professor = professors[temp.prof-1]
  #  if slot not in professor.times and room != None:
  #      cls = classPopularity.pop(idx)
  #      length -= 1
  #      scheduledCls = ScheduledClass(cls.id, slot, room.id, room.capacity, cls.prof)
  #      schedule[cls.id-1] = scheduledCls
  #      professor.times.append(slot)
  #      professor.times.extend(slot.overlap)
  #      room.times.append(slot)
  #      room.times.extend(slot.overlap)
  #  currT += 1
  #  if currT >= t:
  #    currT = 0

  roomBusy = {room.id: [False] * t for room in rooms}
  for cls in classPopularity:
    professor = professors[cls.prof-1]
    for room in roomsSorted:
      for i in range(0, t):
        slot = times[i-1]
        if not roomBusy[room.id][i-1] and room.school == cls.school and slot not in professor.times and slot not in room.times and len(slot.days) >= cls.days and (slot.end - slot.start) >= cls.time:
          scheduledCls = ScheduledClass(cls.id, slot, room.id, room.capacity, cls.prof, cls.school)
          schedule[cls.id-1] = scheduledCls
          roomBusy[room.id][i-1] = True
          if slot not in professor.times:
            professor.times.append(slot)
            for o in slot.overlap:
              if o not in professor.times:
                professor.times.append(o)
          if slot not in room.times:
            room.times.append(slot)
            for o in slot.overlap:
              if o not in room.times:
                room.times.append(o)
          break
      if schedule[cls.id-1] is not None:
        break

  end = time.perf_counter()
  elapsedtime = end - start
  print(f"Runtime: {elapsedtime}")

  #Enroll students
  prefVal = 0
  studentBusy = [[] for _ in range(s)]
  studentEnrolled = [[] for _ in range(s)]
  for i in range(0,s):
    for j in studentPreferences[i]:
        cls = schedule[int(j)-1]
        enroll = True
        if cls == None or cls.numEnrolled >= cls.capacity or cls.time in studentBusy[i]:
            enroll = False
        for e in studentEnrolled[i]:
            if cls != None and cls.school != e.school and (cls.time.days in e.time.days or e.time.days in cls.time.days) and (cls.time.start - e.time.end < 30 or e.time.start - cls.time.end < 30):
                enroll = False
                break
        if enroll:
          studentEnrolled[i].append(cls)
          cls.students.append(i+1)
          cls.numEnrolled += 1
          if cls.time not in studentBusy[i]:
            studentBusy[i].append(cls.time)
          for o in cls.time.overlap:
            if o not in studentBusy[i]:
              studentBusy[i].append(o)
          prefVal += 1

  #Output preference value and fit
  print(f"Student Preference Value: {prefVal}")
  print(f"Best Case Student Preference Value: {optPrefVal}")
  print(f"Fit Ratio: {prefVal / (optPrefVal)}")

  #Write to output
  fileS = open(finalschedule, "w")
  fileS.write("Course\tRoom\tTeacher\tStart Time\tEnd Time\tDays\tStudents\n")
  for cls in schedule:
    if cls is None:
      continue
    fileS.write(str(cls.id) + "\t" + str(cls.room) + "\t" + str(cls.prof) + "\t" + str(cls.time.start) + "\t" + str(cls.time.end) + "\t" + str(cls.time.days) + "\t")
    for student in cls.students:
      fileS.write(str(student) + " ")
    fileS.write("\n")
  fileS.close()

def main():
  constraints = str(sys.argv[1])
  studentprefs = str(sys.argv[2])
  schedule = str(sys.argv[3])
  createSchedule(constraints, studentprefs, schedule)

if __name__ == "__main__":
  main()