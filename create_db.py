from sqlite3 import *


conn = connect('Food_storage.db')
c = conn.cursor()

q = '''
CREATE TABLE Foodstufs(
Name TEXT PRIMARY KEY,
Category TEXT NOT NULL,
Quantity INTEGER NOT NULL,
Location TEXT NOT NULL
)
'''


c.execute(q)
conn.commit()
conn.close()


