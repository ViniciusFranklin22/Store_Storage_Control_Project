import tkinter as tk
from tkinter import ttk  #temas do tkinter, mais mordenos
from tkinter import messagebox
from tkinter import *
from eng_dados import Data_Eng
import re


class NewProductWindow:
    def __init__(self):
        self.table_name = "Product"
        self.data = Data_Eng(self.table_name)
        self.root = tk.Tk()
        self.root.title("New Product Window")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.style = ttk.Style(self.frame)
        self.style.theme_use('clam')
        #primeira linha

        self.product_info = tk.LabelFrame(self.frame,text="Product Information")
        self.product_info.grid(row=0,column=0,pady=20,padx=20)

        self.type_label = tk.Label(self.product_info,text="Type")
        self.type_label.grid(row=0,column=0)
        self.type_drinks = ["Soda","Beer","Water","Energy-Drink","Isotonic","Vodka","Juice","Wine"]
        self.type_combo_box = ttk.Combobox(self.product_info,values=self.type_drinks)
        self.type_combo_box.grid(row=1,column=0)
        self.product_name_label = tk.Label(self.product_info,text="Product Name")
        self.product_name_label.grid(row=0,column=1)
        self.product_name_entry = tk.Entry(self.product_info)
        self.product_name_entry.grid(row=1, column=1)
        self.bottle_size_label = tk.Label(self.product_info,text="Bottle Size")
        self.bottle_size_label.grid(row=0, column=2)
        self.bottle_size_entry = tk.Entry(self.product_info)
        self.bottle_size_entry.grid(row=1, column=2)
        self.unit_label = tk.Label(self.product_info,text="Unit")
        self.unit_label.grid(row=0,column=3)
        self.unit = ["ml","L"]
        self.unit_combo_box = ttk.Combobox(self.product_info,values=self.unit)
        self.unit_combo_box.grid(row=1,column=3)
        self.price_label = tk.Label(self.product_info,text="Sell Price")
        self.price_label.grid(row=2,column=0)
        self.price_entry = tk.Entry(self.product_info)
        self.price_entry.grid(row=3,column=0)

        self.config_padding(self.product_info, 10, 10)

        #segunda linha

        self.input_button = tk.Button(self.frame,text="Input Data",command=self.enter_data,width=50,height=2)
        self.input_button.grid(row=1,column=0,pady=10,padx=10)





        #quarta linha

        self.table = ttk.Treeview(self.frame,columns=["Product Name","Type","Bottle Size","Unit","Price"],show="headings")
        self.table.column('Product Name',anchor=CENTER, stretch=NO, width=200)
        self.table.heading('Product Name',text="Product Name")
        self.table.column('Type',anchor=CENTER, stretch=NO, width=140)
        self.table.heading('Type',text="Type")
        self.table.column('Bottle Size',anchor=CENTER, stretch=NO, width=140)
        self.table.heading('Bottle Size',text="Bottle Size")
        self.table.column('Unit',anchor=CENTER, stretch=NO, width=140)
        self.table.heading('Unit',text="Unit")
        self.table.column('Price', anchor=CENTER, stretch=NO, width=140)
        self.table.heading('Price', text="Price")

        self.table.grid(row=3,column=0,padx=20,pady=20)
        self.insert_table_tview()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def insert_table_tview(self):

        list_tuples = sorted(self.data.select('Name, Type, "Bottle_Size", Unit, "Sell Price"'),key= lambda element : element[0],reverse=True)
        print(list_tuples)
        for i in self.table.get_children():
            self.table.delete(i)
        for tuples in list_tuples:
            self.table.insert(parent='',index=0,values=tuples)

    def get_type(self):
        return self.type_combo_box.get().strip()
    def get_product_name(self):
        return self.product_name_entry.get().strip()

    def get_bottle_size(self):
        return self.bottle_size_entry.get().strip()

    def get_unit(self):
        return self.unit_combo_box.get().strip()

    def get_price(self):
        try:
            return float(re.sub('[a-z]',"",self.price_entry.get().replace(" ","").replace(",",".")))
        except Exception as e:
            return ""




    def enter_data(self):
        if self.check_fields():
            values = [self.get_product_name(),self.get_type(),self.get_bottle_size(),self.get_unit(),self.get_price()]
            status = self.data.insert_data(values=values)
            if status[0] == "Succesfull":
                messagebox.showinfo(title="Data Registration", message="Your information has been submitted")
            else:
                messagebox.showwarning(title="Error", message="Internal Error")
            self.insert_table_tview()
            self.clear_fields()

    def config_padding(self,frame,x,y):
        for widget in frame.winfo_children():

            widget.grid_configure(padx=x, pady=y)

    def check_fields(self):
        if self.get_type() in self.type_drinks and self.get_bottle_size() != ""  and self.get_unit() in self.unit and self.get_product_name() != "" and self.get_price() != "":
            return True
        else:
            messagebox.showwarning(title="Error",message="Please fill all the product fields")
            return False

    def clear_fields(self):
        self.bottle_size_entry.delete(0,tk.END)
        self.type_combo_box.delete(0,tk.END)
        self.product_name_entry.delete(0,tk.END)
        self.unit_combo_box.delete(0,tk.END)
        self.price_entry.delete(0,tk.END)

    def on_closing(self):
        if messagebox.askyesno(title="Close",message="Do you want to close this window?"):
            self.root.destroy()


if __name__ == "__main__":
   NewProductWindow()