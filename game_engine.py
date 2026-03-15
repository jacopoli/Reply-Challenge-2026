import json
from config import *
from data_manager import save_game_state, load_game_state
from random_events import get_random_event, apply_event_impact
from investments import calculate_investment_returns
from pending_requests import add_pending_request, get_due_requests
from major_decisions import get_game_parameters

class GameState:
    def __init__(self, user_id: str = "default_player"):
        self.user_id = user_id
        # L'état initial du jeu
        self.state = {
            "profile": {
                "name": "Alex",
                "age": 22,
                "job": "Stagiaire Marketing",
                "stress": 20, # 0-100
                "fun": 50     # 0-100
            },
            "finance": {
                "balance": STARTING_BALANCE,
                "savings": STARTING_SAVINGS,
                "debt": 0,
                "investments": {},
                "transactions_log": [] # Historique pour le conseiller
            },
            "inventory": ["Vieux Laptop", "Vélo"],
            "time": {
                "month": 1,
                "year": 2024
            },
            "game_over": False
        }

    def get_json(self):
        """Retourne l'état sous forme de JSON pour l'IA"""
        return json.dumps(self.state, indent=2, ensure_ascii=False)
    
    def save(self):
        """Sauvegarde l'état du jeu dans un fichier JSON"""
        return save_game_state(self.user_id, self.state)
    
    def load(self):
        """Charge l'état du jeu depuis un fichier JSON"""
        loaded_state = load_game_state(self.user_id)
        if loaded_state:
            self.state = loaded_state
            return True
        return False

    def update_from_ai(self, ai_updates):
        """Met à jour l'état basé sur la réponse JSON de l'IA"""
        # Exemple d'update reçu : {"balance_change": -50, "stress_change": 5}
        if "balance_change" in ai_updates:
            self.state["finance"]["balance"] += ai_updates["balance_change"]
        if "stress_change" in ai_updates:
            self.state["profile"]["stress"] += ai_updates["stress_change"]
        if "inventory_add" in ai_updates and ai_updates["inventory_add"]:
            self.state["inventory"].append(ai_updates["inventory_add"])
        
        # Modifications du salaire et du loyer
        if "salary_change" in ai_updates and ai_updates["salary_change"] != 0:
            if "employment" not in self.state:
                self.state["employment"] = {"salary": SALARY}
            self.state["employment"]["salary"] += ai_updates["salary_change"]
        
        if "rent_change" in ai_updates and ai_updates["rent_change"] != 0:
            if "housing" not in self.state:
                self.state["housing"] = {"rent": MONTHLY_RENT}
            self.state["housing"]["rent"] += ai_updates["rent_change"]
        
        # Clamping (Garder les jauges entre 0 et 100)
        self.state["profile"]["stress"] = max(0, min(100, self.state["profile"]["stress"]))
        self.state["profile"]["fun"] = max(0, min(100, self.state["profile"].get("fun", 50)))
        
        # Traiter les demandes en attente (pending_request)
        if "pending_request" in ai_updates and ai_updates["pending_request"]:
            pending = ai_updates["pending_request"]
            self.state = add_pending_request(
                self.state,
                pending["type"],
                pending["description"],
                pending["resolution_months"]
            )
        
        # Sauvegarde automatique après chaque modification
        self.save()

    def advance_month(self):
        """LE MOTEUR HYBRIDE : Calculs mathématiques stricts"""
        finance = self.state["finance"]
        
        # Récupérer les paramètres actuels basés sur les décisions du joueur
        params = get_game_parameters(self.state)
        
        # 1. Revenus & Dépenses Fixes
        income = params["salary"]
        expenses = params["rent"] + MONTHLY_EXPENSES
        
        # 2. Intérêts (Calcul dynamique selon les souscriptions)
        savings_rate = SAVINGS_RATE  # Taux par défaut
        
        # Vérifier les souscriptions et ajuster le taux d'intérêt
        subscriptions = self.state.get("subscriptions", {})
        if subscriptions.get("Livret A"):
            savings_rate = 0.04  # 4% annuel
        elif subscriptions.get("Assurance-Vie"):
            savings_rate = 0.035  # 3.5% annuel
        elif subscriptions.get("PER"):
            savings_rate = 0.05  # 5% annuel (plan d'épargne retraite)
        elif subscriptions.get("PEA"):
            savings_rate = 0.10  # 10% annuel (plan d'épargne en actions)
        
        interests = finance["savings"] * (savings_rate / 12)
        
        # 3. Rendements des investissements
        self.state, investment_returns = calculate_investment_returns(self.state)
        
        # 4. Application
        net_change = income - expenses
        finance["balance"] += net_change
        finance["savings"] += interests
        
        # 5. Avance temps
        self.state["time"]["month"] += 1
        if self.state["time"]["month"] > 12:
            self.state["time"]["month"] = 1
            self.state["time"]["year"] += 1
        
        # 6. Récupère les demandes échues et les résout via IA
        due_requests = get_due_requests(self.state)
        request_resolutions = []
        
        if due_requests:
            from ai_agents import get_narrator_response
            for request in due_requests:
                # Générer une réponse pour la demande
                resolution_prompt = f"Résous cette demande du joueur: {request['description']}. Réponds simplement si succès/refusé/partiellement avec les impacts."
                resolution = get_narrator_response(resolution_prompt, self.get_json())
                request_resolutions.append({
                    "request": request,
                    "resolution": resolution
                })
                # Appliquer les impacts de la résolution
                if resolution.get("updates"):
                    self.update_from_ai(resolution["updates"])
        
        # 7. Vérifie si un événement aléatoire se produit
        event = get_random_event()
        event_message = None
        if event:
            self.state = apply_event_impact(self.state, event)
            event_message = event
        
        # 8. Sauvegarde automatique
        self.save()
            
        return {
            "net_change": net_change,
            "interests_earned": interests,
            "investment_returns": investment_returns,
            "new_balance": finance["balance"],
            "event": event_message,
            "request_resolutions": request_resolutions,
            "current_salary": params["salary"],
            "current_rent": params["rent"],
            "savings_rate_applied": savings_rate
        }