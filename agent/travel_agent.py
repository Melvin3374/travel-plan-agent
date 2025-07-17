# Fichier : agent/travel_agent.py (version corrigée)

import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain import hub
from database.postgres_db import get_langchain_db

load_dotenv()

# Ligne à modifier : on ajoute google_api_key
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GEMINI_API_KEY"), # <-- AJOUT IMPORTANT
    temperature=0.7,
    convert_system_message_to_human=True
)
db = get_langchain_db()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
prompt = hub.pull("hwchase17/react-chat")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

def get_response(user_input: str) -> str:
    response = agent_executor.invoke({"input": user_input})
    return response.get("output", "Désolé, je n'ai pas pu traiter votre demande.")