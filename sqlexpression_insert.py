from test_metadata import engine, project_table

connection = engine.connect()
ins1 = project_table.insert(
    values=dict(title=u'project 1', description=u'project 1 description')
)

ins2 = project_table.insert(
    values=dict(title=u'project 2', description=u'project 2 description')
)
'''
The ins object automatically generates the correct SQL 
to insert the values specified. It is to be noted that SQLAlchemy handles
 any type conversion of the values specified to insert() using its type system,
  thus removing any chance of SQL injection attacks.
'''
result = connection.execute(ins1)
result = connection.execute(ins2)

connection.close()