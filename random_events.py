"""
Module de gestion des événements aléatoires du jeu
Génère des événements qui impactent la vie du joueur
"""

import random
from ai_agents import generate_random_event

# Liste des événements pré-définis
PREDEFINED_EVENTS = [
    {
        "name": "Panne de Frigo",
        "description": "Ton frigo a rendu l'âme... Faut le remplacer!",
        "balance_change": -300,
        "stress_change": 10,
        "probability": 0.05
    },
    {
        "name": "Prime Inattendue",
        "description": "Ton boss te donne une prime de performance!",
        "balance_change": 200,
        "stress_change": -5,
        "probability": 0.08
    },
    {
        "name": "Amende de Stationnement",
        "description": "Oups, une amende de stationnement à payer...",
        "balance_change": -50,
        "stress_change": 5,
        "probability": 0.10
    },
    {
        "name": "Vente sur Vinted",
        "description": "Tu as vendu des affaires sur Vinted!",
        "balance_change": 80,
        "stress_change": -2,
        "probability": 0.07
    },
    {
        "name": "Dîner avec Amis",
        "description": "Une soirée sympa avec tes amis!",
        "balance_change": -40,
        "stress_change": -10,
        "fun_change": 15,
        "probability": 0.12
    },
    {
        "name": "Cadeau d'Anniversaire",
        "description": "Un ami te fait un cadeau surprenant!",
        "balance_change": 0,
        "stress_change": -5,
        "fun_change": 10,
        "probability": 0.04
    },
    {
        "name": "Maladie Mineure",
        "description": "Tu es tombé malade... repos obligatoire.",
        "balance_change": 0,
        "stress_change": 15,
        "fun_change": -10,
        "probability": 0.06
    },
    {
        "name": "Augmentation de Loyer",
        "description": "Le propriétaire augmente le loyer... zut!",
        "balance_change": -100,
        "stress_change": 20,
        "probability": 0.03
    },
    {
        "name": "Gain à la Loterie",
        "description": "Tu as gagné un petit truc à la loterie!",
        "balance_change": 150,
        "stress_change": -10,
        "fun_change": 20,
        "probability": 0.02
    },
    {
        "name": "Cours en Ligne Gratuit",
        "description": "Une belle opportunité de formation gratuite!",
        "balance_change": 0,
        "stress_change": -3,
        "probability": 0.05
    },
    {
        "name": "Réparation Urgente",
        "description": "Tes affaires électroniques ont besoin d'une réparation coûteuse.",
        "balance_change": -120,
        "stress_change": 8,
        "probability": 0.06
    },
    {
        "name": "Freelance Payant",
        "description": "Un boulot en freelance bien rémunéré!",
        "balance_change": 250,
        "stress_change": 5,
        "probability": 0.04
    }
]

def get_random_event() -> dict | None:
    """
    Génère un événement aléatoire basé sur les probabilités.
    
    Returns:
        dict: L'événement avec ses impacts, ou None si aucun événement
    """
    # Choisir un événement aléatoire
    rand = random.random()
    cumulative_prob = 0
    
    for event in PREDEFINED_EVENTS:
        cumulative_prob += event["probability"]
        if rand < cumulative_prob:
            return {
                "name": event["name"],
                "description": event["description"],
                "impact": {
                    "balance_change": event.get("balance_change", 0),
                    "stress_change": event.get("stress_change", 0),
                    "fun_change": event.get("fun_change", 0)
                }
            }
    
    return None

def get_events_summary() -> str:
    """Retourne un résumé des types d'événements possibles"""
    summary = "🎲 **Événements Possibles :**\n"
    for event in PREDEFINED_EVENTS:
        probability = int(event["probability"] * 100)
        summary += f"- {event['name']} ({probability}% de chance)\n"
    return summary

def apply_event_impact(state: dict, event: dict) -> dict:
    """
    Applique l'impact d'un événement à l'état du joueur.
    
    Args:
        state: L'état actuel du joueur
        event: L'événement à appliquer
        
    Returns:
        dict: L'état modifié
    """
    impact = event["impact"]
    
    # Appliquer les changements
    if "balance_change" in impact:
        state["finance"]["balance"] += impact["balance_change"]
    
    if "stress_change" in impact:
        state["profile"]["stress"] += impact["stress_change"]
        state["profile"]["stress"] = max(0, min(100, state["profile"]["stress"]))
    
    if "fun_change" in impact:
        state["profile"]["fun"] += impact["fun_change"]
        state["profile"]["fun"] = max(0, min(100, state["profile"]["fun"]))
    
    return state
