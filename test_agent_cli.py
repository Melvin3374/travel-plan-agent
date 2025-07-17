# Fichier : test_agent_cli.py
from agent.travel_agent import get_response
import warnings

# On ignore les avertissements de dépréciation de LangChain pour un affichage plus propre
warnings.filterwarnings("ignore")

print("🤖 Agent de voyage activé. Tapez 'exit' pour quitter.")
print("---")

while True:
    try:
        user_input = input("Vous: ")
        if user_input.lower() == 'exit':
            break
        
        # Appel de la fonction principale de l'agent
        response = get_response(user_input)
        print(f"Assistant: {response}")
        print("---")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        break