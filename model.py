'''
    created by Askao
'''
from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types

# define the structure **********************
metadata = schema.MetaData()

def now():
    return datetime.datetime.now()

project_table = schema.Table('project', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('project_seq_id', optional=True), primary_key=True),
    schema.Column('title', types.Unicode(255), default=u'project'),
    schema.Column('description', types.Text(), nullable=False),
)
task_table = schema.Table('task', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('task_seq_id', optional=True), primary_key=True),
    # one to many relationship
    schema.Column('projectid', types.Integer,
        schema.ForeignKey('project.id'), nullable=False),
    schema.Column('title', types.Unicode(255), default=u''),
    schema.Column('description', types.Text(255), nullable=False),
    schema.Column('created', types.TIMESTAMP(), default=now()),
)

# junction table
taskemployee_table = schema.Table('taskemployee', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('taskemployee_seq_id', optional=True), primary_key=True),
    schema.Column('taskid', types.Integer, schema.ForeignKey('task.id')),
    schema.Column('employeeid', types.Integer, schema.ForeignKey('employee.id')),
)
employee_table = schema.Table('employee', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('employee_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(255), nullable=False, unique=True),
    schema.Column('job_title', types.Unicode(255), nullable=False, unique=True),
)
# ***********************************

# define classes and mappers
class Project(object):
    pass

class Task(object):
    pass

class Employee(object):
    pass

orm.mapper(Project, project_table, properties={
    'tasks':orm.relation(Task, backref='project')
})
orm.mapper(Task, task_table, properties={
    'employees':orm.relation(Employee, secondary=taskemployee_table)
})
orm.mapper(Employee, employee_table)

# ***********************************