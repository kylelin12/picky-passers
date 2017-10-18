import sqlite3
import csv

f = ('secretdb.db')

db = sqlite3.connect(f)
c = db.cursor()

# Returns the name and the grade associated with the name
# in the format: "Name: Grade"
def entries(name):
    s = ""
    entries = lookup(name)
    for entry in entries:
        s += str(entry[1]) + ": " + str(entry[2]) + " | "
    return s

# Prints all data associated with the tuple passed to it
def print_data(entries):
    for entry in entries:
        s = ""
        for data in entry:
            s += str(data) + " | "
        print s

# Returns the name, grades, and classes of the name passed to it.
def lookup(name):
    c.execute("SELECT name, code, mark FROM peeps, courses WHERE courses.id = peeps.id AND '%s' = name;"%(name))
    result = c.fetchall()
    return result

# Computes and returns the average of the name passed to it.
def average(name):
    total = 0
    entries = lookup(name)
    for entry in entries:
        total += int(entry[2])
    return total/len(entries)

# Creates a table in the database to store averages
def create_average_table():
    c.execute("CREATE TABLE peeps_avg (id INTEGER PRIMARY KEY, name TEXT, average INTEGER NOT NULL);")
    c.execute("SELECT name, id FROM peeps;")
    entries = c.fetchall()
    # Inserts the averages from everybody in peeps into the averages table
    #  in the format: <ID of Person>, <Name of Person>, <Average of Person>
    for entry in entries:
        c.execute("INSERT INTO peeps_avg VALUES(%s, '%s', %s)"%(entry[1], entry[0], average(entry[0])))
    print "Averages table created"

# Returns a tuple containing all the averages found in the averages table
def get_averages():
    c.execute("SELECT * FROM peeps_avg;")
    averages = c.fetchall()
    return averages

# After changes are made to the courses (contains grades) database,
# Updates the averages table with re-calculated averages.
def update_averages():
    entries = get_averages()
    for entry in entries:
        c.execute("UPDATE peeps_avg SET average = %d WHERE name = '%s';"%(average(entry[1]), entry[1]))

print "Testing printing grades: Kruder"
print_data(lookup("kruder"))
print "Testing printing average: Kruder"
print_data(lookup("kruder"))

print "Testing printing grades: Tiesto"
print_data(lookup("tiesto"))
print "Testing printing average: Tiesto"
print_data(lookup("tiedo"))

create_average_table()

print "Testing average table print"
print "ID | NAME | AVERAGE"
print_data(get_averages())

print "Adding random values to test update_averages()"
c.execute("INSERT INTO courses VALUES ('ceramics', 99, 3);")
c.execute("INSERT INTO courses VALUES ('apcs', 65, 6);")
c.execute("INSERT INTO courses VALUES ('webdev', 99, 9);")

update_averages()
print "Averages updated for Sasha, Bassnectar, and tINI"
print "ID | NAME | AVERAGE"
print_data(get_averages())

# db.commit() is intentionally ommited to avoid making changes to the database file,
# allowing functions from this program to be run again and again in different orders
# while keeping the same source file.
db.close()