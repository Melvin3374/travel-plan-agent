# Fichier : agent/travel_agent.py (Correction de la faute de frappe)

import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from database.postgres_db import get_langchain_db

# 1. Initialisations
load_dotenv()
# --- CORRECTION DE LA FAUTE DE FRAPPE ICI ---
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
    convert_system_message_to_human=True
)
db = get_langchain_db()

# 2. Création des outils
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
db_tools = toolkit.get_tools()
search_tool = DuckDuckGoSearchRun(name="internet_search")
tools = db_tools + [search_tool]

# 3. LE PROMPT FINAL BASÉ SUR LE STANDARD LANGCHAIN
template = """
Tu es un assistant de voyage IA qui répond en français. Tu as accès aux outils suivants :

{tools}

Utilise le format suivant :

Question: la question initiale de l'utilisateur à laquelle tu dois répondre
Thought: tu dois toujours réfléchir à ce que tu vas faire
Action: l'action à entreprendre, doit être l'un des outils suivants [{tool_names}]
Action Input: l'entrée pour l'action
Observation: le résultat de l'action
... (ce cycle Thought/Action/Action Input/Observation peut se répéter)

Thought: Je connais maintenant la réponse finale
Final Answer: la réponse finale à la question initiale de l'utilisateur

Instructions importantes :
1. Pour les questions sur les voyages, consulte TOUJOURS la base de données en premier avec les outils `sql_db_...`.
2. Si un outil `sql_db_query` renvoie un résultat vide (comme `[]`), cela signifie que l'information n'est pas dans la base de données. Dans ce cas, tu dois immédiatement passer à l'outil `internet_search`. Ne relance jamais la même requête SQL.

Commençons !

Historique de la conversation :
{chat_history}

Question: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template)

# --- Le reste du fichier ne change pas ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=8,
    handle_parsing_errors=True
)

def get_response(user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input})
        return response.get("output", "Désolé, une erreur est survenue.")
    except Exception as e:
        print(f"Erreur dans l'AgentExecutor : {e}")
        return "Je suis désolé, je rencontre une difficulté technique pour traiter votre demande. Pourriez-vous essayer de reformuler ?"