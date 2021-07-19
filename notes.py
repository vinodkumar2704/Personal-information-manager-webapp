import requests
import bs4
import sys
import psycopg2



def create_db():
    dbconn = psycopg2.connect("dbname = pim")
    cursor = dbconn.cursor()
    with open("pim.sql") as f:
        sql_code = f.read()
    cursor.execute(sql_code)
    dbconn.commit()


create_db()

