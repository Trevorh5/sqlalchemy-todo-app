import psycopg2

connection = psycopg2.connect('dbname=testdb user=postgres password=54321')

# Open a cursor to perform database operations
cursor = connection.cursor()

# Delete the table if it exists
cursor.execute('DROP TABLE IF EXISTS table2;')

# Run multi-line commands with triple quote (''' command here ''')
cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT FALSE
  );
''')

# Use %s to do string interpolation
cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

# Just a fancier way to do the above method
SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (3, True))

cursor.execute('SELECT * from table2')

# fetchall, fetchmany, and fetchone will pull results from the previous execute method (select * from table2)
result = cursor.fetchall()
print('fetchall', result)

# Won't recieve anything because the previous "fetchall" already took those results
result2 = cursor.fetchone()
print('fetchone', result2)

cursor.execute('SELECT * from table2')

# Now this one will work since there is a new execute above 
result3 = cursor.fetchone()
print('fetchone', result3)

# commit, so it does the executions on the db and persists in the db
connection.commit()

# close cursor and connection to show this is all that needs to be done (Must do manually)
cursor.close()
connection.close()

