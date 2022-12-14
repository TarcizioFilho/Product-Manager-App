from tkinter import font, ttk
from tkinter import *
import sqlite3
from click import style
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Inicialização do SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_SQLAlchemy.db"
db.init_app(app)
#Fim da inicialização do SQLAlchemy

#Criação da tabela modelo da base de dados "database_SQLAlchemy.db"
class create_table_model(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    db.session.commit()
#Fim da criação da tabela modelo da base de dados "database_SQLAlchemy.db"
    
   
class product:
    
    # db recebe as bases de dados products ou database_SQLAlchemy.db, basta apenas passar o caminho da base de dados
    db = 'database/products.db'
    
    def __init__(self, root):
               
        self.window = root
        self.window.title("App Gestor de Produtos")
        self.window.resizable(1,1) # Ativa o redimensionamento
        self.window.wm_iconbitmap('resources/M6_P2_icon.ico')

        frame = LabelFrame(self.window, text= 'Register a New Product', font=('Calibri', 16, 'bold'))
        frame.grid(row=1, column=0, columnspan=3, pady=20)
        #label product Name
        self.label_name = Label(frame, text="Name ")
        self.label_name.grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()# Ao iniciar o programa a caixa de texto do nome já se encontra selecionada para digitar.
        self.name.grid(row=1, column=1)
        #label price
        self.label_price = Label(frame, text="Price ")
        self.label_price.grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)
        #botton save product
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.button_add = ttk.Button(frame, text="Save Product", style='my.TButton')
        self.button_add.grid(row=3, columnspan=3, sticky= W + E)
        #products table
        #table style
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) #modificar a fonte
        style.configure('mystyle.Treeview.Heading', font=('Calibri', 13, 'bold')) #Modificar fonte do cabeçalho
        style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea', {'sticky':'nswe'})]) #eliminar as bordas
        #table structure
        self.table = ttk.Treeview(height=10, columns=4, style="mystyle.Treeview")
        self.table.grid(row=4, column=0, columnspan=4)
        self.table.heading('#0', text='Name', anchor=CENTER) #Cabeçalho 0
        self.table.heading('#1', text='Price', anchor=CENTER) #Cabeçalho 1
        self.table.heading('#2', text='Quantity', anchor=CENTER) #Cabeçalho 2
        self.table.heading('#3', text='Category', anchor=CENTER) #Cabeçalho 3
    
if __name__ == '__main__':
    root = Tk() #Instancia da janela principal
    app = product(root)
    root.mainloop() #ciclo da aplicação, para mantê-la executando