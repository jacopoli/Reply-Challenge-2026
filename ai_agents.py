import json
import google.generativeai as genai
from config import GOOGLE_API_KEY
from pending_requests import add_pending_request, get_due_requests, generate_resolution_narrative
from banking_products import BANKING_OFFERS, SAVINGS_PRODUCTS, CREDIT_PRODUCTS

# Configuration initiale de Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# On utilise "gemini-2.5-flash" pour la vitesse (idéal pour du temps réel)
# Si tu veux plus de raisonnement complexe, utilise "gemini-2.5-pro"
model = genai.GenerativeModel('gemini-2.5-flash')

# --- AGENT 1 : LE NARRATEUR ---
def get_narrator_response(user_input, game_state_json):
    system_prompt = f"""
    Tu es le Maître du Jeu d'une simulation de vie financière (RPG).
    
    ÉTAT ACTUEL DU JOUEUR :
    {game_state_json}

    ACTION DU JOUEUR : "{user_input}"

    TES DIRECTIVES :
    1. Analyse l'action (vérifie s'il a l'argent dans 'balance').
    2. Si l'action est impossible (fonds insuffisants), refuse-la poliment dans la narration.
    3. Si possible, génère une réponse narrative immersive (courte).
    4. Calcule les impacts mathématiques (updates) : TOUT peut être modifié (salaire, loyer, balance, stress, fun).
    5. Calcule les NOUVELLES stats après application de TOUS les changements
    6. Si l'action est une DEMANDE (augmentation, prêt, formation), ajoute un champ "pending_request" au JSON avec:
       - type: le type de demande
       - description: description courte
       - resolution_months: nombre de mois avant résolution (1-3 généralement)
    
    IMPORTANT : Tu DOIS modifier le salaire et le loyer directement dans 'updates' si l'action le demande !
    Exemples :
    - "Je quitte mon travail" → salary_change: -1800 (tu perds ton salaire)
    - "Je déménage" → rent_change: +300
    - "Je trouve un CDI mieux payé" → salary_change: +500

    Tu dois répondre UNIQUEMENT avec ce schéma JSON :
    {{
        "narrative": "Texte de ce qui se passe...",
        "updates": {{
            "balance_change": 0,
            "stress_change": 0,
            "inventory_add": null,
            "salary_change": 0 (changement du salaire mensuel, ex: +500)
            "rent_change": 0 (changement du loyer, ex: -100)
        }},
        "pending_request": null ou {{
            "type": "augmentation",
            "description": "Demande d'augmentation de 20%",
            "resolution_months": 1
        }},
        "stats_summary": {{
            "new_balance": 950,
            "new_stress": 25,
            "new_fun": 50,
            "new_salary": 2300,
            "new_rent": 550
        }}
    }}
    """

    try:
        response = model.generate_content(
            system_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Erreur Gemini: {e}")
        return {
            "narrative": "Oups, le destin est confus (Erreur IA). Réessaie.",
            "updates": {},
            "pending_request": None
        }

# --- AGENT 2 : LE CONSEILLER (MENTOR) ---
def get_advisor_advice(question_or_situation: str, game_state_json: str):
    """
    Donne un conseil financier personnalisé basé sur la question du joueur.
    Intègre les produits bancaires officiels.
    
    Args:
        question_or_situation: La question du joueur ou une description de la situation
        game_state_json: L'état du jeu en JSON
    """
    # Formater les produits disponibles
    products_context = "\n\nPRODUITS BANCAIRES DISPONIBLES:\n"
    products_context += "== COMPTES CHÈQUES ==\n"
    for name, info in BANKING_OFFERS.items():
        products_context += f"- {name} ({info['bank']}) : {info['monthly_fee']}€/mois\n"
    
    products_context += "\n== PRODUITS D'ÉPARGNE ==\n"
    for name, info in SAVINGS_PRODUCTS.items():
        products_context += f"- {name} : {info['annual_return']*100:.1f}%/an - {info['tax_status']}\n"
    
    products_context += "\n== PRODUITS DE CRÉDIT ==\n"
    for name, info in CREDIT_PRODUCTS.items():
        products_context += f"- {name} : {info['rate']*100:.2f}% - {info['description']}\n"
    
    prompt = f"""
    Tu es "Fin", un conseiller financier expert en produits bancaires pour la Gen Z.
    Tu es un expert certifié qui connaît TOUS les produits financiers officiels.
    
    ÉTAT FINANCIER ACTUEL DU JOUEUR :
    {game_state_json}
    
    {products_context}
    
    QUESTION/DEMANDE DU JOUEUR : "{question_or_situation}"
    
    TACHE :
    1. Analyse la question du joueur et son état financier.
    2. Propose les produits bancaires OFFICIELS les plus adaptés avec leurs noms exacts.
    3. Sois spécifique : cite les taux, frais, avantages fiscaux réels.
    4. Donne un conseil actionable et personnalisé.
    5. Sois bienveillant, utilise des emojis, reste concis (2-4 phrases max).
    6. Si pertinent, mentionne les offres groupées de compte chèques.
    
    RÉPONSE PERSONNALISÉE :
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Le conseiller est en consultation. (Erreur IA)"
    
def generate_random_event(month):
    prompt = f"""
    Génère un événement financier aléatoire mineur (positif ou négatif) pour un jeune adulte au mois numéro {month}.
    Exemples : Panne de frigo, Prime inattendue, Amende, Vente Vinted.
    Réponds en JSON : {{ "event_name": "...", "cost": -50 }}
    """
    response = model.generate_content(
        prompt, 
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)