"""
Module de gestion des décisions majeures du joueur
Permet au joueur de prendre des décisions qui modifient les paramètres du jeu
Ex: Changer de travail, déménager, etc.
"""

import json
from config import SALARY, MONTHLY_RENT, MONTHLY_EXPENSES

# Définition des emplois disponibles
JOBS = {
    "Stagiaire Marketing": {
        "salary": 1800,
        "difficulty": "Facile",
        "description": "Poste de départ, peu expérience requise",
        "required_balance": 0,
        "stress_impact": 20
    },
    "Développeur Junior": {
        "salary": 2500,
        "difficulty": "Moyen",
        "description": "Nécessite des compétences en programmation",
        "required_balance": 500,
        "stress_impact": 30
    },
    "Chef de Projet": {
        "salary": 3200,
        "difficulty": "Difficile",
        "description": "Leadership et gestion requises",
        "required_balance": 2000,
        "stress_impact": 50
    },
    "Consultant Senior": {
        "salary": 4000,
        "difficulty": "Très Difficile",
        "description": "Expertise et expérience essentielles",
        "required_balance": 5000,
        "stress_impact": 60
    },
    "Freelancer": {
        "salary": 2200,
        "difficulty": "Variable",
        "description": "Liberté mais revenus irréguliers",
        "required_balance": 1000,
        "stress_impact": 35
    },
    "Entrepreneur": {
        "salary": 3500,
        "difficulty": "Très Difficile",
        "description": "Ton propre patron, haute volatilité",
        "required_balance": 10000,
        "stress_impact": 70
    }
}

# Définition des logements disponibles
APARTMENTS = {
    "Studio Excentré": {
        "rent": 450,
        "location": "Banlieue",
        "description": "Petit mais abordable",
        "fun_impact": -10,
        "stress_impact": 0,
        "commute_cost": 50
    },
    "Appartement T2 Banlieue": {
        "rent": 600,
        "location": "Banlieue",
        "description": "Confortable, accès OK",
        "fun_impact": 0,
        "stress_impact": 0,
        "commute_cost": 40
    },
    "Appartement T3 Centre": {
        "rent": 900,
        "location": "Centre-Ville",
        "description": "Bien situé, vie sociale facile",
        "fun_impact": 15,
        "stress_impact": -5,
        "commute_cost": 10
    },
    "Maison de Campagne": {
        "rent": 700,
        "location": "Campagne",
        "description": "Tranquille mais isolé",
        "fun_impact": -5,
        "stress_impact": -15,
        "commute_cost": 80
    },
    "Luxe Penthouse": {
        "rent": 1500,
        "location": "Centre-Ville Prestige",
        "description": "Le meilleur, mais très cher",
        "fun_impact": 30,
        "stress_impact": -10,
        "commute_cost": 5
    }
}

def get_available_jobs() -> dict:
    """Retourne les emplois disponibles"""
    return JOBS

def get_available_apartments() -> dict:
    """Retourne les appartements disponibles"""
    return APARTMENTS

def change_job(new_job: str, state: dict) -> tuple[dict, str]:
    """
    Change l'emploi du joueur.
    
    Args:
        new_job: Le nouvel emploi
        state: État actuel du joueur
        
    Returns:
        tuple: (état mis à jour, message d'erreur ou None)
    """
    if new_job not in JOBS:
        return state, "Emploi non trouvé"
    
    job_info = JOBS[new_job]
    
    # Vérifier si le joueur a assez d'argent (frais de transition)
    if state["finance"]["balance"] < job_info["required_balance"]:
        return state, f"❌ Solde insuffisant. Vous avez besoin d'au moins {job_info['required_balance']}€"
    
    old_salary = state.get("employment", {}).get("salary", SALARY)
    
    # Mettre à jour l'emploi
    if "employment" not in state:
        state["employment"] = {}
    
    state["employment"]["job_title"] = new_job
    state["employment"]["salary"] = job_info["salary"]
    state["employment"]["joined_month"] = state["time"]["month"]
    state["profile"]["job"] = new_job
    state["profile"]["stress"] = min(100, state["profile"]["stress"] + job_info["stress_impact"])
    
    salary_change = job_info["salary"] - old_salary
    message = f"✅ Vous avez changé d'emploi ! Nouveau salaire : {job_info['salary']}€/mois (+{salary_change}€)"
    
    return state, message

def change_apartment(new_apartment: str, state: dict) -> tuple[dict, str]:
    """
    Change l'appartement du joueur.
    
    Args:
        new_apartment: Le nouvel appartement
        state: État actuel du joueur
        
    Returns:
        tuple: (état mis à jour, message d'erreur ou None)
    """
    if new_apartment not in APARTMENTS:
        return state, "Appartement non trouvé"
    
    apartment_info = APARTMENTS[new_apartment]
    old_rent = state.get("housing", {}).get("rent", MONTHLY_RENT)
    
    # Mettre à jour le logement
    if "housing" not in state:
        state["housing"] = {}
    
    state["housing"]["apartment"] = new_apartment
    state["housing"]["rent"] = apartment_info["rent"]
    state["housing"]["location"] = apartment_info["location"]
    state["housing"]["moved_month"] = state["time"]["month"]
    
    # Appliquer les impacts
    state["profile"]["fun"] = max(0, min(100, state["profile"]["fun"] + apartment_info["fun_impact"]))
    state["profile"]["stress"] = max(0, min(100, state["profile"]["stress"] + apartment_info["stress_impact"]))
    
    rent_change = apartment_info["rent"] - old_rent
    message = f"✅ Vous avez déménagé ! Nouveau loyer : {apartment_info['rent']}€/mois ({rent_change:+d}€)"
    
    return state, message

def get_game_parameters(state: dict) -> dict:
    """
    Retourne les paramètres actuels du jeu basés sur les décisions du joueur.
    
    Args:
        state: État actuel du joueur
        
    Returns:
        dict: Paramètres (salaire, loyer, etc.)
    """
    salary = state.get("employment", {}).get("salary", SALARY)
    rent = state.get("housing", {}).get("rent", MONTHLY_RENT)
    
    return {
        "salary": salary,
        "rent": rent,
        "expenses": MONTHLY_EXPENSES,
        "net_monthly": salary - rent - MONTHLY_EXPENSES,
        "job": state.get("profile", {}).get("job", "Stagiaire Marketing"),
        "location": state.get("housing", {}).get("location", "Banlieue")
    }

def get_decision_summary(state: dict) -> str:
    """
    Retourne un résumé des décisions prises par le joueur.
    
    Args:
        state: État actuel du joueur
        
    Returns:
        str: Résumé formaté
    """
    params = get_game_parameters(state)
    summary = "📊 **Votre Profil Actuel :**\n"
    summary += f"- 💼 Emploi : {params['job']}\n"
    summary += f"- 💰 Salaire : {params['salary']}€/mois\n"
    summary += f"- 🏠 Logement : {params['location']} ({params['rent']}€/mois)\n"
    summary += f"- 📈 Solde net mensuel : {params['net_monthly']}€\n"
    
    return summary

def validate_major_decision(decision_type: str, new_value: str, state: dict) -> tuple[bool, str]:
    """
    Valide une décision majeure avant application.
    
    Args:
        decision_type: Type de décision (job, apartment, etc.)
        new_value: Nouvelle valeur
        state: État actuel
        
    Returns:
        tuple: (valide, message)
    """
    if decision_type == "job":
        if new_value not in JOBS:
            return False, "❌ Emploi invalide"
        if state["finance"]["balance"] < JOBS[new_value]["required_balance"]:
            return False, f"❌ Solde insuffisant ({JOBS[new_value]['required_balance']}€ requis)"
    
    elif decision_type == "apartment":
        if new_value not in APARTMENTS:
            return False, "❌ Appartement invalide"
    
    return True, "✅ Valide"
