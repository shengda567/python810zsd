import unittest
import os
from homework10.HW10_ShengDa_Zhang import *


class TestSuitHW109(unittest.TestCase):
    def setUp(self):
        self.test_path = "E:\sww810\homework10"
        self.repo = Repository(self.test_path, False)
    def test_student_data(self):

        calculated = {cwid: student.pt_row() for cwid, student in self.repo._students.items()}

        expected = {'10103': ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, None],
                    '10115': ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, None],
                    '10172': ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], {'SSW 540', 'SSW 564'}, {'CS 545', 'CS 501', 'CS 513'}],
                    '10175': ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], {'SSW 540', 'SSW 555'}, {'CS 545', 'CS 501', 'CS 513'}],
                    '10183': ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], {'SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'}, {'CS 545', 'CS 501', 'CS 513'}],
                    '11399': ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], {'SYS 671', 'SYS 612', 'SYS 800'}, None],
                    '11461': ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], {'SYS 671', 'SYS 612'}, {'SSW 565', 'SSW 810', 'SSW 540'}],
                    '11658': ['11658', 'Kelly, P', 'SYEN', [], {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 565', 'SSW 810', 'SSW 540'}],
                    '11714': ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], {'SYS 671', 'SYS 612', 'SYS 800'}, {'SSW 565', 'SSW 810', 'SSW 540'}],
                    '11788': ['11788', 'Fuller, E', 'SYEN', ['SSW 540'], {'SYS 671', 'SYS 612', 'SYS 800'}, None]}
        self.assertEqual(calculated, expected)

    def test_instructors_data(self):

        calculated = {tuple(content) for instructor in self.repo._instructors.values() for content in instructor.pt_row()}

        expected = {('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                         ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                         ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                         ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                         ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                         ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                         ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                         ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                         ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                         ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                         ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1),
                         ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3)}

        self.assertEqual(calculated, expected)

    def test_major_data(self):
        calculated = {dept: courses.pt_row() for dept, courses in self.repo._majors.items()}
        print(calculated)

        expected = {'SFEN': ['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']],
                    'SYEN': ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]}

        self.assertEqual(calculated, expected)


if __name__ == '__main__':
    unittest.main()
