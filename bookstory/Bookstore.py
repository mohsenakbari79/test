import tkinter as tk

from tkinter.simpledialog import askinteger
from tkinter.messagebox import showinfo,showerror
from tkinter import ttk

from bookdb import (
    get_all_data,
    creatbook,
    serch_book,
    removebook,
    editbook,
    add_row_report,
    show_row_report,
    search_rows_report,
    sum_rows_report
)

class App(tk.Tk):
    def __init__(self,title,size):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(width=size[0],height=size[1])
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.menu = tk.Menu(self,tearoff=0)
        self.config(menu=self.menu)
        self.menu.add_command(label="report",command=self.report)
       
        self.book = Book(self)
        Main(self)
        self.mainloop()
        
    def report(self):
        Report(self)
        



class Report(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master,bg= "white")
        menu = tk.Menu(self.master,tearoff=0)
        menu.add_command(label="home",command=self.deleteframe)
        
        self.frame = tk.Frame(self)
        self.s_date = GetValue(self.frame,"start date",0,0)
        self.e_date = GetValue(self.frame,"end date",0,1)
        tk.Button(self.frame, text="search",command=self.serch_items).grid(row=0,column=2,sticky="we")
        tk.Button(self.frame, text="sum",command=self.sum_items).grid(row=0,column=3,sticky="we")
        
        self.frame.pack(side="top",fill="x")
        
        master.config(menu=menu)
        
        columns=("id","idbook","name","author","count","factor","time")
        self.table = ttk.Treeview(
                self,columns=columns,
                show="headings",
                selectmode="browse",
                
                )
        self.table["displaycolumns"]=columns[1:]
        self.table.pack(side="left",fill="both",expand=True)
        scroll = tk.Scrollbar(self,orient="vertical")
        scroll.pack(side="left",fill="y")
        self.table.configure(yscrollcommand=scroll.set)
        for clm in columns:
            self.table.heading(clm,text=clm)
            self.table.column(clm,width=20,anchor="center")
        self.showrow()
        
        self.grid(row=0,column=0,sticky="nwes")
        self.grid(row=0,rowspan=2,column=0,columnspan=1,sticky="news")
        

    def deleteframe(self):
        menu = tk.Menu(self.master,tearoff=0)
        menu.add_command(label="report",command=self.master.report)
        self.master.config(menu=menu)
        # self.grid_forget()
        self.destroy()
        
        
    def remove_all_row(self):
        for child in self.table.get_children():
            self.table.delete(child)
    
    def showrow(self,values=None):
        self.remove_all_row()
        if  values is None:
            values = show_row_report()
        for value in values:
            self.table.insert(
                    index=0,
                    parent="",
                    value=value
                    )
            
        
    def serch_items(self):
        start_date = self.s_date.value.get()
        end_date = self.e_date.value.get()
        if start_date and end_date:
            values = search_rows_report(start_date,end_date)
            print(values)
            
            self.showrow(values)
            
    def sum_items(self):
        start_date = self.s_date.value.get()
        end_date = self.e_date.value.get()
        if start_date and end_date:
            values = sum_rows_report(start_date,end_date)
            if values:
                tk.Label(self.frame, text="Sum Price : "+str(values[0])).grid(row=0, column=4)
        
        
        


class GetValue(tk.Frame):
    def __init__(self,master,text,row,column):
        super().__init__(master=master)
        tk.Label(master=self,text=text,width=10).pack(side="left",fill="both",expand=True,padx=5,pady=5,ipadx=3,ipady=3)
        self.value = tk.Entry(master=self,width=20)
        self.value.pack(side="left",fill="y",expand=True,padx=5,pady=5,ipadx=3,ipady=3)
        self.grid(row=row,column=column,sticky="we")

class Book(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1),weight=1)
        self.grid(row=0,column=0,sticky="sewn")
        
        self.name = GetValue(self,"name",0,0)
        self.author = GetValue(self,"author",0,1)
        self.price = GetValue(self,"price",1,0)
        self.count = GetValue(self,"count",1,1)

    def get_value(self):
        try :
            return (True,{
                "name": self.name.value.get(),
                "author": self.author.value.get(),
                "price": float(self.price.value.get()),
                "count": int(self.count.value.get())
            })
        except:
            showerror(self,"There is a problem with the input value. Please be careful when typing the input values (str,str,int,float)")
            return(False,None)
    def search_get_value(self):
        return {
                "name": self.name.value.get(),
                "author": self.author.value.get(),
        }
        
    def remove_all_value(self):
        self.name.value.delete(0,"end")
        self.author.value.delete(0,"end")
        self.price.value.delete(0,"end")
        self.count.value.delete(0,"end")
        
    def addvalue(self,value):
        if 0<len(value):
            self.name.value.insert(0,value[0])
            self.author.value.insert(0,value[1])
            self.price.value.insert(0,value[2])
            self.count.value.insert(0,value[3])
    
    

class Main(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        self.book = master.book
        self.columnconfigure(0,weight=4)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        self.tablemodel =  Table(self,("id","name","author","price","count"))
        ListButton(self)
        self.grid(row=1,column=0,sticky="nwes")
        

class Table(tk.Frame):
    def __init__(self,master,columns):
        super().__init__(master=master)
        self.table = ttk.Treeview(
                self,columns=columns,
                show="headings",
                selectmode="browse",
                )
        scroll = tk.Scrollbar(self,orient="vertical",command=self.table.yview)
        scroll.pack(side="right",fill="y")
                
        self.table.configure(yscrollcommand=scroll.set)
        
        
        self.table["displaycolumns"]=columns[1:]
        self.table.pack(side="right",fill="both",expand=True)
        for clm in columns:
            self.table.heading(clm,text=clm)
            self.table.column(clm,width=20,anchor="center")
        self.grid(row=0,column=0,sticky="nwes")

    def addrow(self,value):
        self.table.insert(
                index=0,
                parent="",
                value=value
                )
    def remove_all_row(self):
        for child in self.table.get_children():
            self.table.delete(child)

    def show_one_row(self,value):
        self.remove_all_row()
        self.addrow(value)

    def show_value(self,values=None):
        self.remove_all_row()
        if values is None:
            values = get_all_data()
            pass
        for value in values:
            self.addrow(value)



class Button(tk.Button):
    def __init__(self,master,name,func):
        super().__init__(master=master,text=name,command=func,width=20)
        self.pack(side="top",padx=2,pady=3,ipadx=1,ipady=5,fill="both",expand=True)

class ListButton(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        self.model = master.tablemodel
        self.table = master.tablemodel.table
        self.book = master.book
        Button(self,"showall",self.showall)
        Button(self,"addnew",self.addnew)
        Button(self,"search",self.search)
        Button(self,"edit",self.edit)
        Button(self,"delete",self.delete)
        Button(self,"quit",self.quit)
        self.table.bind("<<TreeviewSelect>>",self.select_item)
        self.table.bind("<Double-1>", self.double_item)
        self.model.show_value()
        self.grid(row=0,column=1,sticky="news")
    

    def select_item(self,event):
        if 0<len(self.table.selection()):
            self.book.remove_all_value()
            value = self.table.item(self.table.selection()[0]).get("values")
  
            self.book.addvalue(value[1:])
        
    def addnew(self):
        value= self.book.get_value()
        if value[0]:
            value=value[1]
            creatbook(value.values())
            # self.book.remove_all_value()
            self.model.show_value()
            
    def edit(self):
        id = self.table.item(self.table.selection()[0]).get("values")[0]
        value=self.book.get_value()
        print("test",value)
        if value[0]:
            value =  tuple(value[1].values()) +(id,)
            editbook(value)
            self.showall()
        
        
    def delete(self):
        if 0<len(self.table.selection()):
            id = self.table.item(self.table.selection()[0]).get("values")[0]
            removebook(id)
            self.book.remove_all_value()
            self.model.show_value()
            
    def search(self):
        value= self.book.search_get_value()
        rows = serch_book(value)
        self.model.show_value(rows) 

    def double_item(self,event):
        select_item = self.table.selection()
        if not select_item:
            return
        else:
            item_iid = select_item[0]

            item_text = list(self.table.item(item_iid, "values"))
            asknumber = askinteger(self,f"enter number for sale book{item_text[1]}")
            if asknumber:
                if asknumber < int(item_text[4]):
                    showinfo(self,f"Reduced inventory equals cost {(float(asknumber)*float(item_text[3]))}")
                    item_text[4] = int(item_text[4]) - asknumber
                    value = tuple(item_text[1:]) + (item_text[0],)
                    add_row_report(item_text,(asknumber,float(asknumber)*float(item_text[3])))
                    editbook(value)
                    self.showall()
                else:
                    showerror(self,"Imported stock is more than stock")
            
        
        

        
        
    def showall(self):
        self.model.show_value()
   
#    def seach_book():
    

    def test(self):
        pass



   


if __name__ == "__main__":
    App("Book Store",(800,400))

