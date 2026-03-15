"""
Module de gestion des investissements
Permet au joueur d'investir son argent dans différents produits financiers
"""

import random
from config import INVESTMENTS

def get_investment_options():
    """Retourne les options d'investissement disponibles"""
    return INVESTMENTS

def invest(amount: float, investment_type: str, state: dict) -> dict:
    """
    Place un investissement pour le joueur.
    
    Args:
        amount: Montant à investir
        investment_type: Type d'investissement (clé dans INVESTMENTS)
        state: État actuel du joueur
        
    Returns:
        dict: État mis à jour ou None en cas d'erreur
    """
    if investment_type not in INVESTMENTS:
        return None
    
    investment = INVESTMENTS[investment_type]
    
    # Vérifier si le montant est suffisant
    if amount < investment["min_amount"]:
        return None
    
    # Vérifier le solde
    if state["finance"]["balance"] < amount:
        return None
    
    # Initialiser le portefeuille si nécessaire
    if "investments" not in state["finance"]:
        state["finance"]["investments"] = {}
    
    # Ajouter l'investissement
    if investment_type not in state["finance"]["investments"]:
        state["finance"]["investments"][investment_type] = {
            "amount": 0,
            "purchase_price": 0
        }
    
    # Mettre à jour l'investissement
    state["finance"]["investments"][investment_type]["amount"] += amount
    state["finance"]["investments"][investment_type]["purchase_price"] = \
        (state["finance"]["investments"][investment_type].get("purchase_price", 0) + amount) / 2
    
    # Déduire du solde
    state["finance"]["balance"] -= amount
    
    return state

def calculate_investment_returns(state: dict) -> dict:
    """
    Calcule les rendements des investissements mensuels.
    
    Args:
        state: État actuel du joueur
        
    Returns:
        dict: État mis à jour avec rendements appliqués
    """
    if "investments" not in state["finance"]:
        return state, 0
    
    total_returns = 0
    
    for inv_type, data in state["finance"]["investments"].items():
        if inv_type not in INVESTMENTS or data["amount"] <= 0:
            continue
        
        investment = INVESTMENTS[inv_type]
        monthly_return_rate = investment["annual_return"] / 12
        
        # Calculer le rendement
        monthly_return = data["amount"] * monthly_return_rate
        
        # Appliquer les risques si applicable
        if "risk_factor" in investment and random.random() < investment["risk_factor"]:
            # Perte de 10% en cas de risque
            monthly_return -= data["amount"] * 0.10
        
        # Ajouter au solde
        state["finance"]["balance"] += monthly_return
        total_returns += monthly_return
    
    return state, total_returns

def withdraw_investment(amount: float, investment_type: str, state: dict) -> dict:
    """
    Retire un investissement.
    
    Args:
        amount: Montant à retirer
        investment_type: Type d'investissement
        state: État actuel du joueur
        
    Returns:
        dict: État mis à jour ou None en cas d'erreur
    """
    if investment_type not in state.get("finance", {}).get("investments", {}):
        return None
    
    investment = state["finance"]["investments"][investment_type]
    
    if investment["amount"] < amount:
        return None
    
    # Retirer l'investissement
    investment["amount"] -= amount
    
    # Ajouter au solde
    state["finance"]["balance"] += amount
    
    return state

def get_total_invested(state: dict) -> float:
    """Retourne le montant total investi"""
    if "investments" not in state["finance"]:
        return 0
    
    total = sum(inv["amount"] for inv in state["finance"]["investments"].values())
    return total

def get_investment_summary(state: dict) -> str:
    """Retourne un résumé des investissements"""
    if "investments" not in state["finance"] or not state["finance"]["investments"]:
        return "Aucun investissement actuellement."
    
    summary = "📊 **Vos Investissements :**\n"
    for inv_type, data in state["finance"]["investments"].items():
        if data["amount"] > 0:
            investment = INVESTMENTS[inv_type]
            annual_return = investment["annual_return"] * 100
            summary += f"- **{inv_type}** : {data['amount']:.2f}€ (Rendement : {annual_return}% / an)\n"
    
    return summary
