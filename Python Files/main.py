import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from sales_window import SalesWindow
from tkinter import ttk
from new_product_window import NewProductWindow
from stock_manager import StockManager
from register_new_customer import RegisterNewCustomer
from update_price import UpdatePrice

class Sales:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Beverage Delivery")
        self.root.geometry("720x720")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.image_frame = tk.LabelFrame(self.frame)
        self.image_frame.grid(row=0,column=0)

        self.image1_open = Image.open("Screenshot_1.png")
        self.resize_image1 = self.image1_open.resize((700,200))
        self.image1 = ImageTk.PhotoImage(self.resize_image1)
        self.image1_label_frame = Label(self.image_frame,image=self.image1)
        self.image1_label_frame.pack(pady=10,padx=10)

        self.button_frame_stock = tk.LabelFrame(self.frame)
        self.button_frame_stock.grid(row=1,column=0,padx=10,pady=50)

        self.stock_button = tk.Button(self.button_frame_stock,text="Register Stock",command=self.open_stock_window,
                                      height=2,width=25,background='grey')
        self.stock_button.grid(row=0,column=0)

        #self.button_frame_sales = tk.LabelFrame(self.frame,background='black')
        #self.button_frame_sales.grid(row=1,column=3,padx=10,pady=0)
        self.sales_button = tk.Button(self.button_frame_stock,text="Register Sale",command=self.open_sales_window,
                                      height=2,width=25,background='grey')
        self.sales_button.grid(row=0,column=1)

        #self.uttbon_frame_new_product = tk.LabelFrame(self.frame,background='black')
        #self.button_frame_new_product.grid(row=2,column=0,padx=2,pady=45)
        self.new_product_button = tk.Button(self.button_frame_stock,text="Register New Product",
                                            command=self.open_new_product_window,
                                      height=2,width=25,background='grey')
        self.new_product_button.grid(row=1,column=0)

        #self.button_frame_new_customer = tk.LabelFrame(self.frame,background='black')
        #self.button_frame_new_customer.grid(row=2,column=1,padx=10,pady=0)
        self.new_customer_button = tk.Button(self.button_frame_stock,text="Register New Customer",
                                            command=self.open_new_customer_window,
                                      height=2,width=25,background='grey')
        self.new_customer_button.grid(row=1,column=1)

        #self.button_frame_update_price = tk.LabelFrame(self.frame,background='black')
        #self.button_frame_update_price.grid(row=3,column=0,padx=10,pady=0)
        self.update_price_button = tk.Button(self.button_frame_stock,text="Update Price",
                         command=self.open_update_price_window,
                   height=2,width=25,background='grey')
        self.update_price_button.grid(row=2,column=0)

        self.config_padding(self.button_frame_stock,40,40)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()


    def config_padding(self,frame,x,y):
        for widget in frame.winfo_children():

            widget.grid_configure(padx=x, pady=y)
    def open_stock_window(self):
        StockManager()

    def open_update_price_window(self):
        UpdatePrice()

    def open_sales_window(self):
        SalesWindow()

    def open_new_product_window(self):
        NewProductWindow()

    def open_new_customer_window(self):
        RegisterNewCustomer()

    def on_closing(self):
        if messagebox.askyesno(title="Close",message="Do you want to close this window?"):
            self.root.destroy()


if __name__ == "__main__":
   Sales()