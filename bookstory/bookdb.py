import sqlite3
from datetime import datetime



sql_craete_book_table = """
    CREATE TABLE IF NOT EXISTS BOOK (
        id integer PRIMARY KEY,
        name CHAR(30),
        author CHAR(30),
        price FLOAT,
        count INT
        
    );
    
 
 """
 

conn = sqlite3.connect("book.db")
cur = conn.cursor()



cur.execute(sql_craete_book_table)

sql2="""
   CREATE TABLE IF NOT EXISTS REPORT (
        id integer PRIMARY KEY,
        idbook integer,
        name CHAR(30),
        author ChAR(30),
        count INT,
        Factor Float,
        time DATETIME DEFAULT CURRENT_TIMESTAMP

    );

"""
cur.execute(sql2)
conn.commit()


def get_all_data():
    sql = "SELECT * FROM BOOK"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def creatbook(value):
    sql = "INSERT  INTO BOOK (name,author,price,count) VALUES (?,?,?,?) "
    cur.execute(sql,tuple(value))
    conn.commit()

def serch_book(b_dict:dict):
    b_dict = {x:"%"+y+"%" for x,y in b_dict.items() if bool(y) }
    sql = "".join(key+" LIKE ? AND " for key in b_dict.keys())[:-4]
    sql = "SELECT * FROM BOOK WHERE " + sql
    cur.execute(sql,tuple(b_dict.values()))
    rows = cur.fetchall()
    return rows

def removebook(id):
    sql = "DELETE FROM BOOK WHERE id =?"
    cur.execute(sql,(id,))
    conn.commit()

def editbook(value):
    sql = "UPDATE BOOK SET name=?,author=?,price=?,count=? WHERE id=?"
    cur.execute(sql,value)
    conn.commit()

def add_row_report(book,value):
    # time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    val = list(book)[:-2] + list(value)
    
    sql = "INSERT  INTO Report (idbook,name,author,count,factor) VALUES (?,?,?,?,?) "
    cur.execute(sql,tuple(val))
    
def show_row_report():
    sql = "SELECT   id,idbook,name,author,count,factor,time FROM  REPORT "
    cur.execute(sql)
    row = cur.fetchall()
    return row

def search_rows_report(start_time,end_time):
    sql = "SELECT id,idbook,name,author,count,factor,time FROM REPORT  WHERE time BETWEEN ? AND ?;"
    cur.execute(sql,(start_time,end_time))
    row = cur.fetchall()
    return row

def sum_rows_report(start_time,end_time):
    sql = "SELECT SUM(factor) FROM REPORT  WHERE time BETWEEN ? AND ?;"
    cur.execute(sql,(start_time,end_time))
    row = cur.fetchall()
    return row