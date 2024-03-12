import unittest
from datetime import date
from employee import Employee
from relations_manager import RelationsManager
from employee_manager import EmployeeManager 

class TestEmployeeRelationsManager(unittest.TestCase):

    def setUp(self):
        self.rm = RelationsManager()

    def test_team_leader_john_doe(self):
        john_doe = Employee(id=1, first_name="John", last_name="Doe", base_salary=3000,
                            birth_date=date(1970, 1, 31), hire_date=date(1990, 10, 1))
        self.assertTrue(self.rm.is_leader(john_doe))

    def test_team_members_john_doe(self):
        john_doe = Employee(id=1, first_name="John", last_name="Doe", base_salary=3000,
                            birth_date=date(1970, 1, 31), hire_date=date(1990, 10, 1))
        expected_team_members = [2, 3]
        team_members = self.rm.get_team_members(john_doe)
        self.assertEqual(team_members, expected_team_members)

    def test_tomas_andre_not_team_member_john_doe(self):
        john_doe = Employee(id=1, first_name="John", last_name="Doe", base_salary=3000,
                            birth_date=date(1970, 1, 31), hire_date=date(1990, 10, 1))
        tomas_andre = Employee(id=5, first_name="Tomas", last_name="Andre", base_salary=1600,
                               birth_date=date(1995, 1, 1), hire_date=date(2015, 1, 1))
        team_members = self.rm.get_team_members(john_doe)
        self.assertNotIn(tomas_andre.id, team_members)

    def test_gretchen_watford_salary(self):
        gretchen_watford = Employee(id=4, first_name="Gretchen", last_name="Watford", base_salary=4000,
                                    birth_date=date(1960, 1, 1), hire_date=date(1990, 1, 1))
        expected_salary = 4000
        self.assertEqual(gretchen_watford.base_salary, expected_salary)

    def test_tomas_andre_not_team_leader(self):
        tomas_andre = Employee(id=5, first_name="Tomas", last_name="Andre", base_salary=1600,
                               birth_date=date(1995, 1, 1), hire_date=date(2015, 1, 1))
        is_leader = self.rm.is_leader(tomas_andre)

        self.assertFalse(is_leader)

        team_members = self.rm.get_team_members(tomas_andre)

        self.assertEqual(team_members, None)

    def test_jude_overcash_not_in_database(self):
        jude_overcash = Employee(id=7, first_name="Jude", last_name="Overcash", base_salary=2500,
                                birth_date=date(1985, 1, 1), hire_date=date(2010, 1, 1))
        all_employees = self.rm.get_all_employees()
        self.assertNotIn(jude_overcash, all_employees)


class TestEmployeeManager(unittest.TestCase):

    def setUp(self):
        self.rm = RelationsManager()
        self.em = EmployeeManager(self.rm)

    def test_non_leader_salary(self):
        employee = Employee(id=8, first_name="Non", last_name="Leader", base_salary=1000,
                            birth_date=date(1980, 1, 1), hire_date=date(1998, 10, 10))
        expected_salary = 3000
        self.assertNotEqual(self.em.calculate_salary(employee), expected_salary)

    def test_team_leader_salary(self):
        team_leader = Employee(id=9, first_name="Team", last_name="Leader", base_salary=2000,
                               birth_date=date(1980, 1, 1), hire_date=date(2008, 10, 10))
        self.rm.teams[9] = [10, 11, 12]  
        expected_salary = 3600  
        self.assertEqual(self.em.calculate_salary(team_leader), expected_salary)

     
    def test_salary_calculation_and_email_notification(self):
        employee = Employee(id=1, first_name="John", last_name="Doe", base_salary=3000,
                            birth_date=date(1970, 1, 31), hire_date=date(1990, 10, 1))

        expected_message = f"{employee.first_name} {employee.last_name} your salary: {self.em.calculate_salary(employee)} has been transferred to you."
        self.assertEqual(self.em.calculate_salary_and_send_email(employee), expected_message)

if __name__ == '__main__':
    unittest.main()
