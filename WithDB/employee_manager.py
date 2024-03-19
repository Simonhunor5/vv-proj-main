import datetime
from database import Employees  # Ensure you're importing the correct class
from relations_manager import RelationsManager

class EmployeeManager:
    yearly_bonus = 100
    leader_bonus_per_member = 200

    def __init__(self, relations_manager: RelationsManager):
        self.relations_manager = relations_manager

    def calculate_salary(self, employee: Employees) -> int:
        # Access the correct attribute names, according to your SQLAlchemy Employees model
        salary = employee.baseSalary

        # Calculate years at company using the correct attribute names
        years_at_company = datetime.date.today().year - employee.hireDate.year

        salary += years_at_company * EmployeeManager.yearly_bonus

        # Check if the employee is a leader using the corrected RelationsManager method
        if self.relations_manager.is_leader(employee):
            # Get the list of team member IDs and calculate the leader bonus
            team_members_count = len(self.relations_manager.get_team_members(employee))
            salary += team_members_count * EmployeeManager.leader_bonus_per_member

        return salary

    def calculate_salary_and_send_email(self, employee: Employees) -> str:
        salary = self.calculate_salary(employee)
        # Formulate the message using the correct attribute names
        message = f"{employee.firstName} {employee.lastName}, your salary: {salary} has been transferred to you."
        # In a real scenario, you would integrate with an email service to send this message
        return message

# The __main__ block here would be used for manual testing, which you're now handling with unittest
# So you can comment it out or remove it.
# if __name__ == '__main__':
#     ...
