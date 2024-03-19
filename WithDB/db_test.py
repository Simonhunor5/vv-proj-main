import unittest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Employees, Teams
from relations_manager import RelationsManager
from employee_manager import EmployeeManager


class TestEmployeeRelationsManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///WithDB/employees.db')
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.rm = RelationsManager(self.session)

    def test_team_leader_john_doe(self):
        john_doe = self.session.query(Employees).filter_by(firstName="John", lastName="Doe").first()
        self.assertIsNotNone(john_doe, "John Doe does not exist in the database")
        self.assertTrue(self.rm.is_leader(john_doe), "John Doe is not marked as a leader but should be")

    def test_team_members_john_doe(self):
        john_doe = self.session.query(Employees).filter_by(firstName="John", lastName="Doe").first()
        expected_team_members = self.rm.get_team_members(john_doe)
        self.assertIsNotNone(expected_team_members, "John Doe should have team members")
        # Use the IDs directly since get_team_members returns a list of IDs
        self.assertCountEqual(expected_team_members, [2, 3])

    def test_tomas_andre_not_team_member_john_doe(self):
        john_doe = self.session.query(Employees).filter_by(firstName="John", lastName="Doe").first()
        tomas_andre = self.session.query(Employees).filter_by(firstName="Tomas", lastName="Andre").first()
        team_member_ids = self.rm.get_team_members(john_doe)  # Expecting list of IDs
        self.assertNotIn(tomas_andre.employeeId, team_member_ids)

    def test_gretchen_watford_salary(self):
        gretchen_watford = self.session.query(Employees).filter_by(firstName="Gretchen", lastName="Watford").first()
        self.assertIsNotNone(gretchen_watford, "Gretchen Watford does not exist in the database")
        self.assertEqual(gretchen_watford.baseSalary, 4000, "Gretchen Watford's salary does not match the expected")

    def test_tomas_andre_not_team_leader(self):
        tomas_andre = self.session.query(Employees).filter_by(firstName="Tomas", lastName="Andre").first()
        self.assertIsNotNone(tomas_andre, "Tomas Andre does not exist in the database")
        self.assertFalse(self.rm.is_leader(tomas_andre), "Tomas Andre is incorrectly marked as a leader")


class TestEmployeeManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///WithDB/employees.db')
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def setUp(self):
        self.rm = RelationsManager(self.session)
        self.em = EmployeeManager(self.rm)

    def test_non_leader_salary(self):
        # Query an employee that exists in your database or ensure the database has a "Non Leader"
        # Example for an existing employee
        employee = self.session.query(Employees).filter_by(firstName="Tomas", lastName="Andre").first()
        self.assertIsNotNone(employee, "Employee does not exist in the database")
        calculated_salary = self.em.calculate_salary(employee)
        # Use the correct expected salary as per your business logic
        expected_salary = 3000  # Replace with the correct expected value
        self.assertNotEqual(calculated_salary, expected_salary)

    def test_team_leader_salary(self):
        # Query an employee that exists in your database or ensure the database has a "Team Leader"
        # Example for an existing employee
        team_leader = self.session.query(Employees).filter_by(firstName="Gretchen", lastName="Watford").first()
        self.assertIsNotNone(team_leader, "Team Leader does not exist in the database")
        calculated_salary = self.em.calculate_salary(team_leader)
        expected_salary = 7800  # Replace with the correct expected value
        self.assertEqual(calculated_salary, expected_salary)

    def test_salary_calculation_and_email_notification(self):
        employee = self.session.query(Employees).filter_by(firstName="John", lastName="Doe").first()
        self.assertIsNotNone(employee, "Employee John Doe does not exist in the database")
        expected_message = f"{employee.firstName} {employee.lastName}, your salary: {self.em.calculate_salary(employee)} has been transferred to you."
        actual_message = self.em.calculate_salary_and_send_email(employee)
        self.assertEqual(actual_message, expected_message)

if __name__ == '__main__':
    unittest.main()
