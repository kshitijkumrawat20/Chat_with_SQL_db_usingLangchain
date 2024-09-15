import sqlite3
# connet to sqlite
connection = sqlite3.connect('student.db')

cursor = connection.cursor()

table = """
create table STUDENT(NAME VARCHAR(20), CLASS VARCHAR(20),MARKS VARCHAR(20))
"""

cursor.execute(table)

# inser data 
cursor.execute("insert into STUDENT values('John','10th','91')")
cursor.execute("insert into STUDENT values('Vishal','10th','55')")
cursor.execute("insert into STUDENT values('Krishna','10th','73')")
cursor.execute("insert into STUDENT values('Amit','10th','69')")
cursor.execute("insert into STUDENT values('Soumya','10th','95')")
cursor.execute("insert into STUDENT values('Priyanka','10th','75')")
cursor.execute("insert into STUDENT values('Lakshya','10th','90')")
cursor.execute("insert into STUDENT values('Sneha','10th','70')")
cursor.execute("insert into STUDENT values('Suraj','10th','89')")

# Display the data 
print("The inserted data is:")
data = cursor.execute("select * from STUDENT")
for row in data:
    print(row)
    
connection.commit()
connection.close()
   
