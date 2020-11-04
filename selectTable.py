
import sqlite3
conn = sqlite3.connect('table.db')
cur = conn.cursor()
print("Opened database successfully")
def select_table(condition=None,label="好瓜",sql=None,distict = False):
    if sql:
        cur.execute(sql)
        return cur.fetchmany()
    sql = "select "
    if distict:
        sql = sql + " DISTINCT "
    sql = sql + label+" from test"

    if condition:
        sql = sql + " " +condition

    cur.execute(sql)
    #print(cur.fetchmany())
    return cur.fetchall()