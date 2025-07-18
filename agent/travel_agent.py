# Fichier : agent/travel_agent.py (Version finale avec outil personnalisé)

import os
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.tools import tool # Important : pour créer notre outil

# On importe notre nouvelle fonction "couteau suisse"
from database.postgres_db import get_info_for_city

# 1. Création de notre outil personnalisé
@tool
def travel_database_tool(city: str) -> str:
    """
    Utilise cet outil pour obtenir toutes les informations sur une ville,
    y compris les descriptions, vaccins, hôtels et activités.
    L'entrée doit être uniquement le nom de la ville.
    """
    return get_info_for_city(city)

# 2. Initialisations
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
    convert_system_message_to_human=True
)

# 3. Création de la liste d'outils
search_tool = DuckDuckGoSearchRun(name="internet_search")
tools = [travel_database_tool, search_tool] # Notre outil + la recherche web

# 4. Le Prompt final, simplifié
template = """
Tu es un assistant de voyage IA. Réponds en français. Tu as accès aux outils suivants :

{tools}

Utilise le format suivant :
Question: la question de l'utilisateur
Thought: tu dois réfléchir à ce que tu vas faire
Action: l'action à entreprendre, doit être l'un des outils suivants [{tool_names}]
Action Input: l'entrée pour l'action
Observation: le résultat de l'action
... (ce cycle peut se répéter)
Thought: Je connais maintenant la réponse finale
Final Answer: la réponse finale à la question

Instructions :
1. Pour toute question sur une ville, utilise TOUJOURS l'outil `travel_database_tool` en premier.
2. Si cet outil ne renvoie rien d'utile, utilise `internet_search`.

Commençons !

Historique : {chat_history}
Question: {input}
Scratchpad : {agent_scratchpad}
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
    max_iterations=6,
    handle_parsing_errors=True
)

def get_response(user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input})
        return response.get("output", "Désolé, une erreur est survenue.")
    except Exception as e:
        print(f"Erreur dans l'AgentExecutor : {e}")
        return "Je suis désolé, je rencontre une difficulté technique. Pourriez-vous reformuler ?"