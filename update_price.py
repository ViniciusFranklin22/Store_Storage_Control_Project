import tkinter as tk
from tkinter import ttk  #temas do tkinter, mais mordenos
from tkinter import messagebox
from tkinter import *
from eng_dados import Data_Eng
import re


class UpdatePrice:
    def __init__(self):
        self.table_name = "Product"
        self.data = Data_Eng(self.table_name)
        self.root = tk.Tk()
        self.root.title("New Product Window")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.style = ttk.Style(self.frame)
        self.style.theme_use('clam')

        self.update_price = tk.LabelFrame(self.frame,text="Update Price")
        self.update_price.grid(row=0,column=0)

        self.products_label = tk.Label(self.update_price,text="Products")
        self.products_label.grid(column=0,row=0)
        self.products_combo_box = ttk.Combobox(self.update_price,width=30,values=self.get_updt_products())
        self.products_combo_box.grid(column=0,row=1)
        self.new_price_label = tk.Label(self.update_price,text="New Price")
        self.new_price_label.grid(column=1,row=0)
        self.new_price_entry = tk.Entry(self.update_price)
        self.new_price_entry.grid(column=1,row=1)
        self.update_button = tk.Button(self.frame,text="Update Data",command=self.update_price_value,width=50,height=1)
        self.update_button.grid(column=0,row=1,pady=10,padx=10)

        self.config_padding(self.update_price,x=100,y=10)


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

    def update_price_value(self):
        if self.check_update_fields():
            prd = self.get_update_product().split()
            product_id = prd[0][0:3] + prd[1][0:3] + prd[2]
            print(prd,product_id,self.get_update_price())
            try:
                self.data.update_data(columns_update=f'"Sell Price" = {self.get_update_price()}',where=f'ID="{product_id}"')
                messagebox.showinfo(title="Success",message="Your price has been updated")
                self.clear_update_fields()

            except Exception as e:
                messagebox.showwarning(title="Error",message=f'Error: {e.args}')
            self.insert_table_tview()
    def clear_update_fields(self):
        self.products_combo_box.delete(0,tk.END)
        self.new_price_entry.delete(0,tk.END)



    def check_update_fields(self):
        if self.get_update_price() != "" and self.get_update_product() in self.products_combo_box["values"]:
            return True
        else:
            messagebox.showwarning(title="Error",message="Fill all the fields")
            return False

    def get_updt_products(self):
        list_prod = sorted(self.data.select('Name, Type, "Bottle_Size", Unit, "Sell Price"'),key= lambda element : element[0],reverse=True)
        list = []
        for i in list_prod:
            list.append(i[0]+" "+i[1]+" "+str(i[2])+i[3])
        return list
    def insert_table_tview(self):

        list_tuples = sorted(self.data.select('Name, Type, "Bottle_Size", Unit, "Sell Price"'),key= lambda element : element[0],reverse=True)
        print(list_tuples)
        for i in self.table.get_children():
            self.table.delete(i)
        for tuples in list_tuples:
            self.table.insert(parent='',index=0,values=tuples)



    def get_price(self):
        try:
            return float(re.sub('[a-z]',"",self.price_entry.get().replace(" ","").replace(",",".")))
        except Exception as e:
            return ""

    def get_update_price(self):
        try:
            return float(re.sub("[A-Z]", "",re.sub("[a-z]", "", self.new_price_entry.get().replace(" ", "").replace(",", "."))))

        except Exception as e:
            return ""

    def get_update_product(self):
        return self.products_combo_box.get()


    def config_padding(self,frame,x,y):
        for widget in frame.winfo_children():

            widget.grid_configure(padx=x, pady=y)

    def on_closing(self):
        if messagebox.askyesno(title="Close",message="Do you want to close this window?"):
            self.root.destroy()


if __name__ == "__main__":
   UpdatePrice()