from test_metadata import engine, project_table
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