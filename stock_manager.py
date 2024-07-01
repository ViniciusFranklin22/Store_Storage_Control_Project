import tkinter as tk
from tkinter import ttk  #temas do tkinter, mais mordenos
from tkinter import messagebox
from tkinter import *
from eng_dados import Data_Eng
import re
class StockManager:
    def __init__(self):
        self.table_name = "Stock"
        self.data = Data_Eng(self.table_name)
        self.root = tk.Tk()
        self.root.title("Stock Manager")
    
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.style = ttk.Style(self.frame)
        self.style.theme_use('clam')
        #primeira linha

        self.product_info = tk.LabelFrame(self.frame,text="Product Information")
        self.product_info.grid(row=0,column=0,pady=20,padx=20,sticky="news")

        self.product_name_label = tk.Label(self.product_info,text="Product Name")
        self.product_name_label.grid(row=0,column=0)
        self.product_name_variable = tk.StringVar()
        self.product_name_combo_box = ttk.Combobox(self.product_info,textvariable=self.product_name_variable,values=self.select_product_name())
        self.product_name_combo_box.grid(row=1,column=0)
        self.product_bottle_size_label = tk.Label(self.product_info,text="Bottle Size")
        self.product_bottle_size_label.grid(row=0,column=1)
        self.bottle_size_variable = StringVar()
        self.bottle_size = ttk.Combobox(self.product_info,textvariable=self.bottle_size_variable,values=self.select_bottle_sizes())
        #self.bottle_size.bind('<FocusIn>',lambda event :self.refresh_bottle_sizes(event))
        self.product_name_combo_box.bind('<KeyPress>',lambda event :self.refresh_bottle_sizes(event))
        self.bottle_size.bind('<Button>', lambda event: self.refresh_bottle_sizes(event))
        self.bottle_size.grid(row=1, column=1)
        self.product_quantity_label = tk.Label(self.product_info,text="Quantity")
        self.product_quantity_label.grid(row=0, column=2)
        self.quantity_variable = IntVar(self.root)
        self.product_quantity = tk.Spinbox(self.product_info,from_=0,to='infinity',textvariable=self.quantity_variable)
        self.product_quantity.grid(row=1, column=2)
        self.product_seller_label = tk.Label(self.product_info,text="Seller")
        self.product_seller_label.grid(row=0,column=3)
        self.product_seller = tk.Entry(self.product_info)
        self.product_seller.grid(row=1,column=3)

        self.config_padding(self.product_info, 10, 20)

        #segunda linha

        self.price_info = tk.LabelFrame(self.frame,text="Price Information")
        self.price_info.grid(row=1,column=0,pady=20,padx=20,sticky="news")

        self.cost_price_label = tk.Label(self.price_info,text="Cost Price (R$)")
        self.cost_price_label.grid(row=0,column=0)
        self.cost_price_entry = tk.Entry(self.price_info)
        self.cost_price_entry.grid(row=1,column=0)


        self.config_padding(self.price_info, 90, 20)

        #terceira linha

        self.input_button = tk.Button(self.frame,text="Input Data",command=self.enter_data,width=50,height=2)
        self.input_button.grid(row=2,column=0,padx=20,pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def refresh_bottle_sizes(self,event):

        if (event.state == 8 or 262152 and event.keysym =='??') or ((event.state == 8 or 262152) and event.keysym == "Down"):
            self.bottle_size['values'] = self.select_bottle_sizes()

    def select_bottle_sizes(self):

        query = f" DISTINCT Bottle_Size,Unit"
        where = f"Name = '{self.get_product_name()}'"

        value = self.data.select_where(columns=query,where=where,case="Product")

        if value == "":
            return [""]
        bottle_size_list = []
        for i in value:
            bottle_size_list.append(str(i[0])+i[1])
        print(bottle_size_list)
        return bottle_size_list

    def select_product_name(self):
        query = f"DISTINCT Name"
        value = self.data.select(query,'Product')
        product_list = []

        for i in value:
            product_list.append(i[0])
        return sorted(product_list,key= lambda element:element[0],reverse=False)


    def enter_data(self):

        if self.check_fields():

            where = f" Name = '{self.get_product_name()}' AND Bottle_Size = '{re.sub('[A-Z]','',re.sub('[a-z]','',self.get_bottle_size()))}'"

            fk = self.data.select_where(columns="ID",where=where,case="Product")

            values = [fk[0][0],self.get_quantity(),self.get_seller(),self.get_cost_price()]
            self.data.insert_data(values=values)
            fk_stock = self.data.select(columns="MAX(ID)")
            pk_stock_manager = self.data.select(columns="MAX(ID)",case="Stock_Manager")
            pk_stock_manager = pk_stock_manager if pk_stock_manager[0][0] != None else "0"
            for quantity in range(0,self.get_quantity()):
                stock_manager_values = [fk[0][0],fk_stock[0][0],1,"In Stock",""]
                print(pk_stock_manager[0][0])
                status = self.data.insert_data(values=stock_manager_values,case='Stock_Manager',send_id=int(pk_stock_manager[0][0])+quantity+1)
            if status[0] == "Succesfull":
                messagebox.showinfo(title="Data Registration", message="Your information has been submitted")
            self.clear_fields()

    def config_padding(self,frame,x,y):
        for widget in frame.winfo_children():
            widget.grid_configure(padx=x, pady=y)

    def on_closing(self):
        if messagebox.askyesno(title="Close",message="Do you want to close this window?"):
            self.root.destroy()

    def get_product_name(self):
        return self.product_name_combo_box.get().strip()
    def get_bottle_size(self):
        return self.bottle_size.get().strip()
    def get_quantity(self):
        return int(self.product_quantity.get())
    def get_seller(self):
        return self.product_seller.get().strip()
    def get_cost_price(self):
        try:
            return float(re.sub("[A-Z]", "",re.sub("[a-z]", "", self.cost_price_entry.get().replace(" ", "").replace(",", "."))))

        except Exception as e:
            return ""


    def check_fields(self):
        if self.get_seller() != "" and self.get_product_name() in self.select_product_name() and self.get_bottle_size() in self.select_bottle_sizes() and self.get_quantity() > 0:
            if type(self.get_cost_price()) == type(2.2):
                return True
            else:
                messagebox.showwarning(title="Numeric Error",message="Fill the numeric fields correctly")
        else:
            messagebox.showwarning(title="Error",message="Fill all the fields")
            return False



    def clear_fields(self):
        self.product_name_combo_box.delete(0,tk.END)
        self.bottle_size.delete(0,tk.END)
        self.product_quantity.config(textvariable=self.quantity_variable.set(0))
        self.product_seller.delete(0,tk.END)
        self.cost_price_entry.delete(0,tk.END)




if __name__ == "__main__":
   StockManager()