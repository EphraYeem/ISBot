import sqlite3

con = sqlite3.connect('IS.db')

institutions_create_table ="CREATE TABLE institutions (id INTEGER PRIMARY KEY, name TEXT, matching_emoji TEXT)"

departments_create_table ="""CREATE TABLE departments (id INTEGER PRIMARY KEY, name TEXT, matching_emoji TEXT)"""

departments_in_institutions_create_table="""CREATE TABLE departments_in_institutions (id INTEGER PRIMARY KEY, name TEXT, institution_id INTEGER, department_id INTEGER, FOREIGN KEY(institution_id) REFERENCES institutions(id), FOREIGN KEY(department_id) REFERENCES departments(id))"""

con.row_factory = sqlite3.Row # So we can select the results like a dict
# print(con.execute("select * from institutions").fetchone()['matching_emoji'].encode())
#con.execute("delete from institutions where matching_emoji='<:yee:>'")
#con.commit()
# print(query_results := con.execute(f"select department_id from departments_in_institutions where id = 2"))
role_id_list = []
dbcon = sqlite3.connect('IS.db')
dbcon.row_factory = sqlite3.Row  # So we can select the results like a dict
role_id_list.extend(dbcon.execute("SELECT id FROM institutions").fetchall())
role_id_list.extend(dbcon.execute("SELECT id FROM departments").fetchall())
role_id_list.extend(dbcon.execute("SELECT id FROM departments_in_institutions").fetchall())
print(role_id_list)
for r in role_id_list:
    print(r['id'])
