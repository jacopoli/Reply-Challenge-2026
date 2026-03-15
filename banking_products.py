"""
Module de produits financiers partenaires
Intègre les offres réelles des banques et des produits financiers
"""

# Offres bancaires officielles (Inspirées de BNP Paribas, Crédit Agricole, etc.)
BANKING_OFFERS = {
    "Compte Chèques Essentiel": {
        "bank": "BNP Paribas",
        "monthly_fee": 0,
        "description": "Compte courant avec essentiels",
        "features": [
            "✓ Compte chèques illimité",
            "✓ Carte bleue nationale",
            "✓ Virements gratuits",
            "✗ Pas d'intérêts"
        ],
        "target": "Débutant"
    },
    "Compte Chèques Moyen": {
        "bank": "Crédit Agricole",
        "monthly_fee": 3,
        "description": "Compte avec services additionnels",
        "features": [
            "✓ Compte chèques illimité",
            "✓ Carte bleue internationale",
            "✓ Virements gratuits",
            "✓ Assurance accidents",
            "✓ Petits intérêts"
        ],
        "target": "Utilisateur courant"
    },
    "Compte Chèques Premium": {
        "bank": "Société Générale",
        "monthly_fee": 8,
        "description": "Compte haut de gamme avec avantages",
        "features": [
            "✓ Compte chèques illimité",
            "✓ Carte platinum",
            "✓ Virements gratuits",
            "✓ Assurance complète",
            "✓ Intérêts + importants",
            "✓ Accès prioritaire conseil"
        ],
        "target": "Client fortuné"
    }
}

# Produits d'épargne officiels
SAVINGS_PRODUCTS = {
    "Livret A": {
        "bank": "La Poste / Tous les établissements",
        "annual_return": 0.04,
        "risk_level": "Très Faible",
        "description": "Épargne sécurisée avec garantie État",
        "min_amount": 10,
        "max_amount": 22950,
        "tax_status": "Exonéré d'impôt",
        "official_name": "Livret A"
    },
    "Livret de Développement Durable (LDD)": {
        "bank": "Tous les établissements",
        "annual_return": 0.04,
        "risk_level": "Très Faible",
        "description": "Épargne écologique défiscalisée",
        "min_amount": 10,
        "max_amount": 12000,
        "tax_status": "Exonéré d'impôt",
        "official_name": "LDD (ancien CODEVI)"
    },
    "Compte Épargne Logement (CEL)": {
        "bank": "Tous les établissements",
        "annual_return": 0.02,
        "risk_level": "Très Faible",
        "description": "Préparation à un achat immobilier",
        "min_amount": 300,
        "tax_status": "Intérêts partiellement imposés",
        "official_name": "CEL"
    },
    "Assurance-Vie": {
        "bank": "Toutes les assurances",
        "annual_return": 0.035,
        "risk_level": "Très Faible",
        "description": "Épargne sécurisée à long terme avec transmission",
        "min_amount": 50,
        "tax_status": "Fiscalité avantageuse après 8 ans",
        "official_name": "Contrat d'Assurance-Vie"
    },
    "Plan d'Épargne Retraite (PER)": {
        "bank": "Assurances et mutuelles",
        "annual_return": 0.05,
        "risk_level": "Faible",
        "description": "Épargne pour la retraite avec avantages fiscaux",
        "min_amount": 100,
        "tax_status": "Déductible du revenu imposable",
        "official_name": "PER (Perp, Perco)"
    },
    "Compte Titres Ordinaire (CTO)": {
        "bank": "Banques et courtiers",
        "annual_return": 0.08,
        "risk_level": "Moyen",
        "description": "Investissement en bourse sans limite",
        "min_amount": 100,
        "tax_status": "Impôts sur plus-values",
        "official_name": "Compte Titres Ordinaire"
    },
    "Plan d'Épargne en Actions (PEA)": {
        "bank": "Banques et courtiers",
        "annual_return": 0.10,
        "risk_level": "Moyen",
        "description": "Investissement en actions européennes",
        "min_amount": 300,
        "tax_status": "Exonéré après 5 ans",
        "official_name": "PEA"
    }
}

# Produits de crédit officiels
CREDIT_PRODUCTS = {
    "Crédit Personnel": {
        "bank": "BNP Paribas / Crédit Agricole",
        "rate": 0.05,
        "description": "Prêt personnel sans justification",
        "min_amount": 1000,
        "max_amount": 75000,
        "duration": "3 à 84 mois",
        "official_name": "Crédit Personnel"
    },
    "Crédit Auto": {
        "bank": "Toutes les banques",
        "rate": 0.045,
        "description": "Financement automobile dédié",
        "min_amount": 3000,
        "max_amount": 100000,
        "duration": "12 à 84 mois",
        "official_name": "Crédit Auto"
    },
    "Micro-crédit": {
        "bank": "ADIE, Toutes les banques",
        "rate": 0.08,
        "description": "Petits crédits pour projets perso",
        "min_amount": 300,
        "max_amount": 5000,
        "duration": "1 à 3 ans",
        "official_name": "Micro-crédit Personnel"
    },
    "Prêt Étudiant": {
        "bank": "Toutes les banques",
        "rate": 0.03,
        "description": "Financement des études",
        "min_amount": 1000,
        "max_amount": 50000,
        "duration": "3 à 10 ans",
        "official_name": "Prêt Étudiant"
    }
}

def get_banking_offers() -> dict:
    """Retourne les offres bancaires disponibles"""
    return BANKING_OFFERS

def get_savings_products() -> dict:
    """Retourne les produits d'épargne disponibles"""
    return SAVINGS_PRODUCTS

def get_credit_products() -> dict:
    """Retourne les produits de crédit disponibles"""
    return CREDIT_PRODUCTS

def format_offer_details(offer_type: str, offer_name: str) -> str:
    """
    Formate les détails d'une offre bancaire.
    
    Args:
        offer_type: Type d'offre (banking, savings, credit)
        offer_name: Nom de l'offre
        
    Returns:
        str: Détails formatés
    """
    if offer_type == "banking":
        offers = BANKING_OFFERS
    elif offer_type == "savings":
        offers = SAVINGS_PRODUCTS
    elif offer_type == "credit":
        offers = CREDIT_PRODUCTS
    else:
        return "Offre inconnue"
    
    if offer_name not in offers:
        return "Offre non trouvée"
    
    offer = offers[offer_name]
    details = f"**{offer_name}**\n"
    details += f"🏦 {offer.get('bank', 'Banque partenaire')}\n"
    details += f"📝 {offer.get('description', '')}\n"
    
    if offer_type == "banking":
        details += f"💰 Frais : {offer.get('monthly_fee', 0)}€/mois\n"
        details += "**Fonctionnalités :**\n"
        for feature in offer.get('features', []):
            details += f"{feature}\n"
    
    elif offer_type == "savings":
        details += f"📈 Rendement : {offer.get('annual_return', 0)*100:.1f}%/an\n"
        details += f"⚠️ Risque : {offer.get('risk_level', '')}\n"
        details += f"💼 Min-Max : {offer.get('min_amount', 0)}€ - {offer.get('max_amount', '∞')}€\n"
        details += f"🔍 Fiscalité : {offer.get('tax_status', '')}\n"
    
    elif offer_type == "credit":
        details += f"📊 Taux : {offer.get('rate', 0)*100:.2f}%\n"
        details += f"💼 Montant : {offer.get('min_amount', 0)}€ à {offer.get('max_amount', 0)}€\n"
        details += f"⏱️ Durée : {offer.get('duration', '')}\n"
    
    return details

def get_advisor_recommendation(state: dict) -> str:
    """
    Génère une recommandation personnalisée d'offre bancaire.
    
    Args:
        state: État du joueur
        
    Returns:
        str: Recommandation
    """
    balance = state["finance"]["balance"]
    savings = state["finance"]["savings"]
    total = balance + savings
    
    recommendations = "💡 **Nos offres recommandées pour vous :**\n\n"
    
    # Recommandation compte chèques
    if balance < 2000:
        recommendations += "📌 **Compte Chèques Essentiel** - Parfait pour débuter, frais 0€\n"
    elif balance < 5000:
        recommendations += "📌 **Compte Chèques Moyen** - Bon équilibre avec services utiles\n"
    else:
        recommendations += "📌 **Compte Chèques Premium** - Services premium pour gros patrimoine\n"
    
    # Recommandation épargne
    if total > 2000:
        recommendations += "\n📌 **Livret A** - Sûr et défiscalisé, parfait comme base\n"
    if total > 5000:
        recommendations += "📌 **Assurance-Vie** - Long terme avec avantages fiscaux\n"
    if total > 10000:
        recommendations += "📌 **PEA** - Investissements en bourse avec exonération\n"
    
    # Recommandation crédit si besoin
    if balance < 0:
        recommendations += "\n📌 **Crédit Personnel** - Rattraper vos dettes efficacement\n"
    
    recommendations += "\n👉 *Parlez-en au coach pour plus de détails sur chaque produit !*"
    
    return recommendations
