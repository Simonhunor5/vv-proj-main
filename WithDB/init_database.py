from sqlalchemy.orm import Session
from database import DB, Employees, Teams
from relations_manager import RelationsManager

def main():
    db = DB()
    db.connect_database()
    db.init_database()

    with Session(db.engine) as session:
        manager = RelationsManager(session)


        employee_data_list = session.query(Employees).all()

        for employee_data in employee_data_list:

            is_leader = manager.is_leader(employee_data)
            team_members = manager.get_team_members(employee_data) if is_leader else []

            new_employee = Employees(
                employeeId=employee_data.employeeId,
                firstName=employee_data.firstName,
                lastName=employee_data.lastName,
                birthDate=employee_data.birthDate,
                baseSalary=employee_data.baseSalary,
                hireDate=employee_data.hireDate,
            )
            session.add(new_employee)
            
            if is_leader:
                team = Teams(leaderId=employee_data.employeeId, members=team_members)
                session.add(team)

        session.commit()

if __name__ == "__main__":
    main()
