import psycopg2

conn = psycopg2.connect(
        dbname='mydatabase',
        user='mydb',
        password='zxcvb',
        host='localhost'
    )

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS BOOKS(
        id SERIAL PRIMARY KEY,
        name CHAR(25),
        author CHAR(25),
        price FLOAT,
        count INT
    );
""")


def get_all_book():
    cur.execute("SELECT  id,name,author,price,count FROM BOOKS")
    row = cur.fetchall()
    return row

def craete_book(value):
    cur.execute("INSERT INTO BOOKS(name,author,price,count) VALUES  (%s,%s,%s,%s) ",value)
    conn.commit()

def edit_book(value):
    cur.execute("UPDATE BOOKS SET name=%s,author=%s,price=%s.count=%s WHERE id=%s",value)
    conn.commit()

def remove_book(id):
    cur.execute("DELETE FROM BOOKS WHERE id=%s",id)

def search_book(book_dict):
    book_dict = {x:"%"+y+"%" for x,y in book_dict.items() if bool(y)}
    if not bool(book_dict):
        return get_all_book()
    sql = "".join(key+" like %s AND " for key in book_dict.keys())
    print(sql)
    sql = "SELECT name,author,price,count,id FROM BOOKS WHERE " + sql[:-4]
    cur.execute(sql,tuple(book_dict.values()))
    row = cur.fetchall()
    return row


