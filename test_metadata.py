'''
    created by Askao
'''
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