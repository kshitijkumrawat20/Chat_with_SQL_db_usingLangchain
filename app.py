import streamlit as st 
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


st.set_page_config(page_title="Chat with SQL Database Using LangChain", page_icon="🔍🦜")
st.title("Chat with SQL Database Using LangChain🦜🗄️🔎")

LOCALDB ="USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["Use SQLite3 Database-student.db", "connect to MySQL Database"]
selected_db = st.sidebar.radio(label="Choose the DB which you want to chat with", options=radio_opt)

if radio_opt.index(selected_db)==1:
    db_uri =MYSQL
    mysql_host = st.sidebar.text_input("Enter the MySQL Host")
    mysql_user = st.sidebar.text_input("Enter the MySQL user")
    mysql_password = st.sidebar.text_input("Enter the MySQL password", type="password")
    mysql_db = st.sidebar.text_input("Enter the MySQL database name")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input("Enter the Groq API Key", type="password")

if not api_key:
    st.info("Enter the API Key")

if not db_uri:
    st.info("Enter the DB URI")
    
llm = ChatGroq(api_key=api_key, model_name="llama-3.1-70b-versatile", streaming=True)

@st.cache_resource(ttl="2h")
def setup_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        db_path = (Path(__file__).parent/"STUDENT.db").absolute()
        print(db_path)
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator = creator))
    elif db_uri==MYSQL:
        if not(mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Enter the MySQL details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

if db_uri==MYSQL:
    db = setup_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = setup_db(db_uri)

toolkit = SQLDatabaseToolkit(db=db, llm = llm)
agent = create_sql_agent(
    llm = llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,handle_parsing_errors=True
    )
# creating a session state for the chat history
if "messages" not in st.session_state or st.sidebar.button("Reset chat history"):
    st.session_state["messages"]= [{"role":"Assistat","content":"you are an AI assitant that helps the user with their queries about the database. Please answer the user's questions about the database. Make sure the response should be fully informative and helpful, it should not be half descriptive"}]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    
user_query = st.chat_input(placeholder="ask about database")

if user_query:
    st.session_state.messages.append({"role":"user", "content":user_query})
    st.chat_message("user").write(user_query)
    
    # creating a callback to handle the response
    with st.chat_message("assistant"):
        streamlit_cb = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_cb])
        st.session_state.messages.append({"role":"assistant", "content":response})
        st.write(response)
