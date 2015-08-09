from test_metadata import engine, project_table
from sqlalchemy import update

# get connection pool of connections
connection = engine.connect()

u = update(project_table, project_table.c.title==u'project 1')
connection.execute(u, title=u"project_1")

connection.close()