import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = sa.create_engine('sqlite:///IS.db')
Session = sessionmaker(engine, expire_on_commit=False)
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
        return session.query(DepartmentsInInstitution.id.label('id'), 
                             Department.name.label('name'), 
                             Department.matching_emoji.label('matching_emoji')).\
                       select_from(DepartmentsInInstitution).\
                       join(Institution).\
                       join(Department).\
                       filter(Institution.name==institution).all()


def get_department_from_dii(department_in_institution_id: id):
    with Session.begin() as session:
        return session.query(DepartmentsInInstitution).\
                filter(DepartmentsInInstitution.id==department_in_institution_id).\
                one_or_none()
    # dbcon.execute(f"select department_id from departments_in_institutions where id = {interaction.custom_id}").fetchone()


#TODO: chnage to just insert the role itself and an emoji?
def insert_institution(id: int, name: str, matching_emoji: str):
    with Session.begin() as session:
        session.add(Institution(id=id, name=name, matching_emoji=matching_emoji))


def insert_department(id: int, name: str, matching_emoji: str):
    with Session.begin() as session:
        session.add(Department(id=id, name=name, matching_emoji=matching_emoji))


def insert_department_in_institution(id: int, name: str, institution_id: int, department_id: int):
    with Session.begin() as session:
        session.add(DepartmentsInInstitution(id=id, name=name, institution_id=institution_id, department_id=department_id))


# with Session.begin() as session:
#     session.add(Institution(id=1, name='a', matching_emoji=':yee:366667220312522763'))
#     session.add(Department(id=2, name='b', matching_emoji='😂'))
#     session.add(DepartmentsInInstitution(id=3, name='yoya', institution_id=1, department_id=2))
