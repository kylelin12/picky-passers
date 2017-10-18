import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="secretdb.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

# Populate Code

c.execute("CREATE TABLE courses (code TEXT, mark INTEGER, id INTEGER);")

with open('courses.csv') as csvfilein:
    courses_csv = csv.DictReader(csvfilein)
    for row in courses_csv:
        c.execute("INSERT INTO courses VALUES(\'" + row["code"] + "\', " + row['mark'] + "," + row['id'] + ");")

c.execute("CREATE TABLE peeps (name TEXT, age INTEGER, id INTEGER PRIMARY KEY);")
with open('peeps.csv') as csvfilein:
    peeps_csv = csv.DictReader(csvfilein)
    for row in peeps_csv:
        c.execute("INSERT INTO peeps VALUES(\'" + row["name"] + "\', " + row['age'] + "," + row['id'] + ");")

db.commit() #save changes
db.close() #close database