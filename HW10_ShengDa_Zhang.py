import os
from collections import defaultdict

from prettytable import PrettyTable

from homework8.HW08_ShengDa_Zhang import file_reading_gen


class Student:
    """"
        - CWID
        - name
        - department
        - course/grade
    """
    PT_FIELDS = ['CWID', 'Major', 'Course', 'Completed Courses', 'Remaining Required', 'Ramaining Eletives']

    def __init__(self, cwid, name, major_name, major):
        self._cwid = cwid
        self._name = name
        self._major_name = major_name
        self._major = major  #instance of class Major corresponding to this student's major
        self._courses = defaultdict(str) #_course[course] = grade

    def add_course(self, course, grade):
        """store the grade associated with a course for this student """
        self._courses[course] = grade
        if self._courses[course] == "":
            print(f"{self._cwid} student does not have a grade")

    def pt_row(self):
        """return a list of values needed in the pretty table for one student (me)"""
        passed = self._major.pass_courses(self._courses)
        rem_required = self._major.remaining_required(self._courses)
        rem_electieves = self._major.remaining_electives(self._courses)

        return [self._cwid, self._name, self._major_name, sorted(passed), rem_required, rem_electieves]

class Instructor:

    """"
        - CWID
        - name
        - department
        - course/#students
    """
    PT_FIELDS = ['CWID', 'Name', 'Dept', 'Course', '# Student']

    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int) #track_courses[coures] = # of studens

    def add_course(self, course):
        """Note that the instructor taught another course to the student"""
        self._courses[course] += 1

    def pt_row(self):
        for course, student in self ._courses.items():
            yield [self._cwid, self._name, self._dept, course, student]

class Repository:
        """
            Need to know:
            - students
            - instructors
            intialize everything
            read files
            print pretty tables
        """
        def __init__(self, path, ptable=False):
            self._students = dict() #student[cwid] = Student
            self._instructors = dict() #instructors [cwid] = Instructor
            self._majors = dict() #_major[dept] = instance of class
            self._get_majors(os.path.join(path, "majors.txt"))
            self._get_students(os.path.join(path, "students.txt"))
            self._get_instructors(os.path.join(path, "instructors.txt"))
            self._get_grades(os.path.join(path, "grades.txt")) #use cwid get


            if ptable:
                self.student_prettytable()
                self.instructor_prettytable()
                self.major_prettytable()

        def _get_students(self, path):
            """read the students and populate self._studens"""
            try:
                for cwid, name, major_name in file_reading_gen(path, 3, sep=';', header=True):
                    self._students[cwid] = Student(cwid, name, major_name, self._majors[major_name])
            except KeyError as ke:
                print(ke,"this student's major is not in the major.txt")
            except FileNotFoundError as fnfe:
                print(fnfe)
            except ValueError as ve:
                print(ve)

        def _get_instructors(self, path):
            """read the instructors and populate self._instructors"""
            try:
                for cwid, name, dept in file_reading_gen(path, 3, sep='|', header=True):
                    self._instructors[cwid] = Instructor(cwid, name, dept)
            except FileNotFoundError as fnfe:
                print(fnfe)
            except ValueError as ve:
                print(ve)

        def _get_grades(self, path):
            try:
                for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='|', header = True):
                    if student_cwid in self._students:
                        self._students[student_cwid].add_course(course, grade) #tell the student about a course
                    else:
                        print(f"Found grade for unknowm student {student_cwid}")

                    if instructor_cwid in self._instructors:
                        self._instructors[instructor_cwid].add_course(course) #tell the instructor about a course/student
                    else:
                        print(f"Found grade for unknowm instructor {instructor_cwid}")

            except FileNotFoundError as fnfe:
                print(fnfe)
            except ValueError as ve:
                print(ve)

        def _get_majors(self, path):
            try:
                for major, RE, course in file_reading_gen(path, 3, "\t", header=True):
                    self._majors[major] = Major(major)

                for major, RE, course in file_reading_gen(path, 3, "\t", header=True):
                    if major in self._majors:
                        self._majors[major].add_course(course, RE)

            except FileNotFoundError as fnfe:
                print(fnfe)
            except ValueError as ve:
                print(ve)

        def student_prettytable(self):
            """print the student pretty table"""
            pt = PrettyTable(field_names=Student.PT_FIELDS)

            for student in self._students.values():
                pt.add_row(student.pt_row())
        
            print(pt)

        def instructor_prettytable(self):
            """print the student pretty table"""
            pt = PrettyTable(field_names=Instructor.PT_FIELDS)

            for instructor in self._instructors.values():
                for content in instructor.pt_row():
                    pt.add_row(content)

            print(pt)

        def major_prettytable(self):
            pt = PrettyTable(field_names=Major.PT_FIELDS)
            for dept in self._majors.values():
                pt.add_row(dept.pt_row())

            print(pt)


class Major:
    PT_FIELDS = ['Dept', 'Required', 'Electives']

    def __init__(self, dept):
        self._dept = dept
        self._required = set()  #set of required courses
        self._electives = set() #set of elective courses

    def add_course(self, course, flag):
        #add course to required or electives based on flag
        if flag is "R":
            self._required.add(course)
        if flag is "E":
            self._electives.add(course)
    def pass_courses(self, course_grades):
        """get course_grades[course] = grade from the Student
        return a set of passed courses base on the course and grade"""
        passed_courses = set()
        for course, grade in course_grades.items():
            if grade and grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+','C']:
                passed_courses.add(course)

        return passed_courses

    def remaining_required(self, course_grades):
         rem_required = self._required - self.pass_courses(course_grades)

         return rem_required

    def remaining_electives(self, course_grades):
        rem_electives = self._electives - self.pass_courses(course_grades)
        if len(rem_electives) < 3:
            rem_electives = None

        return rem_electives

    def pt_row(self):
        return [self._dept, sorted(self._required), sorted(self._electives)]


def main():
    stevens = Repository("E:\sww810\homework10", ptable=True)
    #njit = Repository("E:\sww810\homework9", ptable=True)

if __name__ == '__main__':
    main()