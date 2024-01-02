import mysql.connector


conn = mysql.connector.connect(
  host="localhost",
  user="mydb",
  password="zxcvb",
  database="mydatabase"
  )
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS BOOKS(
                id integer PRIMARY KEY AUTO_INCREMENT,
                name CHAR(20),
                author CHAR(20),
                price FLOAT,
                count INT
            );
""")


def get_all_book():
    cur.execute("SELECT name,author,price,count,id FROM BOOKS")
    row = cur.fetchall()
  
    return row

def craete_book(value):
    
    print(value)
    print("\n\n\nsclasacasc")
    cur.execute("INSERT  INTO BOOKS (name,author,price,count) VALUES (%s,%s,%s,%s) ",tuple(value))
    conn.commit()

def edit_book(value):
    cur.excute("UPDATE BOOKS SET name=%s,author=%s,price=%s,count=%s where id%s",tuple(value))
    conn.commit()

def remove_book(id):
    cur.execute("DELETE FROM BOOKS WHERE id=%s",(id,))
    conn.commit()

def search_book(book_dict):
    book_dict = {x:y for x,y in book_dict.items() if bool(y)}
    if not bool(book_dict):
        return get_all_book()
    sql = "".join(key+" like %s AND " for key in book_dict.keys())
    sql = "SELECT name,author,price,count,id FROM BOOKS WHERE " + sql[:-4]
    print(sql)
    cur.execute(sql,tuple(book_dict.values()))
    row = cur.fetchall()
    return row


