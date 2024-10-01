import sqlite3 as sql

def create_product_table():
    conn = sql.connect("C:\\Users\\vinic\\Documents\\Python\\Projeto_Loja\\project_store.db") #  conexão
    query = '''CREATE TABLE IF NOT EXISTS Product 
     (ID TEXT  PRIMARY KEY, Name TEXT, Type  TEXT, Bottle_Size INT, Unit TEXT)
       '''
    conn.execute(query)     # executa a query
    conn.close()
connection = sql.connect("C:\\Users\\vinic\\Documents\\Python\\Projeto_Loja\\project_store.db")
#connection.row_factory = sql.Row
#q = 'ALTER TABLE Product ADD COLUMN Time TEXT'

#print("a")
#cursor = connection.cursor()
#result = cursor.execute('select * from Product')
#names = result.fetchall()
#print(names)

def select_where():
    # passar where como string // x = y
    try:
        con = sql.connect("C:\\Users\\vinic\\Documents\\Python\\Projeto_Loja\\project_store.db")
        cursor = con.execute(f"SELECT * FROM Address WHERE ID = '360105321272402'")
        result = cursor.fetchall()
        return result
    except Exception as e:
        print('ERROR: ', e.args)

#for i in select_where("*","Unit = 'ml'"):
  #  print(i[0])
print(["0"]== [])


