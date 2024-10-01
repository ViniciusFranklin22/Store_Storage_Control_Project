import tkinter as tk
from tkinter import ttk  #temas do tkinter, mais mordenos
from tkinter import messagebox
from tkinter import *
from eng_dados import Data_Eng
import requests
import json
import re

class SalesWindow:
    def __init__(self):
        self.table_name = 'Sales'
        self.data = Data_Eng(self.table_name)
        self.root = tk.Tk()
        self.root.title("Sales Window")
        self.root.geometry("720x720")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.style = ttk.Style(self.frame)
        self.style.theme_use('clam')

        #primeira linha

        self.product_sale_frame = tk.LabelFrame(self.frame,text="Product Information",width=50,height=50)
        self.product_sale_frame.grid(row=0,column=0)

        self.type_label = tk.Label(self.product_sale_frame,text="Type")
        self.type_label.grid(row=0,column=0)
        self.type_variable = tk.StringVar()
        self.type_values = self.get_one_info("DISTINCT Type",case="Product")

        self.type_combobox = ttk.Combobox(self.product_sale_frame,textvariable=self.type_variable,values=self.type_values)
        self.type_combobox.grid(row=1,column=0)
        self.type_combobox.bind('<KeyPress>',lambda event:self.refresh_product_field(event))

        self.product_label = tk.Label(self.product_sale_frame,text="Product")
        self.product_label.grid(row=0,column=1)
        self.product_variable = tk.StringVar()

        self.product_combobox = ttk.Combobox(self.product_sale_frame,textvariable=self.product_variable)
        self.product_combobox.grid(row=1,column=1)
        self.product_combobox.bind('<Button>',lambda event:self.refresh_product_field(event))
        self.product_combobox.bind('<KeyPress>',lambda event :self.refresh_bottle_size(event))

        self.bottle_size_label = tk.Label(self.product_sale_frame,text="Bottle Size")
        self.bottle_size_label.grid(row=0,column=2)
        self.bottle_size_variable = tk.StringVar()
        self.bottle_size_combobox = ttk.Combobox(self.product_sale_frame, textvariable=self.bottle_size_variable)
        self.bottle_size_combobox.grid(row=1,column=2)
        self.bottle_size_combobox.bind('<Button>', lambda event: self.refresh_bottle_size(event))

        self.quantity_label = tk.Label(self.product_sale_frame,text="Quantity")
        self.quantity_label.grid(row=0,column=3)
        self.quantity_variable = tk.IntVar(self.root)
        self.quantity_spin_box = tk.Spinbox(self.product_sale_frame,from_=0,to="infinity",
                                            textvariable=self.quantity_variable)
        self.quantity_spin_box.grid(row=1,column=3)

        self.config_padding(self.product_sale_frame,10,10)
        self.product_sale_frame.grid_configure(pady=10,padx=10)

        # segunda linha
        self.add_basket_button = tk.Button(self.frame,text="Add to the Basket",command=self.add_to_the_basket,width=50,height=2)
        self.add_basket_button.grid(row=1,column=0)

        self.add_basket_button.grid_configure(padx=10,pady=10)





        # terceira linha


        self.basket_table = ttk.Treeview(self.frame,columns=('Type','Product','Bottle Size','Quantity','Price'),
                                         height=10,show="headings")
        self.basket_table.column('Type',anchor=CENTER, stretch=NO, width=140)
        self.basket_table.heading('Type',text='Type')
        self.basket_table.column('Product', anchor=CENTER, stretch=NO, width=250)
        self.basket_table.heading('Product', text='Product')
        self.basket_table.column('Bottle Size', anchor=CENTER, stretch=NO, width=100)
        self.basket_table.heading('Bottle Size', text='Bottle Size')
        self.basket_table.column('Quantity', anchor=CENTER, stretch=NO, width=100)
        self.basket_table.heading('Quantity', text='Quantity')
        self.basket_table.column('Price', anchor=CENTER, stretch=NO, width=100)
        self.basket_table.heading('Price', text='Price')
        self.basket_table.grid(row=2,column=0)
        self.basket_table.grid_configure(pady=10,padx=10)

        self.basket_table.bind('<Delete>',lambda event: self.delete_item_ttkview_table(event))

        # quarta linha

        self.customer_frame = LabelFrame(self.frame,text="Customer Information",width=50,height=50)
        self.customer_frame.grid(row=3,column=0)
        self.customer_name_label = tk.Label(self.customer_frame,text="Customer Name")
        self.customer_name_label.grid(row=0,column=0)


        self.customer_name_combo_box = ttk.Combobox(self.customer_frame,values=self.get_two_info(field="DISTINCT FIRST,LAST",case="Customer"))
        self.customer_name_combo_box.grid(row=1,column=0)
        self.customer_neighborhood_label = tk.Label(self.customer_frame,text="Customer Neighborhood")
        self.customer_neighborhood_label.grid(row=0,column=2)


        self.customer_neighborhood= tk.Entry(self.customer_frame)
        self.customer_neighborhood.grid(row=1, column=2)
        self.customer_street_label = tk.Label(self.customer_frame,text="Customer Street")
        self.customer_street_label.grid(row=0,column=3)


        self.customer_street = tk.Entry(self.customer_frame)
        self.customer_street.grid(row=1 ,column=3)
        self.customer_complement_label = tk.Label(self.customer_frame,text="Customer Complement")
        self.customer_complement_label.grid(row=2,column=1)


        self.customer_complement_combo_box = ttk.Combobox(self.customer_frame)
        self.customer_complement_combo_box.grid(row=3, column=1)
        self.customer_cep_label = tk.Label(self.customer_frame,text="CEP XXXXX-XXX")
        self.customer_cep_label.grid(row=0,column=1)
        self.customer_cep_combo_box = ttk.Combobox(self.customer_frame)
        self.customer_cep_combo_box.grid(row=1,column=1)
        self.customer_cep_combo_box.bind('<KeyPress>',lambda event :self.refresh_after_cep(event))
        self.customer_street.bind('<Button>',lambda event :self.refresh_after_cep(event))
        self.customer_neighborhood.bind('<Button>', lambda event: self.refresh_after_cep(event))
        self.customer_number_label = tk.Label(self.customer_frame,text="Number")
        self.customer_number_label.grid(row=2,column=0)
        self.customer_name_combo_box.bind('<KeyPress>',lambda event:self.refresh_cep_fields(event))
        self.customer_cep_combo_box.bind('<Button>',lambda event:self.refresh_cep_fields(event))
        self.customer_number = ttk.Combobox(self.customer_frame)
        self.customer_number.grid(row=3,column=0)

        self.config_padding(self.customer_frame,10,10)
        self.customer_frame.grid_configure(padx=10,pady=10)
        # quinta linha

        self.finnish_sale_button = tk.Button(self.frame,text="Finnish Sale",width=50,height=2,command=self.finnish_sale)
        self.finnish_sale_button.grid(row=4,column=0)
        self.finnish_sale_button.grid_configure(pady=10,padx=10)

        self.table_control = 0

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()




    def config_padding(self,frame,x,y):
        for widget in frame.winfo_children():
            widget.grid_configure(padx=x, pady=y)

    def refresh_number_complement(self):

        info = self.data.select_where(columns="NUMBER,COMPLEMENT",case="Address",where=f"CEP = '{self.get_customer_cep()}'")
        number = []
        complement = []
        for x in info:
            number.append(x[0])
            complement.append(x[1])
        self.customer_number["values"] = number
        self.customer_complement_combo_box["values"] = complement

    def refresh_product_field(self,event):

        if ((event.state == 8 or 262152) and event.keysym =='??') or ((event.state == 8 or 262152) and (event.keysym == "Tab" or event.keysym =="Return")):

            self.product_combobox['values'] = self.get_one_info(field="DISTINCT NAME",case="Product",where=f"Type = '{self.get_type()}'")

    def refresh_cep_fields(self,event):

        if ((event.state == 8 or 262152) and event.keysym == '??') or ((event.state == 8 or 262152) and (event.keysym == "Tab" or event.keysym == "Return")):
            name = self.get_customer_name().split()
            self.customer_cep_combo_box["values"] = self.data.select_where(columns="DISTINCT(Address.CEP)",where=f"Address.ID = Sales.ADDRESS_ID AND Sales.CUSTOMER_ID = Customer.ID AND Customer.FIRST = '{name[0]}'AND Customer.LAST = '{name[1]}'",case="Address,Sales,Customer ")


    def refresh_bottle_size(self,event):
        if ((event.state == 8 or 262152) and event.keysym =='??') or ((event.state == 8 or 262152) and (event.keysym == "Tab" or event.keysym =="Return")):
            self.bottle_size_combobox['values'] = self.get_two_info(field="DISTINCT Bottle_Size, Unit", case="Product",
                                                                where=f"Type = '{self.get_type()}' AND Name ='{self.get_product()}'")

    def refresh_after_cep(self,event):
        if ((event.state == 8 or 262152) and event.keysym =='??') or ((event.state == 8 or 262152) and (event.keysym == "Tab" or event.keysym =="Return")):
            self.cep_api()



    def get_one_info(self,field,case="1",where="5"):
        value = self.data.select(columns=field,case=case) if where == "5" else self.data.select_where(columns=field,where=where,case=case)
        list = []

        for i in value:
            list.append(i[0])

        return list

    def get_two_info(self,field,case="1",where="5"):
        value = self.data.select(columns=field,case=case) if where == "5" else self.data.select_where(columns=field,where=where,case=case)
        list = []

        for i in value:

            list.append(str(i[0])+" "+ str(i[1]))

        return list

    def check_avalilability(self):
        product_id = self.get_product()[0:3]+self.get_type()[0:3]+self.get_bottle_size().replace(" ","")
        value = self.data.select_where(columns="SUM(VALUE)",where=f"AVAILABILITY = 'In Stock' AND PRODUCT_ID = '{product_id}' GROUP BY PRODUCT_ID",case="Stock_Manager")

        return 0 if value==[] else int(value[0][0])

    def finnish_sale(self):

        if self.check_customer_fields() and self.get_values_in_ttview_table()[:-1] != []:
            status_add = self.insert_address()
            status_sales = self.insert_sales()
            if status_sales[0] == "Succesfull" and status_add[0] == "Succesfull":
                messagebox.showinfo(title="Data Submitted",message="Your Data has been Successfully Submitted")
                self.clear_customer_fields()
                self.basket_table.delete(*self.basket_table.get_children())
                self.table_control = 0
            else:
                messagebox.showwarning(title="Error",message=f"Address: {status_add}, Sales: {status_sales}")

    def cep_api(self):
        url = 'https://brasilapi.com.br/api/cep/v1/' + self.get_customer_cep()
        try:
            result = requests.get(url=url)
            json_result = json.loads(result.content)
            self.customer_neighborhood.delete(0,tk.END)
            self.customer_neighborhood.insert(0,json_result["neighborhood"])
            self.customer_street.delete(0, tk.END)
            self.customer_street.insert(0,json_result["street"])
            self.refresh_number_complement()
        except Exception as e:
            print(e.args)


    def add_to_the_basket(self):
        if self.check_product_fields() and self.table_control == 0:
            info_products_values = [self.get_type(),self.get_product(),self.get_bottle_size(),self.get_quantity(),'R$ '+str(self.get_price(self.get_quantity()))]
            self.basket_table_insert(info_products_values,index=0)
            soma = ['', '', '', 'Total: ', "R$ " + str(self.find_item_basket_table(2, 'Total: '))]
            self.basket_table_insert(soma,index=tk.END)
            self.table_control=+1
            self.clear_product_fields()

        elif (self.table_control > 0 and self.check_product_fields()):
            info_products_values = [self.get_type(),self.get_product(),self.get_bottle_size(),self.get_quantity(),'R$ '+str(self.get_price(self.get_quantity()))]
            self.basket_table_insert(info_products_values,index=0)
            soma = ['', '', '','Total: ', "R$ " + str(self.find_item_basket_table(2, 'Total: '))]
            self.basket_table.item((self.find_item_basket_table(1,'Total: ')),values=soma)
            self.clear_product_fields()


    def get_price(self,quantity):
        product_id = self.get_product()[0:3]+self.get_type()[0:3]+self.get_bottle_size().replace(" ","")
        print(product_id)
        return float((self.data.select_where(columns='"Sell Price"',where=f"ID='{product_id}'",case="Product"))[0][0])*quantity




    def find_item_basket_table(self,function,item):
        if function == 1:
            for line in self.basket_table.get_children():
                if self.basket_table.item(line)['values'][3] == item:
                    return line
        elif function == 2:
            list = []
            for line in self.basket_table.get_children():
                list.append(float(self.basket_table.item(line)['values'][4][3:]))
            if len(list) > 1:
                return sum(list[:-1])
            else:
                return sum(list)


    def basket_table_insert(self,values,index):
        self.basket_table.insert(parent='',index=index,values=values)

    def check_product_fields(self):

        if self.get_type() in self.type_combobox["values"] and self.get_product() in self.product_combobox['values'] and self.get_bottle_size() in self.bottle_size_combobox['values'] and self.get_quantity() > 0:
            if self.check_avalilability() >= self.get_quantity():
                return True
            else:
                messagebox.showwarning(title="Not in Stock", message=f"Just {self.check_avalilability()} {self.get_product()} {self.get_bottle_size()} in Stock")
                return False
        else:
            messagebox.showwarning(title="Error",message="Please fill all the product fields")
            return False

    def clear_product_fields(self):
        self.type_combobox.delete(0,tk.END)
        self.product_combobox.delete(0,tk.END)
        self.bottle_size_combobox.delete(0,tk.END)
        self.quantity_variable.set(0)
        self.quantity_spin_box.config(textvariable=self.quantity_variable)

    def check_customer_fields(self):
        if self.get_customer_name() in self.customer_name_combo_box["values"] and self.find_item_basket_table(2,'') > 0 and self.get_customer_neighborhood() != '' and self.get_customer_street() != '':
            if len(self.get_customer_cep()) == 8 and self.get_customer_number() != "":
                return True
        else:
            messagebox.showwarning(title="Error",message="Please fill all the customer fields")
            return False

    def clear_customer_fields(self):
        self.customer_complement_combo_box.delete(0,tk.END)
        self.customer_neighborhood.delete(0, tk.END)
        self.customer_street.delete(0, tk.END)
        self.customer_name_combo_box.delete(0, tk.END)
        self.customer_number.delete(0,tk.END)
        self.customer_cep_combo_box.delete(0,tk.END)


    def delete_item_ttkview_table(self,_):
        for i in self.basket_table.selection():
            self.basket_table.delete(i)
        info_products_values = [self.get_type(),self.get_product(),self.get_bottle_size(),self.get_quantity(),'R$ '+str(self.get_price(self.get_quantity()))]
        self.basket_table_insert(info_products_values,index=0)
        for i in self.basket_table.get_children():
            print(self.basket_table.item(i)["values"])
        soma = ['', '', '','Total: ', "R$ " + str(self.find_item_basket_table(2, 'Total: '))]
        self.basket_table.item((self.find_item_basket_table(1,'Total: ')),values=soma)
        self.clear_product_fields()




    def get_values_in_ttview_table(self):
        list = []
        for line in self.basket_table.get_children():
            list.append(self.basket_table.item(line)["values"])
        return list

    def insert_sales(self):
        sales_list = self.get_values_in_ttview_table()[:-1]
        product_id = []
        quantity = []
        for i in sales_list:
            product_id.append((i[1][0:3] + i[0][0:3] + i[2].replace(' ',"")))
            quantity.append(i[3])
        address_id = str(self.get_customer_cep())+str(self.get_customer_number())+self.get_customer_complement()
        name = self.get_customer_name().split()
        customer_id = self.data.select_where(columns="ID",where=f"FIRST = '{name[0]}'AND LAST = '{name[1]}'",case="Customer")[0][0]
        print(address_id,product_id[0],quantity,customer_id,name)
        session = self.data.select(columns="MAX(SESSION)",case="Sales")[0][0]
        session = session + 1 if session is not None else 1
        print(session)
        for x in range(0,len(product_id)):
            print(product_id[x])
            values = [session,product_id[x],customer_id,address_id,quantity[x],self.data.select_where(columns='"Sell Price"',where=f"ID ='{product_id[x]}'",case="Product")[0][0]]
            print(values)
            status =self.data.insert_data(values=values,case="Sales")
            stock_manager_id = self.data.select_where(columns="ID",where=f"PRODUCT_ID = '{product_id[x]}' AND AVAILABILITY = 'In Stock'",case="Stock_Manager")
            for n in range(0,int(quantity[x])):
                print(stock_manager_id)
                self.data.update_data(columns_update=f"AVAILABILITY = 'Sold',SELL_ID = '{status[1]}'",where=f"ID='{stock_manager_id[n][0]}'",case="Stock_Manager")
            return status




    def insert_address(self):
        ##############      Arrumar
        print(self.get_values_in_ttview_table()[:-1])
        address_id = str(self.get_customer_cep()) + str(self.get_customer_number()) + self.get_customer_complement()
        print(self.data.select_where(columns="*",where=f"ID = '{address_id}'",case="Address"))
        if self.data.select_where(columns="*",where=f"ID = '{address_id}'",case="Address") == []:
            values = [self.get_customer_cep(),self.get_customer_street(),self.get_customer_neighborhood(),self.get_customer_number(),self.get_customer_complement()]
            status = self.data.insert_data(values=values,case="Address")
            return status
        return ["Succesfull"]


    def get_type(self):
        return self.type_combobox.get().strip()
    def get_product(self):
        return self.product_combobox.get().strip()
    def get_bottle_size(self):
        return self.bottle_size_combobox.get().strip()
    def get_quantity(self):
        return int(self.quantity_spin_box.get().strip())
    def get_customer_name(self):
        return self.customer_name_combo_box.get().strip()
    def get_customer_neighborhood(self):
        return self.customer_neighborhood.get().strip()
    def get_customer_street(self):
        return self.customer_street.get().strip()
    def get_customer_complement(self):
        return self.customer_complement_combo_box.get().strip()
    def get_customer_number(self):
        return re.sub("[A-Z]","",re.sub("[a-z]","",self.customer_number.get().replace(" ","").replace("-","")))
    def get_customer_cep(self):
        return re.sub("[A-Z]","",re.sub("[a-z]","",self.customer_cep_combo_box.get().replace(" ","").replace("-","")))

    def on_closing(self):
        if messagebox.askyesno(title="Close",message="Do you want to close this window?"):
            self.root.destroy()


if __name__ == "__main__":
   SalesWindow()