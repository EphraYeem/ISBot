import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = sa.create_engine('sqlite:///IS.db')
Session = sessionmaker(engine)
Base = declarative_base()

class Institution(Base):
    __tablename__ = 'institutions'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    matching_emoji = sa.Column(sa.String)

class Department(Base):
    __tablename__ = 'departments'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    matching_emoji = sa.Column(sa.String)

class DepartmentsInInstitution(Base):
    __tablename__ = 'departments_in_institutions'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    institution_id = sa.Column(sa.Integer, sa.ForeignKey('institutions.id'))
    department_id = sa.Column(sa.Integer, sa.ForeignKey('departments.id'))
    institution = relationship('Institution')
    department = relationship('Department')

Base.metadata.create_all(engine)

def get_institutions():
    with Session.begin() as session:
        return session.query(Institution).all()


def get_departments(institution: str):
    with Session.begin() as session:
        return session.query(DepartmentsInInstitution).join(Institution).join(Department).filter(Institution.name==institution).first().department.name

print(get_departments('a'))
# with Session.begin() as session:
#     session.add(Institution(id=1, name='a', matching_emoji='yee'))
#     session.add(Department(id=2, name='b', matching_emoji='yoo'))
#     session.add(DepartmentsInInstitution(id=3, name='yoya', institution_id=1, department_id=2))
