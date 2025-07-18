# Fichier : agent/travel_agent.py (Version finale et stable)

import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits import SQLDatabaseToolkit # type: ignore
from langchain.agents import AgentExecutor, create_react_agent # type: ignore
from langchain_community.tools import DuckDuckGoSearchRun # type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
from langchain.memory import ConversationBufferMemory # type: ignore
from langchain.prompts import ChatPromptTemplate # type: ignore

from database.postgres_db import get_langchain_db

# 1. Initialisations
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
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

# 3. LE PROMPT FINAL ET ROBUSTE
template = """
Tu es un assistant de voyage IA. Réponds en français. Tu as accès à des outils.

Voici les outils que tu peux utiliser :
{tools}

**Utilise le format EXACT suivant pour répondre :**

Thought: Tu dois toujours réfléchir à ce que tu vas faire.
Action: L'action à entreprendre. Doit être l'un des outils suivants : [{tool_names}].
Action Input: L'entrée pour l'action. Pour un outil qui ne nécessite pas d'entrée comme `sql_db_list_tables`, utilise deux guillemets vides comme ceci : "".
Observation: Le résultat de l'action.

...(ce cycle Thought/Action/Action Input/Observation peut se répéter)...

Thought: Je connais maintenant la réponse finale.
Final Answer: La réponse finale et complète à la question de l'utilisateur.

**Instructions importantes :**
1. Pour les questions sur les voyages, consulte TOUJOURS la base de données en premier avec les outils `sql_db_...`.
2. Si la base de données ne renvoie rien d'utile, utilise `internet_search`.

Commençons !

Historique de la conversation :
{chat_history}

Question : {input}
Scratchpad :
{agent_scratchpad}
"""

prompt = ChatPromptTemplate.from_template(template)

# --- Le reste du fichier ne change pas ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    max_iterations=8, # On augmente un peu pour lui laisser le temps de se corriger
    handle_parsing_errors=True
)

def get_response(user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input})
        return response.get("output", "Désolé, une erreur est survenue.")
    except Exception as e:
        # Gérer les erreurs de manière plus gracieuse
        print(f"Erreur dans l'AgentExecutor : {e}")
        return "Je suis désolé, je rencontre une difficulté technique pour traiter votre demande. Pourriez-vous essayer de reformuler ?"