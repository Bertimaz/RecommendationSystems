import pandas as pd

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config
import json
from dados.clientes import clientes

def connect():
    #  print(config.connection_string)
     connection = psycopg2.connect(config.connection_string)
     return connection
    

class DatabaseManager:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def read_file(self,file_path):
        with open(r'dados\01_DataSetOpenFinance.txt', 'r') as file:
            content = file.read()
            clientes_from_file = eval(content)
            
        return clientes_from_file
    
    def create_database(self, dbname):
        self.db=dbname
        # Connect to PostgreSQL (template1 database) to create a new database
        connection=connect()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()

        # Use the psycopg2.sql.SQL class to create the database for safer SQL string formatting
        create_db_query = sql.SQL("CREATE DATABASE  {}").format(
            sql.Identifier(dbname)
        )
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateDatabase:
            print(f'{dbname} already exists')
            pass
                # Connect to PostgreSQL (template1 database) to create a new database
        connection=connect()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()


        create_db_query = sql.SQL(" CREATE SCHEMA fato"
        )
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateSchema:
            print('Schema Fato already exists')
            pass  

        #Create Schem dim
        create_db_query = sql.SQL(" CREATE SCHEMA dim"
        )
        try:
            # Execute the SQL command to create the new database
            cursor.execute(create_db_query)
        except psycopg2.errors.DuplicateSchema:
            print('Schema dim already exists')
            pass  

         # Create Table cliente
        print('Creating table dim.cliente')
        create_db_query = sql.SQL("CREATE TABLE dim.cliente ("
            " ID SERIAL PRIMARY KEY,"
            " nome_cliente varchar(255)"
            ")" 
        )  
        try:
            # Execute the SQL command to create the table dim.cliente
            cursor.execute(create_db_query)
            print('table dim.cliente created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.cliente already exists')
           
        except Exception as e:
            print(f'Unkown Error: {e}')

       # Create Table produto
        print('Creating table dim.produto')
        create_db_query = sql.SQL("CREATE TABLE dim.produto ("
            " ID SERIAL PRIMARY KEY,"
            " nome_produto varchar(255),"
            " likes_quant int"
            ")" 
        )  
        try:
            # Execute the SQL command to create the table dim.cliente
            cursor.execute(create_db_query)
            print('table dim.produto created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.produto already exists')
           
        except Exception as e:
            print(f'Unkown Error: {e}')

         # Create Table cliente produto
        print('Creating table dim.cliente_produto')
        create_db_query = sql.SQL("CREATE TABLE dim.cliente_produto ("
            " ID_cliente INT REFERENCES dim.cliente(ID),"
            " ID_produto INT REFERENCES dim.produto(ID),"
            "valor int"
            ")" 
        )  
        try:
            # Execute the SQL command to create the table dim.cliente_produto
            cursor.execute(create_db_query)
            print('table dim.clienteProduto created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.cliente_pdotuto already exists')
           
        except Exception as e:
            print(f'Unkown Error: {e}')


         # Create Table cliente cliente_similiridade
        print('Creating table dim.cliente_similaridade')
        create_db_query = sql.SQL("CREATE TABLE dim.cliente_similaridade ("
            " ID_cliente_origem INT REFERENCES dim.cliente(ID),"
            " ID_cliente_destino INT REFERENCES dim.cliente(ID),"
            "similaridade FLOAT"
            ")" 
        )  
        try:
            # Execute the SQL command to create the table dim.cliente_produto
            cursor.execute(create_db_query)
            print('table dim.clienteProduto created')
        except psycopg2.errors.DuplicateTable:
            print('table dim.cliente_pdotuto already exists')
           
        except Exception as e:
            print(f'Unkown Error: {e}')
        # Close the cursor and connection
        cursor.close()
        connection.close()


    def insert_client(self,id,client_name):
        # Connect to PostgreSQL (template1 database) to create a new database
        connection=connect()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()

        cursor.execute(f"insert into dim.cliente(ID,nome_cliente) VALUES({id},'{client_name}')")

        # Close the cursor and connection
        cursor.close()
        connection.close()

    def insert_produtos(self):
        # Connect to PostgreSQL (template1 database) to create a new database
        connection=connect()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        print(connection.get_dsn_parameters()["dbname"])

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()
        self.produto={1:'Cartão de Crédito',2: 'Conta Corrente',3:'Crédito Pessoal',4:'Poupança',5:'Renda Fixa',6:'Renda Variável'}
        self.produto_invertido={'Cartão de Crédito':1,'Conta Corrente':2,'Crédito Pessoal':3,'Poupança':4,'Renda Fixa':5,'Renda Variável':6}
        for id in self.produto:
            cursor.execute(f"insert into dim.produto(ID,nome_produto, likes_quant) VALUES({id},'{self.produto[id]}',0)")

        # Close the cursor and connection
        cursor.close()
        connection.close()


    def insert_cliente_produtos(self,id_cliente, id_produto, valor):
        # Connect to PostgreSQL (template1 database) to create a new database
        connection=connect()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object to execute SQL commands
        cursor = connection.cursor()
        cursor.execute(f"insert into dim.cliente_produto(ID_cliente,ID_produto,valor) VALUES({id_cliente},{id_produto},{valor})")

        # Close the cursor and connection
        cursor.close()
        connection.close()


    def insert_data(self):
        self.insert_produtos()
        id=1
        for cliente in clientes:
            self.insert_client(id,cliente)
            for produto in clientes[cliente]:
                id_produto=self.produto_invertido[produto]
                valor=clientes[cliente][produto]
                self.insert_cliente_produtos(id,id_produto,valor)
            id+=1


if __name__ == "__main__":
    db_manager = DatabaseManager(
        host=config.databaseSuperUser['Server'],
        port=config.databaseSuperUser['port'],
        user=config.databaseSuperUser['Username'],
        password=config.databaseSuperUser['password']
    )

    db_manager.create_database('recommendationsSystems')

    print("Database 'recomendationSystems' created successfully.")

    db_manager.insert_data()

    print('Data Inserted')

