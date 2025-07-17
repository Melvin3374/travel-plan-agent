# Fichier : agent/travel_agent.py (version finale avec formatage explicite)

import os
from dotenv import load_dotenv

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

from database.postgres_db import get_langchain_db

# 1. Initialisations
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0, # On met 0 pour que l'agent soit plus déterministe et suive mieux les instructions
    convert_system_message_to_human=True
)
db = get_langchain_db()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# 2. PROMPT FINAL
template = """
Tu es un assistant de voyage IA expert et serviable. Tu dois répondre en français.
Tu as accès aux outils suivants pour aider l'utilisateur :

{tools}

Les noms des outils que tu peux utiliser sont : {tool_names}

---
**IMPORTANT : Pour utiliser un outil, tu dois utiliser le format EXACT suivant :**

Thought: La pensée de l'agent sur l'action à entreprendre.
Action: Le nom de l'outil à utiliser, qui doit être l'un de [{tool_names}].
Action Input: L'entrée pour l'outil.
Observation: Le résultat de l'outil.

**(Ce cycle Thought/Action/Action Input/Observation peut se répéter plusieurs fois)**

Quand tu as assez d'informations pour répondre, utilise le format suivant :

Thought: Je connais maintenant la réponse finale.
Final Answer: La réponse finale et complète à la question initiale de l'utilisateur.
---

Maintenant, commence !

Historique de la conversation :
{chat_history}

Question de l'utilisateur : {input}
Ta réflexion et tes actions (scratchpad) :
{agent_scratchpad}
"""

prompt = ChatPromptTemplate.from_template(template)

# 4. Création de la mémoire
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 5. Création de l'agent
agent = create_react_agent(llm, tools, prompt)

# 6. Création de l'Exécuteur de l'Agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True # Très utile pour gérer les petites erreurs de formatage
)

# 7. Fonction d'interaction principale
def get_response(user_input: str) -> str:
    response = agent_executor.invoke({"input": user_input})
    return response.get("output", "Désolé, je n'ai pas pu traiter votre demande.")