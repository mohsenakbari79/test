#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 18:38:26 2023

@author: malevin
"""

import tkinter as tk 

from tkinter import ttk
from tkinter.messagebox import showerror,showinfo

from postgre import (
    craete_book,
    get_all_book,
    remove_book,
    search_book
)


class App(tk.Tk):
    def __init__(self,title,defualt_size):
        super().__init__()
        self.geometry(f"{defualt_size[0]}x{defualt_size[1]}")
        self.title("title")
        self.rowconfigure(0,weight=1,uniform="a")
        self.rowconfigure(1,weight=3,uniform="a")
        self.columnconfigure(0,weight=1)
        self.book = Book(self)
        Main(self)
        self.mainloop()
        
        
        

class Book(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1),weight=1)
        self.name = GetValue(self, "name", 0,0)
        self.author = GetValue(self, "author",0,1)
        self.price = GetValue(self, "price",1,0)
        self.count = GetValue(self, "count",1,1)
        self.grid(row=0,column=0,sticky="news")
    
    def get_value(self):
        return {
            "name" : self.name.value.get(),
            "author" : self.author.value.get(),
            "price" : self.price.value.get(),
            "count" : self.count.value.get(),
            }
    def del_value(self):
        self.name.value.delete(0,"end")
        self.author.value.delete(0,"end")
        self.price.value.delete(0,"end")
        self.count.value.delete(0,"end")
        
    def set_value(self,value):
        self.del_value()
        self.name.value.insert(0,value[0])
        self.author.value.insert(0,value[1])
        self.price.value.insert(0,value[2])
        self.count.value.insert(0,value[3])



        
        
        
class GetValue(tk.Frame):
    def __init__(self,master,name,row,column):
        super().__init__(master=master)
        tk.Label(self,text=name,width=10).pack(side="left",padx=5, pady=5, ipadx=3,ipady=5,fill="x",expand=True)
        self.value = tk.Entry(self,width=25)
        self.value.pack(side="left",padx=5, pady=5, ipadx=3, ipady=5 ,fill="x",expand=True)
        self.grid(row=row,column=column,sticky="news")
        




class Main(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        self.book = master.book
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=4)
        self.columnconfigure(1,weight=1)
        self.table =TableModel(self, ("id","name","author","price","count"))
        ListButton(self)
        self.grid(row=1,column=0,sticky="news")
    
class TableModel(tk.Frame):
    def __init__(self,master,columns):
        super().__init__(master=master)
        scroll = tk.Scrollbar(self,orient="vertical")
        self.table = ttk.Treeview(self,columns=columns,show="headings",yscrollcommand=scroll.set,selectmode="browse")
        
        self.table.pack(side="left",fill="both",expand=True)
        scroll.pack(side="left",fill="y")
        
        self.grid(row=0,column=0,sticky="news")
            
        for clm in columns[1:]:
            self.table.heading(clm, text=clm)
            self.table.column(clm, width=20)
        self.table.heading(columns[0], text=columns[0])
        self.table.column(columns[0], width=20)
        self.table["displaycolumns"]=columns[1:]
        
    def addrow(self,value=None):
        self.table.insert(parent="", index=0, value = value)
    def remove_rows(self):
        for child in self.table.get_children():
            self.table.delete(child)
    
    def showrow(self,value):
        self.remove_rows()
        self.addrow(value)
    def showrows(self,values):
         self.remove_rows()
         if values:
             for value in values:
                 self.addrow(value)
                         
class Button(tk.Button):
    def __init__(self,master,text,func):
        super().__init__(master=master,text=text,command=func,width=15)
        self.pack(side="top",fill="both",expand=True,padx=3,pady=3,ipadx=3,ipady=3)

class ListButton(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        self.tablemodel= master.table
        self.table = master.table.table
        self.book = master.book
        Button(self,"اضافه کردن",self.addbook)
        Button(self,"show all",self.showall)
        Button(self,"remove",self.remove)
        Button(self,"serch",self.search)
        Button(self,"test5",self.test)
        Button(self,"test6",self.test)
        self.table.bind("<<TreeviewSelect>>",self.selecitems)
        self.grid(row=0,column=1,sticky="nesw")

    def selecitems(self,event):
        print("selected")
        select =  self.table.selection()
        if select:
            value = self.table.item(select[0])
            print(value.values())
            self.book.set_value(value.get("values")[:-1])
        pass
    
    def addbook(self):
        value = self.book.get_value()
        craete_book(tuple(value.values()))
        self.showall()
        pass
    def showall(self):
        values = get_all_book()
        self.tablemodel.showrows(values)

    def remove(self):
        select =  self.table.selection()
        if select:
            value = self.table.item(select[0])
            remove_book(value[-1])
            self.showall()
      
    def search(self):
        value = self.book.get_value()
        rows = search_book(value)
        print(rows)
        self.tablemodel.showrows(rows)
        
        pass
    def test(self):
        pass
if __name__ == "__main__":
    App("aprrove",(600,400))
    