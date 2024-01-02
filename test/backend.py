import sqlite3
from sqlite3 import Error
from typing import Tuple


try:
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    sql_creat_book_table = """
        CREATE TABLE IF NOT EXISTS BOOKS ( 
            id integer PRIMARY KEY ,
            name CHAR(25) NOT NULL,
            author CHAR(25) NOT NULL,
            price FLOAT NOT NULL,
            inventory integer  default 0,
            UNIQUE(name,author)            
        );
        """
    sql_creat_order_table = """
        CREATE TABLE IF NOT EXISTS ORDERS (
            id integer PRIMERY KEY ,
            book_id integer NOT NULL,
            quantity integer,
            price FLOAT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES BOOKS(id) 
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )
    """
    cur.execute(sql_creat_book_table)
    cur.execute(sql_creat_order_table)

    conn.commit()
except Error as e:
    print("error", e)


def creat_book(value: tuple) -> bool:
    try:
        sql = "INSERT INTO BOOKS(name,author,price,inventory) VALUES (?,?,?,?)"
        cur.execute(sql, value)
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def remove_book(id: int):
    sql = "DELETE FROM BOOKS WHERE id =?"
    cur.execute(sql, (id,))
    conn.commit()


def edit_book(value: tuple, id: int) -> bool:
    try:
        sql = "UPDATE BOOKS SET name=?,author=?,price=?,inventory=? WHERE id=?"
        query_items = value + (id,)
        cur.execute(sql, query_items)
        conn.commit()
        return True
    except Error as e:
        print(e)
        return False


def search_book(book_dic: dict) -> Tuple[bool, list]:
    try:
        book_dic = {x: y for x, y in book_dic.items() if bool(y)}
        if book_dic:
            
            query_for_search = "".join(key + "=? AND " for key in book_dic.keys())[:-4]
            query_for_search = (
                """ SELECT id,name,author,price,inventory FROM BOOKS WHERE  """
                + query_for_search
            )
            cur.execute(query_for_search,tuple(book_dic.values()))
            rows = cur.fetchall()
            return (True, rows)
        else:
            return (True, [])
    except Error as e:
        print("db error", e)
        return (False, [])


def get_all_book() -> Tuple[bool, list]:
    try:
        query_book = """SELECT id,name,author,price,inventory FROM BOOKS"""
        cur.execute(query_book)
        rows = cur.fetchall()
        print(rows)
        return (True, rows)
    except Error as e:
        print(e)
        return (False, [])


def add_order(book_id: int, quantity: int) -> Tuple[bool, str]:
    query = "SELECT inventory,price FROM BOOKS WHERE id=?"
    book = cur.execute(query, (book_id,)).fetchone()
    try:
        if quantity < book[0]:
            query = "INSERT INTO ORDERS(book_id,quantity,price) VALUES (?,?,?)  "
            cur.execute(query, (book_id,quantity, book[1] * quantity))
            cur.execute("UPDATE BOOKS SET inventory=? WHERE Id=?",(book[0]-quantity,book_id))
            conn.commit()
            return (True, "add successfuly")
        else:
            return (False, "insuffiCint inventory")
    except Error as e:
        print(e)
        return (False, "have a problme not adds")


def show_order():
    query = "SELECT ORDERS.id,name,quantity,(ORDERS.price*quantity) as prices FROM ORDERS join BOOKS on ORDERS.book_id=BOOKS.id  "
    cur.execute(query)
    row = cur.fetchall()
    return row


def sum_order():
    query = "SELECT SUM(quantity),SUM(price) FROM ORDERS"
    cur.execute(query)
    row = cur.fetchone()
    return row
