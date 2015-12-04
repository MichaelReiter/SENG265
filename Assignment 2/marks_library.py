import libxml2
import sys

'''
purpose
  return the course mark for student s
preconditions
  student is a list of the form:
    [last_name, first_name, student_id, marks]
    where
    marks is a list of the form: [ [assignment_id,score], ... ]
  assignments is a dictionary of the form:
    {mark_id:[points, percentage], ... }
'''
def compute_mark(student, assignments):
  marks = student[3]

  sum = 0
  for mark in marks:
    assignment_id = mark[0]
    points = mark[1]
    total = assignments[assignment_id][0]
    weight = assignments[assignment_id][1]
    score = 1.0 * points / total #multiply by 1.0 to implicitly convert to float
    sum += score * weight
  return sum

'''
purpose
  extract the information from a and return it as a list:
    [mark_id, points, percentage]
preconditions
  s is an assignment element from a legal students XML file
'''
def extract_assignment(a):
  list = [0,0,0]  # initialize list (soon to be overwritten with proper values)
  while a is not None:
    if a.name == "mark_id":
      list[0] = a.content
    if a.name == "points":
      list[1] = int(a.content)
    if a.name == "percentage":
      list[2] = float(a.content)
    a = a.next
  return list

'''
purpose
  extract the information from s and return it as a list:
    [last_name, first_name, student_id, marks]
    where
    marks is a list of the form: [ [assignment_id,score], ... ]
preconditions
  s is a student element from a legal students XML file
'''
def extract_student(s):
  list = [0,0,0,0]
  while s is not None:
    if s.name == "last_name":
      list[0] = s.content
    if s.name == "first_name":
      list[1] = s.content
    if s.name == "student_id":
      list[2] = s.content
    if s.name == "marks":

      # iterate through marks
      m = s.children
      marks = []
      while m is not None:
        if m.name == "mark":

          # iterate through each mark
          q = m.children
          mark = [0, 0]
          while q is not None:
            if q.name == "mark_id":
              mark[0] = q.content
            if q.name == "score":
              mark[1] = int(q.content)
            q = q.next

          marks.append(mark)
        m = m.next
      list[3] = marks
    s = s.next
  return list
