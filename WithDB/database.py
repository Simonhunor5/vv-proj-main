from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
Base = declarative_base()

class Employees(Base):
    __tablename__ = "employees"

    employeeId = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    birthDate = Column(Date)
    baseSalary = Column(Integer)
    hireDate = Column(Date)
    team_id = Column(Integer, ForeignKey("teams.teamId"), nullable=True)
    team = relationship("Teams", back_populates="members")

class Teams(Base):
    __tablename__ = "teams"

    teamId = Column(Integer, primary_key=True)
    leaderId = Column(Integer)
    members = relationship("Employees", back_populates="team", cascade="all, delete-orphan")

class DB:
    __instance = None

    def __init__(self):
        if DB.__instance is not None:
            raise Exception("This class is Singleton!")
        else:
            DB.__instance = self

        self.engine = None
        self.connection = None
        self.metadata = None
        self.DB_NAME = "employees.db"

    def get_instance(self):
        return self.__instance

    def connect_database(self):
        self.engine = create_engine(f"sqlite:///{self.DB_NAME}", echo=True)
        self.metadata = Base.metadata
        self.metadata.bind = self.engine
        self.connection = self.engine.connect()

    def init_database(self):
        Base.metadata.create_all(self.engine)
