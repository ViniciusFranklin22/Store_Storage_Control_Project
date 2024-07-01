import sqlite3 as sql
from datetime import date
from threading import Lock
from datetime import datetime

DB_PATH = "C:\\Users\\vinic\\Documents\\Python\\Projeto_Loja\\project_store.db"


class Data_Eng:
    def __init__(self,table_name):
        self.table_name = table_name
        self.db_path = DB_PATH
        self.con = sql.connect(self.db_path, check_same_thread=False)
        self.cursor = self.con.cursor()
        self.columns = self.get_columns
        self.lock = Lock()

    def get_columns(self,case='1'):

        try:
            cursor = self.con.execute(f'SELECT * FROM {self.table_name if case == "1" else case}')
            return list(map(lambda x: x[0], cursor.description))
        except Exception as e:
            print('ERROR: ',e.args)


    def select_where(self,columns,where,case='1'):
        #passar where como string // x = y
        # retorna uma lista de tuplas

        try:

            cursor = self.con.execute(f'SELECT {columns} FROM {self.table_name if case == "1" else case} WHERE {where}')
            result = cursor.fetchall()
            return result
        except Exception as e:
            print('ERROR: ',e.args)



    def select(self,columns,case='1'):
        #retorna uma lista de tuplas

        try:

            cursor = self.con.execute(f'SELECT {columns} FROM {self.table_name if case == "1" else case}')
            result = cursor.fetchall()
            return result
        except Exception as e:
            print('ERROR: ',e.args)


    def define_id(self,values="",case="1"):
        if self.table_name == 'Product':
            id = ''
            for i in range(0,4):
                print(i)
                id += str(values[i])[0:3]
            print(id)
            return id
        elif self.table_name == "Address" or case == "Address":
            return str(values[0])+str(values[3])+values[4]

        else:
            query = f'SELECT MAX(ID) FROM {self.table_name if case == "1" else case}'
            try:
                self.lock.acquire()
                self.cursor.execute(query)
                records = self.cursor.fetchall()
                print(records[0][0])
                if records[0][0] is None:
                    id = 1
                else:
                    id = str(int(records[0][0]) + 1)
                self.lock.release()

                return id
            except Exception as e:
                print("Error", e.args)

    def update_data(self,columns_update,where,case="1"):
        update_query = f"UPDATE {self.table_name if case =='1' else case} SET {columns_update} WHERE {where}"
        try:
            self.lock.acquire()
            self.cursor.execute(update_query)
            self.con.commit()
            self.lock.release()
            return "Succesfull"
        except Exception as e:
            print("Error: ",e.args)
            return f"Erro: {e.args}"


    def insert_data(self,values,case="1",send_id="2"):
        cols = ''

        for x in self.get_columns(case=case):
            cols = cols +'"' + str(x) +'"'  + ', '
        col_values = ''
        for x in values:
            col_values = col_values + '"' + str(x) +'"' + ', '
        id = send_id if send_id != "2" else (self.define_id(values,case="1" if case == "1" else case))
        data_insert = f'''INSERT INTO {self.table_name if case == "1" else case} ({cols[:-2]}  ) VALUES ( "{id}", {col_values[:-2]},
                           '{date.today()}','{datetime.now().strftime('%H:%M:%S')}'  )'''
        print(data_insert)


        try:
            self.lock.acquire()
            self.cursor.execute(data_insert)
            self.con.commit()
            self.lock.release()
            return ["Succesfull",id]
        except Exception as e:
            print("Error: ",e.args)
            return f"Erro: {e.args}"





