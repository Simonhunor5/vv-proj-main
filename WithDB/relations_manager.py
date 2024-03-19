# relations_manager.py

from database import Employees, Teams

class RelationsManager:
    def __init__(self, session):
        self.session = session

    def is_leader(self, employee: Employees) -> bool:
        # Query the database to check if an employee is a leader
        return self.session.query(Teams).filter(Teams.leaderId == employee.employeeId).count() > 0

    def get_team_members(self, employee: Employees) -> list:
        # Query the database to get team members if an employee is a leader
        if self.is_leader(employee):
            team = self.session.query(Teams).filter(Teams.leaderId == employee.employeeId).first()
            return [member.employeeId for member in team.members] if team else []
        return []
