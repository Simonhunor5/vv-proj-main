import datetime
from sqlalchemy.orm import Session
from database import DB, Employees, Teams
from relations_manager import RelationsManager

def main():
    db = DB()
    db.connect_database()
    db.init_database()

    with Session(db.engine) as session:
        manager = RelationsManager()

        for employee_data in manager.employee_list:
            employee = Employees(
                employeeId=employee_data.id,
                firstName=employee_data.first_name,
                lastName=employee_data.last_name,
                birthDate=employee_data.birth_date,
                baseSalary=employee_data.base_salary,
                hireDate=employee_data.hire_date,
            )
            session.add(employee)

        for team_id, member_ids in manager.teams.items():
            team = Teams(leaderId=team_id, members=[])
            for member_id in member_ids:
                employee = session.query(Employees).get(member_id)
                team.members.append(employee)

            session.add(team)

        session.commit()

if __name__ == "__main__":
    main()
