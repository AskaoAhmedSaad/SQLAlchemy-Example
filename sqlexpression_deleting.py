from test_metadata import engine, project_table
from sqlalchemy import delete

# get connection pool of connections
connection = engine.connect()

d = delete(project_table, project_table.c.id==1)
connection.execute(d)

connection.close()