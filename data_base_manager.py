import psycopg2
from setupDB import connect
class DatabaseManager:
    def __init__(self, host, port, user, password,db):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.db=db
    
    def connect(self):
        self.connection=connect()

    def disconnect(self):
        self.connection.close()
        
        
    def get_clients(self):
        self.connect()
        cursor=self.connection.cursor()
        cursor.execute('select id,nome_cliente from dim.cliente')
        clientes = cursor.fetchall()
        cursor.close()
        self.disconnect()
        return clientes
    
    def get_most_similar_client(self,client_id):
        self.connect()
        cursor=self.connection.cursor()
        cursor.execute(f'select id_cliente_destino from dim.cliente_similaridade where id_cliente_origem={client_id} order by similaridade DESC')
        clientes_por_similaridade=cursor.fetchone()
        cliente_mais_similar =  clientes_por_similaridade[0]
        cursor.close()
        self.disconnect()
        return cliente_mais_similar
    
    def get_products_from_similar_cliente(self,cliente_origem,cliente_destino):
        self.connect()
        cursor=self.connection.cursor()
        cursor.execute(f'select id_produto from dim.cliente_produto where id_cliente={cliente_origem}')
        produtos_origem=[produto[0] for produto in cursor.fetchall()]
        cursor.execute(f'select id_produto from dim.cliente_produto where id_cliente={cliente_destino}')
        produtos_destino=[produto[0] for produto in cursor.fetchall()]
        produtos_escolhidos_id=[produto for produto in produtos_destino if produto not in produtos_origem]
        produtos_escolhidos_id_string=','.join([f"'{item}'" for item in produtos_escolhidos_id])
        cursor.execute(f"select nome_produto from dim.produto where id in ({produtos_escolhidos_id_string})")
        produtos_escolhidos_nomes=[produto_nome[0] for produto_nome in cursor.fetchall()]
        cursor.close()
        self.disconnect()
        return produtos_escolhidos_nomes
       
    def get_two_most_popular_products(self):
        self.connect()
        cursor=self.connection.cursor()
        cursor.execute(f'select nome_produto from dim.produto order by likes_quant DESC')
        produtos_populares=[produto_nome[0] for produto_nome in cursor.fetchall()]
        self.disconnect()
        cursor.close()

        if len(produtos_populares)>=2: 
            return produtos_populares[:2]
        if len(produtos_populares)==1:
            return produtos_populares
        return None
    
    def add_like(self, produto_id):
        self.connect()
        cursor=self.connection.cursor()
        command=f'update dim.produto SET likes_quant=likes_quant+1 where id={produto_id}'
        print('linhas alteradas', cursor.execute(command))
        print('comando ', command)
        self.connection.commit()
        cursor.close()
        self.disconnect()


    def get_products(self):
        self.connect()
        cursor=self.connection.cursor()
        cursor.execute(f'select id, nome_produto,likes_quant from dim.produto order by likes_quant DESC')
        produtos=cursor.fetchall()
        cursor.close()
        self.disconnect()
        return produtos
    
    def get_products_from_client(self,id_client):
        self.connect()
        cursor=self.connection.cursor()
        cursor.execute(f'select id_produto from dim.cliente_produto where id_cliente={id_client}')
        produtos_cliente=[produto_id[0] for produto_id in cursor.fetchall()]
        self.disconnect()
        cursor.close()
        return produtos_cliente


