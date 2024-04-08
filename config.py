import streamlit as st


databaseSuperUser={'Server':st.secrets['databaseSuperUser_server'],
                    'port':st.secrets['databaseport'],
                    'Username':st.secrets['databaseuser'],
                    'password':st.secrets['database_password'],
                    'db':st.secrets['db_name']
                    }

database=st.secrets['db_name']

connection_string=st.secrets['connection_string']







