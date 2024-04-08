import streamlit as  st
from data_base_manager import DatabaseManager
import config
import pandas as pd

db=DatabaseManager(
        host=config.databaseSuperUser['Server'],
        port=config.databaseSuperUser['port'],
        user=config.databaseSuperUser['Username'],
        password=config.databaseSuperUser['password'],
        db= config.databaseSuperUser['db']
    )

st.title("Sistemas de Recomendação")

clientes_dict={client[1]:client[0] for client in db.get_clients()}
cliente_nome=st.selectbox('Escolha um Cliente',[cliente for cliente in clientes_dict])
client_id=clientes_dict[cliente_nome]
similar_client_id=db.get_most_similar_client(client_id)

produtos_recomendados_similaridade=db.get_products_from_similar_cliente(client_id,similar_client_id)
produtos_populares=db.get_two_most_popular_products()
produtos_cliente=db.get_products_from_client(client_id)
produtos_recomendados=produtos_recomendados_similaridade+produtos_populares
produtos_recomendados=[produto for produto in produtos_recomendados if produto not in produtos_cliente]


df_produtos_recomendados=pd.DataFrame(produtos_recomendados, columns=['Produtos Recomendados'])
df_produtos_recomendados.drop_duplicates(inplace=True)
st.table(df_produtos_recomendados)

# Create a DataFrame
products_list=db.get_products()
df_product = pd.DataFrame(products_list, columns=['id','nome','likes'])
df_product.set_index('id', inplace=True)
# print(df_product)


st.header('Produtos mais populares')
# # Showproducts table 
colms = st.columns((1,1,1))
fields = ["ID","Curtidas","Curtir"]

for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)

likes=st.empty()
for i_, produto in df_product.iterrows():
    col1, col2,col3 = st.columns((1, 1, 1))
    col1.write(produto['nome'])  # index
    col2.write(produto['likes'])
    button_phold = col3.empty()  # create a placeholder
    do_action = button_phold.button(key=i_,label='Curtir')
    if do_action:
        id_produto_curtido=i_
        db.add_like(id_produto_curtido)
        st.rerun()
        st.info(f"O produto {produto['nome']} foi curtido")
        
  
 





