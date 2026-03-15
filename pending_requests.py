"""
Module de gestion de la mémoire des demandes/actions en attente
Garde en mémoire les demandes du joueur avec des délais et les résout automatiquement
"""

import json

def add_pending_request(state: dict, request_type: str, description: str, resolution_month: int) -> dict:
    """
    Ajoute une demande en attente au journal du joueur.
    
    Args:
        state: État actuel du joueur
        request_type: Type de demande (augmentation, prêt, formation, etc.)
        description: Description de la demande
        resolution_month: Nombre de mois avant la résolution
        
    Returns:
        dict: État mis à jour
    """
    if "pending_requests" not in state:
        state["pending_requests"] = []
    
    current_month = state["time"]["month"]
    current_year = state["time"]["year"]
    
    # Calculer le mois de résolution
    resolution_date = current_month + resolution_month
    resolution_year = current_year
    
    if resolution_date > 12:
        resolution_year += 1
        resolution_date = resolution_date % 12
        if resolution_date == 0:
            resolution_date = 12
    
    request = {
        "type": request_type,
        "description": description,
        "created_month": current_month,
        "created_year": current_year,
        "resolution_month": resolution_date,
        "resolution_year": resolution_year,
        "status": "pending"
    }
    
    state["pending_requests"].append(request)
    return state

def get_due_requests(state: dict) -> list:
    """
    Récupère toutes les demandes qui arrivent à échéance ce mois-ci.
    
    Args:
        state: État actuel du joueur
        
    Returns:
        list: Liste des demandes à résoudre
    """
    current_month = state["time"]["month"]
    current_year = state["time"]["year"]
    
    due_requests = []
    
    if "pending_requests" not in state:
        return due_requests
    
    for request in state["pending_requests"]:
        if (request["resolution_month"] == current_month and 
            request["resolution_year"] == current_year and
            request["status"] == "pending"):
            due_requests.append(request)
    
    return due_requests

def resolve_request(state: dict, request_index: int, outcome: str, impact: dict) -> dict:
    """
    Résout une demande avec un résultat et ses impacts.
    
    Args:
        state: État actuel du joueur
        request_index: Index de la demande
        outcome: Résultat (succès, refusé, partiellement approuvé)
        impact: Dict avec les changements (balance_change, stress_change, etc.)
        
    Returns:
        dict: État mis à jour
    """
    if "pending_requests" not in state or request_index >= len(state["pending_requests"]):
        return state
    
    request = state["pending_requests"][request_index]
    request["status"] = "resolved"
    request["outcome"] = outcome
    request["impact"] = impact
    
    # Appliquer les impacts
    if "balance_change" in impact:
        state["finance"]["balance"] += impact["balance_change"]
    
    if "stress_change" in impact:
        state["profile"]["stress"] += impact["stress_change"]
        state["profile"]["stress"] = max(0, min(100, state["profile"]["stress"]))
    
    if "fun_change" in impact:
        state["profile"]["fun"] += impact["fun_change"]
        state["profile"]["fun"] = max(0, min(100, state["profile"]["fun"]))
    
    if "salary_change" in impact:
        # À implémenter dans config si nécessaire
        pass
    
    return state

def get_pending_requests_summary(state: dict) -> str:
    """
    Retourne un résumé des demandes en attente.
    
    Args:
        state: État actuel du joueur
        
    Returns:
        str: Résumé des demandes
    """
    if "pending_requests" not in state or not state["pending_requests"]:
        return "Aucune demande en attente."
    
    pending = [r for r in state["pending_requests"] if r["status"] == "pending"]
    
    if not pending:
        return "Aucune demande en attente."
    
    summary = "📋 **Demandes en Attente :**\n"
    for i, req in enumerate(pending):
        months_left = calculate_months_until(
            state["time"]["month"],
            state["time"]["year"],
            req["resolution_month"],
            req["resolution_year"]
        )
        summary += f"- **{req['type']}** : {req['description']} (Réponse dans {months_left} mois)\n"
    
    return summary

def calculate_months_until(current_month: int, current_year: int, 
                          target_month: int, target_year: int) -> int:
    """Calcule le nombre de mois entre deux dates."""
    if current_year == target_year:
        return target_month - current_month
    else:
        return (target_year - current_year - 1) * 12 + (12 - current_month) + target_month

def generate_resolution_narrative(request: dict) -> str:
    """
    Génère une narration pour la résolution d'une demande.
    
    Args:
        request: La demande à résoudre
        
    Returns:
        str: Texte narratif de la résolution
    """
    request_type = request["type"].lower()
    outcome = request.get("outcome", "")
    
    narratives = {
        "augmentation": {
            "succès": f"Félicitations ! 🎉 Ton patron a approuvé ta demande d'augmentation ! Tu vas gagner plus désormais.",
            "refusé": f"Malheureusement 😔 ton patron a décliné ta demande d'augmentation. Peut-être une autre fois...",
            "partiellement": f"Ton patron a approuvé une augmentation partielle. C'est mieux que rien ! 💰"
        },
        "prêt": {
            "succès": f"Bonne nouvelle ! 🏦 La banque a approuvé ton prêt ! Les fonds sont maintenant sur ton compte.",
            "refusé": f"Malheureusement 😔 la banque a rejeté ta demande de prêt. Tes revenus sont insuffisants.",
            "partiellement": f"La banque a approuvé un prêt de montant réduit. C'est un début ! 💰"
        },
        "formation": {
            "succès": f"Super ! 🎓 Tu as été accepté(e) dans la formation ! Les apprentissages vont commencer.",
            "refusé": f"Désolé 😔 tu n'as pas été accepté(e) dans cette formation.",
            "partiellement": f"Tu as été mis(e) en liste d'attente pour la formation."
        },
        "congés": {
            "succès": f"Génial ! 🏖️ Ton patron a approuvé tes congés ! Profite bien du repos.",
            "refusé": f"Dommage 😔 ton patron ne peut pas approuver tes congés maintenant.",
        }
    }
    
    if request_type in narratives and outcome in narratives[request_type]:
        return narratives[request_type][outcome]
    
    return f"Résolution de ta demande de {request['type']}: {outcome}"
