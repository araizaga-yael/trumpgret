import sqlite3
con = sqlite3.connect('trumpgret.db')
cursor = con.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS tweets
             (id integer primary key, date text)''')