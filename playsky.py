import sqlite3

con = sqlite3.connect('IS.db')

institutions_create_table ="CREATE TABLE institutions (id INTEGER PRIMARY KEY, name TEXT, matching_emoji TEXT)"

departments_create_table ="""CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT, matching_emoji TEXT)"""

departments_in_institutions_create_table="""CREATE TABLE departments_in_institutions (id INTEGER PRIMARY KEY, name TEXT, institution_id INTEGER, department_id INTEGER, FOREIGN KEY(institution_id) REFERENCES institutions(id), FOREIGN KEY(department_id) REFERENCES departments(id))"""

print("select id from departments where name = 'math'")
print(con.execute("select id from departments where name = 'math'").fetchone()[0])