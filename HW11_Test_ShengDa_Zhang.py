import unittest
from homework11.HW11_ShengDa_Zhang import *


class TestSuit(unittest.TestCase):
    def setUp(self):
        self.test_path = "E:\sww810\homework11"
        self.repo = Repository(self.test_path, False)
    def test_student_data(self):

        expect_majors = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']],
                         ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]

        expect_students = [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], {'SSW 540', 'SSW 555'}, None],
                           ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], {'SSW 540', 'SSW 555'}, {'CS 501', 'CS 546'}],
                           ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], {'SSW 540'}, {'CS 501', 'CS 546'}],
                           ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], {}, None],
                           ['11717', 'Kernighan, B', 'CS', [], {'CS 570', 'CS 546'}, {'SSW 565', 'SSW 810'}]]

        expect_instructors = [('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                              ('98762', 'Hawking, S', 'CS', 'CS 546', 2),
                              ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
                              ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                              ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4)]

        majors = [major.pt_row() for major in self.repo._majors.values()]
        students = [student.pt_row() for student in self.repo._students.values()]
        instructors = self.repo.instructor_table_db("810_startup.db")
        self.assertEqual(majors,expect_majors)
        self.assertEqual(students,expect_students)
        self.assertEqual(instructors,expect_instructors)

if __name__ == '__main__':
    unittest.main()
