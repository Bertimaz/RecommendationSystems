import streamlit as st




connection_string=st.secrets['connection_string']

#legado - não usa mais, porém se tirar quebra.
databaseSuperUser={'Server':st.secrets['databaseSuperUser_server'],
                    'port':st.secrets['databaseport'],
                    'Username':st.secrets['databaseuser'],
                    'password':st.secrets['database_password'],
                    'db':st.secrets['db_name']
                    }

database=st.secrets['db_name']






