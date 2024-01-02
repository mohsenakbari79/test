import tkinter as tk

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askinteger


from backend import (
    creat_book,
    edit_book,
    search_book,
    get_all_book,
    add_order,
    show_order,
    sum_order,
    remove_book,
)


class App(tk.Tk):
    def __init__(self, title, default_size):
        super().__init__()
        self.title(title)
        self.minsize(width=default_size[0], height=default_size[1])
        self.geometry(f"{default_size[0]}x{default_size[1]}")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=3, uniform="a")
        self.columnconfigure(0, weight=1)
        self.create_menu()
        self.book = Book(self)
        Main(self)
        
        self.mainloop()
    
    def create_menu(self):
        self.menu = tk.Menu(self)
        self.menu.add_command(label="Orders", command=self.order)
        self.menu.add_command(label="Repor", command=self.report)
        self.config(menu=self.menu)
        
    def order(self):
        Order(self)
    
    def report(self):
        Report(self)
        


class Order(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.table = TableModel(self, columns=("id", "book_name", "quantity","price"), row=1, column=0)
        self.frame = tk.Frame(self)
        tk.Label(
            self.frame,
            text="برای اضافه کردن یک سفارش در صفحه home  دوبار روی کتاب مورد نظر کلید کرده و مقدار سفارش را وارد کنید ",
        ).pack(fill="y",expand=True)
        self.frame.grid(row=0, column=0)
        self.columnconfigure(0, weight=1)
        menu = tk.Menu(master)
        menu.add_command(label="Home", command=self.remove_fame)
        master.config(menu=menu)
        self.show_all()
        self.grid(row=0, column=0, rowspan=2, sticky="news")

    def remove_fame(self):
        self.master.create_menu()
        self.destroy()

    def show_all(self):
        rows = show_order()
        self.table.show_rows(rows)


class Report(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        menu = tk.Menu(master)
        menu.add_command(label="Home", command=self.remove_fame)
        master.config(menu=menu)
        self.grid(row=0, column=0, rowspan=2, sticky="news")
        
    def remove_fame(self):
        self.master.create_menu()
        self.destroy()




class Book(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        # get value
        self.name = GetValue(self, "نام", 0, 0)
        self.author = GetValue(self, "نویسنده", 0, 1)
        self.price = GetValue(self, "قیمت", 1, 0)
        self.count = GetValue(self, "موحودی", 1, 1)

        self.grid(row=0, column=0, sticky="news")

    def get_value(self):
        try:
            value = {
                "name": self.name.value.get(),
                "author": self.author.value.get(),
                "price": self.price.value.get(),
                "count": self.count.value.get(),
            }
            return (True, value)

        except Exception as e:
            showerror(
                "get value error",
                "مشکلی در داده های ورودی وجود دارد ",
            )
            print(e)
            return (False, None)

    def delete_value(self):
        self.name.value.delete(0, "end")
        self.author.value.delete(0, "end")
        self.price.value.delete(0, "end")
        self.count.value.delete(0, "end")

    def get_search_value(self):
        value = {
            "name": self.name.value.get(),
            "author": self.author.value.get(),
        }
        if any(value.values()):
            return (True, value)
        else:
            return (False, {})

    def add_value(self, value):
        self.delete_value()
        self.name.value.insert(0, value[0])
        self.author.value.insert(0, value[1])
        self.price.value.insert(0, value[2])
        self.count.value.insert(0, value[3])


class GetValue(tk.Frame):
    def __init__(self, master, name, row, column):
        super().__init__(master=master)
        tk.Label(self, text=name, width=10).pack(
            side="left", fill="y", pady=2, padx=2, ipady=3, ipadx=3
        )
        self.value = tk.Entry(self, width=25)
        self.value.pack(side="left", fill="y", pady=2, padx=2, ipady=3, ipadx=3)
        self.grid(row=row, column=column, sticky="we")


class Main(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.book = master.book
        self.table = TableModel(
            self, columns=("id", "name", "author", "price", "count")
        )
        ListButton(self)
        self.grid(row=1, column=0, sticky="news")


class TableModel(tk.Frame):
    def __init__(self, master, columns, row=0, column=0):
        super().__init__(master=master)
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        scroll = tk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y", pady=2)
        self.table.pack(side="right", fill="both", expand=True, padx=2, pady=2)
        for clm in columns:
            self.table.column(clm, width=20, anchor = "center")
            self.table.heading(clm, text=clm)
        self.table["displaycolumns"] = columns[1:]
        self.grid(row=row, column=column, sticky="news")

    def remove_all_rows(self):
        children = self.table.get_children()
        for child in children:
            self.table.delete(child)

    def add_row(self, value):
        self.table.insert("", index=0, values=value)

    def show_rows(self, values):
        self.remove_all_rows()
        for value in values:
            self.add_row(value)


class CreateButton(tk.Button):
    def __init__(self, master, text, width, func, side="top"):
        super().__init__(master=master, text=text, width=width, command=func)
        self.pack(side=side, fill="both", expand=True, padx=5, pady=5, ipadx=2, ipady=2)


class ListButton(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.tablemodel = master.table
        self.table = master.table.table
        self.book = master.book
        CreateButton(self, text="تمایش همه ", width=20, func=self.show_all)
        CreateButton(self, text="اضافه کردن", width=20, func=self.add_book)
        CreateButton(self, text="جستجو ", width=20, func=self.search)
        CreateButton(self, text="ویرایش کردن ", width=20, func=self.editbook)
        CreateButton(self, text="حذف کردن ", width=20, func=self.delet_book)
        CreateButton(self, text="خروج", width=20, func=self.quit)
        self.table.bind("<<TreeviewSelect>>", self.item_select)
        self.table.bind("<Double-1>", self.double_select)
        self.show_all()
        self.grid(row=0, column=1, sticky="news")

    # creat_book,
    #     edit_book,
    #     search_book,
    #     get_all_book,
    #     add_order,
    #     show_order,
    #     sum_order,
    def double_select(self,event):
        child = self.table.selection()
        if 0 < len(child):
            value = self.table.item(child[0]).get("values")
            ask = askinteger(self,"تعداد خریداری شده را وارد کنید")
            if ask and ask < value[-1]:
                add_order(value[0],ask)
                self.show_all()
            else:
                showerror("","show error")
                        
    def item_select(self, event):
        child = self.table.selection()
        if 0 < len(child):
            value = self.table.item(child[0]).get("values")
            self.book.add_value(value[1:])

    def show_all(self):
        value = get_all_book()
        if value[0]:
            self.tablemodel.show_rows(value[1])
        else:
            showerror(
                "show date error",
                "مشکلی در نمایش داده ها وجود دارد لطفا بعدا تلاش کنید",
            )

    def add_book(self):
        value = self.book.get_value()
        if value[0]:
            resopons = creat_book(tuple(value[1].values()))
            if resopons:
                showinfo("", " کتاب  با موفقیت اضافه شد  ")
                self.show_all()
            else:
                showerror(
                    "add book error",
                    "در اضافه کردن کتاب به دیتابیس مشکلی پیش امد دوباره سعی کنید",
                )

    def delet_book(self):
        child = self.table.selection()
        if 0 < len(child):
            value = self.table.item(child[0]).get("values")
            remove_book(value[0])
            self.show_all()
            showinfo("", "با موفقیت حذف شد")
        else:
            showerror("", "برای حذف فیلد مورد نظر خود را انتخواب کنید")

    def editbook(self):
        child = self.table.selection()
        if 0 < len(child):
            id = self.table.item(child[0]).get("values")[0]
            value = self.book.get_value()
            if value[0]:
                if edit_book(tuple(value[1].values()), id):
                    showinfo("", "با موفقیت تغییر کرد")
                else:
                    showerror("have problem")
                self.show_all()

        pass

    def search(self):
        answer = self.book.get_search_value()
        if answer[0]:
            rows = search_book(answer[1])
            self.tablemodel.show_rows(rows[1])
        else:
            showerror("", "yeki az do gozine name ya order ra por konid")


if __name__ == "__main__":
    App("آزمون", (700, 500))
