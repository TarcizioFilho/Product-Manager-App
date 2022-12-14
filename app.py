from tkinter import ttk
import tkinter as tk
from tkinter import *
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Inicialização do SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_SQLAlchemy.db"
db.init_app(app)
#Fim da inicialização do SQLAlchemy

#Criar tabela modelo da base de dados "database_SQLAlchemy.db"
class create_table_model(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    db.session.commit()
#Fim de criar tabela modelo da base de dados "database_SQLAlchemy.db"
    
   
class product:
    
    # db recebe as bases de dados products ou database_SQLAlchemy.db, basta apenas passar o caminho da base de dados
    db = 'database/products.db'
    #db = 'instance/database_SQLAlchemy.db' 
    
    def __init__(self, root):
               
        self.window = root
        self.window.title("App Gestor de Produtos")
        self.window.resizable(1,1) # Ativa o redimensionamento
        self.window.wm_iconbitmap('resources/M6_P2_icon.ico')

        frame = LabelFrame(self.window, text= 'Register a New Product', font=('Calibri', 12, 'bold'))
        frame.grid(row=1, column=0, sticky=W, pady=10 )
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
        #label quantity
        self.label_quantity = Label(frame, text="Quantity ")
        self.label_quantity.grid(row=3, column=0)
        self.quantity = Entry(frame)
        self.quantity.grid(row=3, column=1)
        #label category
        self.label_category = Label(frame, text="Category ")
        self.label_category.grid(row=4, column=0)
        self.category = Entry(frame)
        self.category.grid(row=4, column=1)
        
        #botton save product
        s = ttk.Style()
        s.configure('TButton', font=('Calibri', 10, 'bold'))
        self.button_add = ttk.Button(frame, text="Save Product", command=self.add_product, style='TButton')
        self.button_add.grid(row=5, columnspan=2, sticky=E)
        
        
        #table style
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) #modificar a fonte
        style.configure('mystyle.Treeview.Heading', font=('Calibri', 10, 'bold')) #Modificar fonte do cabeçalho
        style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea', {'sticky':'nswe'})]) #eliminar as bordas
             
        #estrutura da tabela -> Cabeçalhos 
        self.table = ttk.Treeview(self.window ,height=10, columns=('#1','#2','#3'), style="mystyle.Treeview")
        self.table.grid(row=4, column=0, columnspan=7)
        self.table.heading('#0', text='Name', anchor=CENTER) #Cabeçalho 0
        self.table.heading('#1', text='Price', anchor=CENTER) #Cabeçalho 1
        self.table.heading('#2', text='Quantity', anchor=CENTER) #Cabeçalho 2
        self.table.heading('#3', text='Category', anchor=CENTER) #Cabeçalho 3
        
        #Scroll Vertical 
        yscrollbar = ttk.Scrollbar(self.table, orient='vertical', command=self.table.yview)
        yscrollbar.place(x=780, y=1, height=220)
        
        self.table.configure(yscrollcommand=yscrollbar.set)
        #Fim Scrol Vertical
        
        self.get_products()
        
        #mensagem informativo para o utilizador
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W, ipadx=30, ipady=10)
        
        #Frame da caixa ações
        frame_actions = LabelFrame(self.window, text= 'Actions', font=('Calibri', 12, 'bold'))
        frame_actions.grid(row=1, column=1,ipady=28)
        
        #Botões eliminar e editar o produto
        s = ttk.Style()
        s.configure('TButton', font=('Calibri', 10, 'bold'))
        self.delete_button = ttk.Button(frame_actions, text='Delete', command= self.modal_delete_confirmation, style='TButton')
        self.delete_button.grid(row=3, column=1)
        self.edit_button = ttk.Button(frame_actions, text="Edit", command=self.edit_product, style='TButton')
        self.edit_button.grid(row=2, column=1)
        #Fim Botões eliminar e editar o produto
        
    #Método para conectar, criar cursor e executar ações no banco de dados através dos parametros informados   
    def db_query(self, query, parameters=()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters) #receber os paramentro para serem consultados na database
            conn.commit()#executar a consulta
        return result
    
    def get_products(self):
        # Ao iniciar o programa, irá limpara a tabela se tiver dados residuais ou antigos
        table_records = self.table.get_children()
        for data in table_records:
            self.table.delete(data)
        
        #SQL query
        query ='SELECT * FROM product ORDER BY Name DESC'
        db_records = self.db_query(query) #chamar o método de consulta
        
        #Mostrar dados no ecrã
        for data in db_records:
            self.table.insert('', 0, text=data[1] ,values=(data[2], data[3], data[4]))
            
    #validar nome
    def validate_name(self):
        name_entered_by_user = self.name.get()
        return len(name_entered_by_user) != 0
    
    #validar preço
    def validate_price(self):
        price_entered_by_user = self.price.get()
        return len(price_entered_by_user) != 0
    
    #validar quantidade
    def validate_quantity(self):
        quantity_entered_by_user = self.quantity.get()
        return len(quantity_entered_by_user) != 0
    
    #validar categoria
    def validate_category(self):
        category_entered_by_user = self.category.get()
        return len(category_entered_by_user) != 0
    
    #adicionar produto
    def add_product(self):
        if self.validate_name() and self.validate_price() and self.validate_quantity() and self.validate_category():
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?, ?)' # consulta database sem os daddos
            parameters = (self.name.get(), self.price.get(), self.quantity.get(), self.category.get()) # parametros que irão para o método db_query(consulta database)
            self.db_query(query, parameters)
            self.message['text'] = 'Product {} added successfully.'.format(self.name.get())
            self.name.delete(0, END) #apagar o campo nome do formulário
            self.price.delete(0, END) #apagar o campo nome do formulário
            self.quantity.delete(0, END) #apagar o campo nome do formulário
            self.category.delete(0, END) #apagar o campo nome do formulário
            # Para o debug
            #print(self.nome.get())
            #print(self.preço.get())
        else:
            print('Please fill all blanks')
            self.message['text'] = 'Please fill all blanks'
        
        self.get_products()# invocar o método para que o produto aparecça no ecrã do programa.
    
    #modal de confirmação e excluir ou cancelar ação de excluir o produto
    def modal_delete_confirmation(self):
        self.message['text'] = ''
        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select a product.'
            return
        
        #criação da janela de confirmação para deletar o produto
        self.edit_window = Toplevel() 
        self.edit_window.title = 'Delete Product'
        self.edit_window.resizable(1, 1)
        self.edit_window.wm_iconbitmap('resources/M6_P2_icon.ico')
        
        #criação do recipiente frame da janela de confirmaão para deletar o produto
        rep_frame = LabelFrame(self.edit_window, font=('Calibri', 14, 'bold'))
        rep_frame.grid(row=1, column=0, pady=30)
        #label confirmação de exclusão do produto
        self.label_confirmation = Label(rep_frame, text='Delele this Product? ', font=('Calibri', 10), pady=10)
        self.label_confirmation.grid(row=1, column=0, columnspan=5)
        
        #botão de confirmação para excluir o produto
        s = ttk.Style()
        s.configure('TButton', font=('Calibri', 10, 'bold'))
        self.confirm_button = ttk.Button(rep_frame, text='Confirm', command= self.delete_product,style='TButton')
        self.confirm_button.grid(row=6, column=0)
        #Botão cancelar 
        self.cancel_button = ttk.Button(rep_frame, text='Cancel', command= self.edit_window.destroy ,style='TButton')
        self.cancel_button.grid(row=6, column=1)
        #Fim do modal de confirmação e excluir ou cancelar ação de excluir o produto
        
    #Deletar o produto
    def delete_product(self):
        #debug - Teste para verificar se a informação a ser deletada está correta
        #print(self.table.item(self.table.selection()))
        #print(self.table.item(self.table.selection())['text'])
        #print(self.table.item(self.table.selection())['values'])
        #print(self.table.item(self.table.selection())['values'][0])  
        
        self.message['text'] = ''
        name =  self.table.item(self.table.selection())['text']
        query = 'DELETE FROM product WHERE name = ?' #Consulta database
        self.db_query(query, (name,)) #executar consulta e eliminar
        self.edit_window.destroy()
        self.message['text'] = 'Product {} has been deleted successfully'.format(name)
        self.get_products() #atualizar tabela e mostrar no ecrã
    #Fim de deletar produto
    
    #Editar produto
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select a product.'
            return
        
        name = self.table.item(self.table.selection())['text']
        old_price = self.table.item(self.table.selection())['values'][0]
        old_quantity = self.table.item(self.table.selection())['values'][1]
        old_category = self.table.item(self.table.selection())['values'][2]
               
        #criação da janela editar produto
        self.edit_window = Toplevel() 
        self.edit_window.title = 'Edit Product'
        self.edit_window.resizable(1, 1)
        self.edit_window.wm_iconbitmap('resources/M6_P2_icon.ico')
               
        #criação do recipiente frame da janela editar produto
        rep_frame = LabelFrame(self.edit_window, text='Edit Product', font=('Calibri', 12, 'bold'))
        rep_frame.grid(row=1, column=0, columnspan=20, pady=20)
        #label nome antigo
        self.old_label_name = Label(rep_frame, text='Current Name: ', font=('Calibri', 12))
        self.old_label_name.grid(row=2, column=0)
        #Entrada do nome antigo(para ter como referencia)
        self.old_name_input = Entry(rep_frame, textvariable=StringVar(self.edit_window, value=name), state='readonly', font=('Calibri', 12))
        self.old_name_input.grid(row=2,column=1)
        
        #label Nome novo
        self.new_name = Label(rep_frame, text='New Name: ', font=('Calibri', 12))
        self.new_name.grid(row=2, column=2)
        #entrar com o novo nome do produto
        self.new_name_input = Entry(rep_frame, font=('Calibri', 12))
        self.new_name_input.grid(row=2,column=3)
        self.new_name.focus()
        
        #label preço antigo
        self.old_label_price = Label(rep_frame, text='Current Price: ', font=('Calibri', 12))
        self.old_label_price.grid(row=3, column=0)
        #Entrada com o preço antigo, para ter como referencia no ecrã
        self.old_price_input = Entry(rep_frame, textvariable=StringVar(self.edit_window, value=old_price),state='readonly',font=('Calibri', 12))
        self.old_price_input.grid(row=3, column=1)
        
        #label preço novo
        self.new_price_label = Label(rep_frame, text='New Price: ', font=('Calibri', 12))
        self.new_price_label.grid(row=3, column=2)
        #entrar com novo preço 
        self.new_price_input = Entry(rep_frame, font=('Calibri', 12))
        self.new_price_input.grid(row=3, column=3)
        
        #label Quantidade antiga
        self.old_label_quantity = Label(rep_frame, text='Current Quantity: ', font=('Calibri', 12))
        self.old_label_quantity.grid(row=4, column=0)
        #Entrada da quantidade antiga, para ter como referencia no ecrã
        self.old_quantity_input = Entry(rep_frame, textvariable=StringVar(self.edit_window, value=old_quantity),state='readonly',font=('Calibri', 12))
        self.old_quantity_input.grid(row=4, column=1)
        
        #label nova quantidade
        self.new_quantity_label = Label(rep_frame, text='New Quantity: ', font=('Calibri', 12))
        self.new_quantity_label.grid(row=4, column=2)
        #entrar com nova quantidade
        self.new_quantity_input = Entry(rep_frame, font=('Calibri', 12))
        self.new_quantity_input.grid(row=4, column=3)
        
        #label categoria antiga
        self.old_label_category = Label(rep_frame, text='Current Category: ', font=('Calibri', 12))
        self.old_label_category.grid(row=5, column=0)
        #Entrada do nome antigo(para ter como referencia)
        self.old_category_input = Entry(rep_frame, textvariable=StringVar(self.edit_window, value=old_category), state='readonly', font=('Calibri', 12))
        self.old_category_input.grid(row=5,column=1)
        
        #label Nome novo
        self.new_category = Label(rep_frame, text='New Category: ', font=('Calibri', 12))
        self.new_category.grid(row=5, column=2)
        #entrar com o novo nome do produto
        self.new_category_input = Entry(rep_frame, font=('Calibri', 12))
        self.new_category_input.grid(row=5,column=3)
        
        #botão atualizar produto
        s = ttk.Style()
        s.configure('TButton', font=('Calibri', 12, 'bold'))
        self.update_button = ttk.Button(rep_frame, text='Confirm', command=lambda:self.update_product(self.new_name_input.get(),
        self.old_name_input.get(), 
        self.new_price_input.get(),
        self.old_price_input.get(),
        self.new_quantity_input.get(),
        self.old_quantity_input.get(),
        self.new_category_input.get(),
        self.old_category_input.get()),style='TButton')
        self.update_button.grid(row=8, columnspan=2, sticky=W)
        #Botão cancelar edição do produto
        self.cancel_button = ttk.Button(rep_frame, text='Cancel', command= self.edit_window.destroy ,style='TButton')
        self.cancel_button.grid(row=8, column=1, sticky=E)
    
    #Método para atualizar valores na base de dados     
    def update_product(self, new_name, old_name, new_price, old_price, new_quantity, old_quantity, new_category, old_category):
        product_modified = False
        query = 'UPDATE product SET name = ?, price = ?, quantity = ?, category = ? WHERE name = ? AND price = ? AND quantity = ? AND category = ?'
        #se o utilizador altrera o nome e o preço, então ambos serão atualizados
        if new_name != '' and new_price != '' and new_quantity != '' and new_category != '':
            parameters = (new_name, new_price,new_quantity,new_category, old_name, old_price, old_quantity, old_category)
            product_modified = True
        #regra para alterar os campos individualmente
        elif new_name != '' and new_price == '' and new_quantity == '' and new_category == '':
            parameters = (new_name, old_price, old_quantity, old_category, old_name , old_price, old_quantity, old_category)
            product_modified = True
        elif new_price != '' and new_name == '' and new_quantity == '' and new_category == '':
            parameters = (old_name, new_price, old_quantity, old_category, old_name , old_price, old_quantity, old_category)
            product_modified = True
        elif new_quantity != '' and new_price == '' and new_name == '' and new_category == '':
            parameters = (old_name, old_price, new_quantity, old_category, old_name , old_price, old_quantity, old_category)
            product_modified = True
        elif new_category != '' and new_price == '' and new_quantity == '' and new_name == '':
            parameters = (old_name, old_price, old_quantity, new_category, old_name , old_price, old_quantity, old_category)
            product_modified = True
        
        if product_modified:
            self.db_query(query, parameters) #executar a consulta
            self.edit_window.destroy() #fechar janela de edição de produtos
            self.message['text'] = 'Product has been updated.' #mensagem de atualização do produto ao usuário
            self.get_products()#atualizar a tabela no ecrã do programa
        else:
            self.edit_window.destroy() #Fechar janela de edição de produtos
            self.message['text'] = 'Product has NOT updated.' #mesagem ao utilizador, produto não atualizado
            self.get_products()#atualizar a tabela no ecrã do programa


if __name__ == '__main__':
    root = Tk() #Instancia da janela principal
    app = product(root)
    root.mainloop() #ciclo da aplicação, para mantê-la executando

    
    