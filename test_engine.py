'''
    created by Askao
'''
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
