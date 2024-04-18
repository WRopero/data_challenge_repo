from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import List

Base = declarative_base()

class ColumnDepartmentModel(Base):
    __tablename__ = 'departments'

    id = Column(Integer(), primary_key=True)
    department = Column(String(255), nullable=False)
    created_on = Column(DateTime(), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = Column(DateTime(), nullable=True, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))

    employees = relationship("ColumnEmployeesModel", back_populates="department")


class ColumnJobsModel(Base):
    __tablename__ = 'jobs'

    id = Column(Integer(),  primary_key=True)
    job = Column(String(255), nullable=False)
    created_on = Column(DateTime(), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = Column(DateTime(), nullable=True, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))

    employees = relationship("ColumnEmployeesModel", back_populates="job")

class ColumnEmployeesModel(Base):
    __tablename__ = 'hired_employees'

    id = Column(Integer(),  primary_key=True)
    name = Column(String(255), nullable=False)
    datetime = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    created_on = Column(DateTime(), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_on = Column(DateTime(), nullable=True, server_default=text("NULL ON UPDATE CURRENT_TIMESTAMP"))

    department = relationship("ColumnDepartmentModel", back_populates="hired_employees")
    job = relationship("ColumnJobsModel", back_populates="hired_employees")




MODELS_LIST : List = [ColumnEmployeesModel, ColumnDepartmentModel, ColumnJobsModel]