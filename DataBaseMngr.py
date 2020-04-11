import sqlite3
import time

# methods: create database, add to database, delete from database, retrieve all data and input into list
dbcon = sqlite3.connect('SCMdb.db')


def createDB():
    # try to create the database unless it already exists
    try:
        dbcon.execute("CREATE TABLE SCM(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Name TEXT NOT NULL, Price TEXT "
                      "NOT NULL, Quantity TEXT NOT NULL);")

        dbcon.commit()
        print("Database has been created")

    except sqlite3.OperationalError:
        print("Database loaded")


def addDB(name, price, quantity):
    # add a new row to the database
    dbcon.execute("INSERT INTO SCM (Name, price, quantity) VALUES ('{}', '{}', '{}')".format(name, price, quantity))
    dbcon.commit()


def delDB(name):
    # delete a specific row from the database
    dbcon.execute("DELETE FROM SCM WHERE Name='{}'".format(name))
    dbcon.commit()


def retrieveDB():
    # retrieve the entire current contents
    try:
        theCursor = dbcon.cursor()
        cursor_results = theCursor.execute("SELECT * FROM SCM")

        item_list = cursor_results.fetchall()
        return item_list

    except sqlite3.OperationalError:
        print("Operational Error")

def clearDB():
    print("Cleaning out database: ")
    id_num = 0
    while id_num < 10000:
        dbcon.execute("DELETE FROM SCM WHERE ID='{}'".format(id_num))
        dbcon.commit()

        id_num = id_num + 1
        if (id_num % 1000) == 0:

            time.sleep(.25)
            print("...")

def searchNames(keyword):
    # search for entries containing string keyword, by appending '%'
    keyword = "%" + keyword + "%"

    try:
        theCursor = dbcon.cursor()
        cursor_results = theCursor.execute("SELECT * FROM SCM WHERE Name LIKE '{}'".format(keyword))

        item_list = cursor_results.fetchall()
        return item_list

    except sqlite3.OperationalError:
        print("Operational Error")