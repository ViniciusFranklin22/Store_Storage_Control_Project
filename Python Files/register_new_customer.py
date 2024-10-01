import tkinter as tk
from tkinter import ttk  #temas do tkinter, mais mordenos
from tkinter import messagebox
from datetime import date
import re
from eng_dados import Data_Eng

class RegisterNewCustomer:
    def __init__(self):
        self.table_name = "Customer"
        self.data = Data_Eng(self.table_name)

        self.root = tk.Tk()
        self.root.title("Register New Customer")

        self.frame = tk.Frame(self.root)  # dentro da janela, root é o parente
        self.frame.pack()

        # inicia o primeiro label 1x1
        self.user_info_frame = tk.LabelFrame(self.frame, text="Customer Information")
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=10)

        self.first_name_label = tk.Label(self.user_info_frame, text="First Name")
        self.first_name_label.grid(row=0, column=0)
        self.first_name_entry = tk.Entry(self.user_info_frame)
        self.first_name_entry.grid(row=1, column=0)

        self.last_name_label = tk.Label(self.user_info_frame, text="Last Name")
        self.last_name_label.grid(row=0, column=1)
        self.last_name_entry = tk.Entry(self.user_info_frame)
        self.last_name_entry.grid(row=1, column=1)

        self.title_label = tk.Label(self.user_info_frame, text="Title")
        self.titles = ["", "Sr.", "Sra.", "Dr."]
        self.title_combobox = ttk.Combobox(self.user_info_frame, values=self.titles)  # abas para escolha
        self.title_label.grid(row=0, column=2)
        self.title_combobox.grid(row=1, column=2)

        self.date_of_birth_label = tk.Label(self.user_info_frame, text="Date of Birth (DD/MM/YYYY)")
        self.date_of_birth_entry = tk.Entry(self.user_info_frame)  # box com os valores
        self.date_of_birth_label.grid(row=2, column=0)
        self.date_of_birth_entry.grid(row=3, column=0)

        self.cell_phone_label = tk.Label(self.user_info_frame, text="Cell Phone")
        self.cell_phone_label.grid(row=2, column=1)
        self.cell_phone_entry = tk.Entry(self.user_info_frame)
        self.cell_phone_entry.grid(row=3, column=1)

        self.cpf_label = tk.Label(self.user_info_frame,text="CPF (XXXXXXXXX-XX)")
        self.cpf_label.grid(row=2,column=2)
        self.cpf_entry = tk.Entry(self.user_info_frame)
        self.cpf_entry.grid(row=3,column=2)


        self.config_padding(self.user_info_frame,10,10)

        #inicia o 3 label 2x1

        self.terms_frame = tk.LabelFrame(self.frame, text="Terms & Conditions")
        self.terms_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

        self.check_terms_state = tk.IntVar()
        self.terms_checkstate = tk.Checkbutton(self.terms_frame, text="I accept the terms and conditions",variable=self.check_terms_state)
        self.terms_checkstate.grid(row=1, column=0)

        self.button = tk.Button(self.frame, text="Enter Data", command=self.enter_data)
        self.button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # ação ao fechar a janela
        self.root.mainloop()

    def config_padding(self,frame,x,y):
        for widget in frame.winfo_children():
            widget.grid_configure(padx=x, pady=y)

    def check_user_registrition(self):
        where = f"CPF = '{self.get_cpf()}'"
        value=self.data.select_where('CPF', where)
        print(value)
        if len(value) != 0:
            messagebox.showwarning(title="Error", message="User already registered")
            return False
        else:
            return True

    def get_date_format(self):
        if self.check_date_format():
            value = self.get_date_of_birth().replace(" ", "").replace("/", "")
            values = f'{value[4:]}-{value[2:4]}-{value[0:2]}'
            return values

    def enter_data(self):
        if self.check_fields() and self.check_date_format() and self.check_user_registrition():
            values = [self.get_cpf(),self.get_title(),self.get_first_name(),self.get_last_name(),self.get_date_format(),self.get_cell_phone(),self.get_terms_state()]
            status = self.data.insert_data(values=values)
            if status[0] == "Succesfull":
                messagebox.showinfo(title="Data Registration", message="Your information has been submitted")
            else:
                messagebox.showwarning(title="Error", message="Internal Error")
            self.clear()


    def check_date_format(self):

        value = self.get_date_of_birth().replace(" ","").replace("/","")
        compair = re.sub('[a-z]',"",value)

        if len(value) > 0 and value == compair and len(value) == 8 and int(value[0:2]) <= 31 and int(value[2:4]) <= 12:
            if (int(str(date.today())[0:4]) - int(value[4:])) > 17:
                return True
            else:
                messagebox.showwarning(title="Error",message="The Customer must be 18 or older")
                return False
        else:
            messagebox.showwarning(title="Error", message="Fill the Date field according to the pattern \nDD/MM/YYYY")
            return False



    def check_fields(self):
        compair = re.sub('[a-z]',"",self.get_cpf())
        if self.get_first_name() != '' and self.get_last_name() != '' and len(self.get_cell_phone()) >= 8 and self.get_title() != '' and self.check_terms_state != 0:
            if self.get_cpf() == compair and len(self.get_cpf())== 12 and self.get_cpf()[9]=='-':
                return True
            else:
                messagebox.showwarning(title="Error",message="Fill the CPF field according to the pattern \nXXXXXXXXX-XX")
                return False
        else:
            messagebox.showwarning(title="Error", message="Please fill all the fields")
            return False

    def get_first_name(self):
        return self.first_name_entry.get().strip()

    def get_last_name(self):
        return self.last_name_entry.get().replace(" ","")

    def get_title(self):
        return self.title_combobox.get().replace(" ","")

    def get_cell_phone(self):
        return re.sub("[A-Z]","",re.sub("[a-z]","",self.cell_phone_entry.get().replace(" ","").replace("-","")))

    def get_date_of_birth(self):
        return self.date_of_birth_entry.get().replace(" ","")

    def get_cpf(self):
        return self.cpf_entry.get().replace(" ","")

    def get_terms_state(self):
        return self.check_terms_state.get()

    def on_closing(self):
        if messagebox.askyesno(title="Close",message="Do you want to close this window?"):
            self.root.destroy()

    def clear(self):
        self.first_name_entry.delete(0,tk.END)
        self.last_name_entry.delete(0,tk.END)
        self.title_combobox.delete(0,tk.END)
        self.date_of_birth_entry.delete(0,tk.END)
        self.cell_phone_entry.delete(0,tk.END)
        self.cpf_entry.delete(0,tk.END)
        self.terms_checkstate.deselect()


if __name__ == '__main__':
    RegisterNewCustomer()

