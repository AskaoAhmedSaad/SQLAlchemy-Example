# SQLAlchemy-Example

**Engine API**<br>
-create connections to the database<br>
-send SQL statements<br>
-retrieve results<br>
see test_engine.py:-

    from sqlalchemy.engine import create_engine

    #create connections to the database
    engine = create_engine('mysql://user:pass@host/db')
    #for sqlite
    #engine = create_engine('sqlite:///:memory:', echo=True)
    connection = engine.connect()

    # send SQL statements
    connection.execute(
        """
        CREATE TABLE employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            job_title VARCHAR(255) NOT NULL
        );
        """
    )
    connection.execute(
        """
        INSERT INTO employees (name, job_title) VALUES ("askao", "developer");
        """
    )

    # retrieve results
    result = connection.execute("SELECT name FROM employees")
    # print table rows
    for row in result:
        print "name:", row['name']
    connection.close()

***


**Metadata**<br>
The metadata object holds all the information about the tables, columns, types, foreign keys, indexes, and sequences that make up the database structure.<br>

The metadata object can be used to create the tables in the database. For this bind the metadata to an engine, and call its create_all method.<br>
see test_metadata.py:<br>

    from sqlalchemy import schema, types

    metadata = schema.MetaData()

    project_table = schema.Table('project', metadata,
        schema.Column('id', types.Integer, primary_key=True),
        schema.Column('title', types.Unicode(255), default=u'Untitled project'),
        schema.Column('description', types.Text(), default=u''),
    )
    for t in metadata.sorted_tables:
        print "Table name: ", t.name
        print "t is project_table: ", t is project_table

    for column in project_table.columns:
        print "Column Table type: ", column.type

    from sqlalchemy.engine import create_engine

    engine = create_engine('mysql://user:pass@host/db', echo=True)
    metadata.bind = engine

    metadata.create_all(checkfirst=True)

***

## SQL Expression API

The SQL Expression API allows you to build SQL queries using Python objects and operators


**Selecting**<br>
see sqlexpression_selecting.py:<br>
    
    from test_metadata_and_types import engine, project_table
    from sqlalchemy.sql import select
    from sqlalchemy.sql import and_, or_, not_

    # get connection pool of connections
    connection = engine.connect()
    print '**** select all (with no conditions) *****'
    s = select([project_table])
    result = connection.execute(s)
    for row in result:
        print row

    print '**** select with conditions*****'
    s = select([project_table], and_(project_table.c.id<=5, project_table.c.title.like(u'pro%')))
    s = s.order_by(project_table.c.title.desc(), project_table.c.id)
    result = connection.execute(s)
    # print result
    print result.fetchall()

    connection.close()

**Updating**<br>
see sqlexpression_updating.py:<br>

    from test_metadata_and_types import engine, project_table
    from sqlalchemy import update

    # get connection pool of connections
    connection = engine.connect()

    u = update(project_table, project_table.c.title==u'project 1')
    connection.execute(u, title=u"project_1")

    connection.close()

**Deleting**<br>
see sqlexpression_deleting.py:<br>

    from test_metadata_and_types import engine, project_table
    from sqlalchemy import delete

    # get connection pool of connections
    connection = engine.connect()

    d = delete(project_table, project_table.c.id==1)
    connection.execute(d)

    connection.close()

***

### Object-Relational API<br>
The API allows to work directly with Python objects without needing to think too much about the SQL that would normally be required to work with them.<br>

see model.py :<br>

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
        # one to one relationship
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

**Create the Session**<br>
see test_session.py:<br>

    import model
    from sqlalchemy import orm
    from sqlalchemy import create_engine

    # Create an engine and create all the tables we need
    engine = create_engine('mysql://user:pass@host/db')
    model.metadata.bind = engine
    model.metadata.create_all()

    # Set up the session
    sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
        expire_on_commit=True)
    session = orm.scoped_session(sm)

The sessionmaker function returns an object for building the particular session you want.<br>
Let’s now look at the arguments being passed to sessionmaker:

  -bind=engine: this binds the session to the engine, the session will automatically create the connections it needs.<br>
  -autoflush=True: if you commit your changes to the database before they have been flushed, this option tells SQLAlchemy to flush them before the commit is gone.<br>
  -autocommit=False: this tells SQLAlchemy to wrap all changes between commits in a transaction. If autocommit=True is specified, SQLAlchemy automatically commits any changes after each flush; this is undesired in most cases.<br>
  -expire_on_commit=True: this means that all instances attached to the session will be fully expired after each commit so that all attribute/object access subsequent to a completed transaction will load from the most recent database state.<br><br>

The scoped_session() object ensures that a different session is used for each thread so that every request can have its own access to the database.<br>

**Use the Session**<br>
see use_session file:<br>

    - open the console on the same path of all files and wite this commands

    ********** Insert **********

    >>> from test_session import session


    >>> import model

    >>> project = model.Project()
    >>> project.title = u'project 3'
    >>> project.description = u'project 3 description'
    
    >>> session.add(project)
    >>> print project.id

    >>> session.flush()
    >>> print project.id

    >>> session.commit()

    *************** delete ************************
    >>> session.delete(project)
    >>> session.flush()

    you can rollback this:

    >>> session.rollback()

    ************* Query ****************************

    Queries are performed with query objects that<br>
    are created from the session.<br>
    The simplest way to create and use a query object is like this:<br>

    >>> project_q = session.query(model.Project)
    >>> for project in project_q:
    ...     print project.title


    >>> project_q.all()

    >>> project = project_q.first()
    >>> project.title

    >>> project_q[0:2]

    >>> project_q.get(1)

    *********** Working with relationships *****************

    >>> task = model.Task()
    >>> task.title= u'task 1'
    >>> task.description = u'task 1 description'
    >>> project.tasks.append(task)
    >>> session.commit()


    >>> employee = model.Employee()
    >>> employee.name= u'samir'
    >>> employee.job_title= u'developer'
    >>> task.employees.append(employee)
    >>> session.commit()





