import streamlit as st
from game_engine import GameState
from ai_agents import get_narrator_response, get_advisor_advice
from data_manager import list_users, user_exists, delete_user_data
from random_events import get_events_summary
from investments import get_investment_options, invest, withdraw_investment, get_total_invested, get_investment_summary
from pending_requests import get_pending_requests_summary
from major_decisions import get_available_jobs, get_available_apartments, change_job, change_apartment, get_decision_summary
from config import SALARY, MONTHLY_RENT
from banking_products import get_banking_offers, get_savings_products, get_credit_products, get_advisor_recommendation, format_offer_details

# --- GESTION DES UTILISATEURS ---
st.sidebar.title("👤 Gestion Utilisateur")

# Sélection ou création d'utilisateur
users = list_users()
selected_user = st.sidebar.selectbox(
    "Sélectionne un profil :",
    users + ["➕ Créer un nouveau profil"],
    key="user_select"
)

if selected_user == "➕ Créer un nouveau profil":
    new_user = st.sidebar.text_input("Nom du nouveau profil :", key="new_user_input")
    if new_user and st.sidebar.button("Créer"):
        if user_exists(new_user):
            st.sidebar.error("❌ Ce profil existe déjà!")
        else:
            st.session_state.current_user = new_user
            st.rerun()
else:
    st.session_state.current_user = selected_user

# Initialisation du jeu avec le bon utilisateur
current_user = st.session_state.get("current_user", "default_player")

if 'game' not in st.session_state or st.session_state.get("last_user") != current_user:
    game = GameState(current_user)
    if not game.load():
        # Nouveau jeu
        pass
    st.session_state.game = game
    st.session_state.last_user = current_user
    
if 'history' not in st.session_state:
    st.session_state.history = []
if 'advisor_msg' not in st.session_state:
    st.session_state.advisor_msg = None

game = st.session_state.game
state = game.state

# --- BOUTONS DE GESTION ---
col1, col2 = st.sidebar.columns(2)
if col1.button("🔄 Recharger", key="reload_btn"):
    game.load()
    st.rerun()

if col2.button("💾 Sauvegarder", key="save_btn"):
    game.save()
    st.sidebar.success("✅ Sauvegardé!")

if st.sidebar.button("🗑️ Supprimer ce profil", key="delete_btn"):
    if st.sidebar.checkbox("Confirmer la suppression"):
        delete_user_data(current_user)
        st.sidebar.success("✅ Profil supprimé!")
        st.session_state.current_user = "default_player"
        st.rerun()

# --- LAYOUT ---
st.set_page_config(layout="wide", page_title="FinSim: Life Simulator")

# COLONNE GAUCHE : DASHBOARD
with st.sidebar:
    st.divider()
    st.title("📊 Mon Profil")
    st.write(f"**Joueur:** {current_user}")
    st.metric("Âge", f"{state['profile']['age']} ans")
    
    # Récupérer les paramètres dynamiques
    from major_decisions import get_game_parameters
    params = get_game_parameters(state)
    
    st.write(f"**Emploi:** {state['profile']['job']}")
    st.write(f"💰 Salaire: {params['salary']:.0f}€/mois")
    st.write(f"🏠 Loyer: {params['rent']:.0f}€/mois")
    
    st.divider()
    
    # Jauges Financières
    col1, col2 = st.columns(2)
    col1.metric("Solde Courant", f"{state['finance']['balance']:.2f}€")
    col2.metric("Épargne", f"{state['finance']['savings']:.2f}€")
    
    st.divider()
    st.progress(state['profile']['stress'], text="Niveau de Stress")
    
    st.subheader("🎒 Inventaire")
    for item in state['inventory']:
        st.write(f"- {item}")

# COLONNE DROITE : ONGLETS
st.header(f"📅 {state['time']['month']}/{state['time']['year']} - Tableau de Bord")

# Créer les onglets
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["👤 Personnel", "💰 Impôts", "🏦 Épargne/Investissements", "😌 Bien-être", "📊 Comptabilité", "🎯 Décisions Majeures", "🏪 Offres Bancaires"])

# --- ONGLET 1 : PERSONNEL ---
with tab1:
    st.subheader("👤 Informations Personnelles")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nom", state['profile']['name'])
    with col2:
        st.metric("Âge", f"{state['profile']['age']} ans")
    with col3:
        st.metric("Métier", state['profile']['job'])
    
    st.divider()
    st.subheader("🎒 Inventaire")
    for item in state['inventory']:
        st.write(f"✓ {item}")

# --- ONGLET 2 : IMPÔTS ---
with tab2:
    st.subheader("💰 Impôts et Taxes")
    
    # Obtenir les paramètres dynamiques
    from major_decisions import get_game_parameters
    params = get_game_parameters(state)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Salaire Brut", f"{params['salary']:.0f}€/mois")
    with col2:
        # Estimation d'impôts (simplifiée)
        estimated_tax = max(0, params['salary'] * 0.10) if params['salary'] > 2500 else 0
        st.metric("Estimation Impôts", f"{estimated_tax:.0f}€/an")
    
    st.divider()
    st.write("**💼 Situation Professionnelle :**")
    st.write(f"- Emploi : {params['job']}")
    st.write(f"- Revenus mensuels : {params['salary']}€")
    st.write(f"- Loyer/Habitation : {params['rent']}€")
    st.write(f"- Dépenses courantes : 400€")
    st.write(f"- **Solde net mensuel : {params['net_monthly']}€**")
    
    st.divider()
    st.write("💡 *Vérifiez vos obligations fiscales auprès des autorités compétentes.*")

# --- ONGLET 3 : ÉPARGNE/INVESTISSEMENTS ---
with tab3:
    st.subheader("🏦 Épargne et Investissements")
    
    # Obtenir les paramètres dynamiques
    from major_decisions import get_game_parameters
    params = get_game_parameters(state)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Épargne Totale", f"{state['finance']['savings']:.2f}€")
    with col2:
        # Rendement selon le produit souscrit
        savings_rate = 0.03  # Livret A par défaut
        if state.get("subscriptions", {}).get("Livret A"):
            savings_rate = 0.04
        if state.get("subscriptions", {}).get("Assurance-Vie"):
            savings_rate = 0.035
        rate = (state['finance']['savings'] * savings_rate / 12)
        st.metric("Intérêts Mensuels", f"{rate:.2f}€")
    with col3:
        total_invested = get_total_invested(state)
        st.metric("Investissements", f"{total_invested:.2f}€")
    
    st.divider()
    
    # Afficher les produits souscrits
    st.subheader("📋 Vos Souscriptions")
    subscriptions = state.get("subscriptions", {})
    if subscriptions:
        for product, active in subscriptions.items():
            if active:
                st.write(f"✅ {product}")
    else:
        st.write("*Aucune souscription actuellement*")
    
    st.divider()
    st.subheader("🏦 Souscrire à un Produit d'Épargne")
    
    col_prod1, col_prod2 = st.columns(2)
    
    with col_prod1:
        savings_products = get_savings_products()
        product_choice = st.selectbox(
            "Choisir un produit :",
            list(savings_products.keys()),
            key="savings_product_choice"
        )
    
    with col_prod2:
        amount = st.number_input(
            "Montant initial (€) :",
            min_value=0.0,
            step=100.0,
            key="savings_amount"
        )
    
    if product_choice:
        product_info = savings_products[product_choice]
        st.info(f"""
        **{product_choice}**
        - 🏦 {product_info.get('bank', 'Partenaire')}
        - 📈 Rendement : {product_info['annual_return']*100:.1f}%/an
        - ⚠️ Risque : {product_info['risk_level']}
        - 💰 Montant min : {product_info['min_amount']}€
        - 🔍 Fiscalité : {product_info['tax_status']}
        """)
        
        if st.button("✅ Souscrire à ce produit", key="subscribe_savings"):
            if amount >= product_info['min_amount'] and state['finance']['balance'] >= amount:
                # Ajouter la souscription
                if "subscriptions" not in state:
                    state["subscriptions"] = {}
                state["subscriptions"][product_choice] = True
                
                # Débiter le solde
                state['finance']['balance'] -= amount
                state['finance']['savings'] += amount
                
                # Sauvegarder
                game.state = state
                game.save()
                
                st.success(f"✅ Souscription confirmée ! {amount}€ investis dans {product_choice}")
                st.rerun()
            else:
                st.error("❌ Solde insuffisant ou montant en dessous du minimum")
    
    st.divider()
    st.write(get_investment_summary(state))

# --- ONGLET 4 : BIEN-ÊTRE ---
with tab4:
    st.subheader("😌 Bien-être et Santé Mentale")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Niveau de Stress", f"{state['profile']['stress']}/100")
        st.progress(state['profile']['stress'] / 100, text="Stress")
    with col2:
        st.metric("Plaisir/Fun", f"{state['profile']['fun']}/100")
        st.progress(state['profile']['fun'] / 100, text="Fun")
    
    st.divider()
    st.subheader("📋 Demandes en Attente")
    st.write(get_pending_requests_summary(state))
    
    st.divider()
    if state['profile']['stress'] > 70:
        st.warning("⚠️ Votre stress est élevé. Pensez à vous détendre!")
    if state['profile']['fun'] < 30:
        st.warning("⚠️ Vous manquez de plaisir. Prévoyez une activité sympa!")

# --- ONGLET 5 : COMPTABILITÉ ---
with tab5:
    st.subheader("📊 Comptabilité et Finances")
    
    # Récupérer les paramètres dynamiques
    from major_decisions import get_game_parameters
    params = get_game_parameters(state)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Solde Courant", f"{state['finance']['balance']:.2f}€")
    with col2:
        total_assets = state['finance']['balance'] + state['finance']['savings']
        st.metric("Patrimoine Total", f"{total_assets:.2f}€")
    
    st.divider()
    st.write("📋 Résumé Financier :")
    monthly_expenses = 400  # From config
    net_monthly = params['salary'] - params['rent'] - monthly_expenses
    
    st.write(f"- Revenus Mensuels : {params['salary']:.0f}€")
    st.write(f"- Loyer : {params['rent']:.0f}€")
    st.write(f"- Dépenses Courantes : {monthly_expenses}€")
    st.write(f"- **Solde Net : {net_monthly:.0f}€**")
    
    st.divider()
    st.subheader("🎲 Événements Aléatoires")
    st.write(get_events_summary())

# --- ONGLET 6 : DÉCISIONS MAJEURES ---
with tab6:
    st.subheader("🎯 Décisions Majeures")
    st.write(get_decision_summary(state))
    
    st.divider()
    st.info("💡 **Utilisez le chat pour changer d'emploi, déménager, ou modifier vos conditions de vie !**\n\nExemples :\n- *Je cherche un nouvel emploi en tant que développeur*\n- *Je veux déménager au centre-ville*\n- *Je quitte mon travail pour devenir freelancer*")

# --- ONGLET 7 : OFFRES BANCAIRES ---
with tab7:
    st.subheader("🏪 Offres Bancaires & Produits Financiers")
    st.write("💡 Découvrez les offres bancaires officielles adaptées à votre profil !")
    
    st.divider()
    st.write(get_advisor_recommendation(state))
    
    st.divider()
    
    # Sélection d'offre détaillée
    offer_type = st.selectbox(
        "Explorez nos offres :",
        ["Comptes Chèques", "Produits d'Épargne", "Produits de Crédit"],
        key="offer_type_select"
    )
    
    if offer_type == "Comptes Chèques":
        col1, col2 = st.columns(2)
        for i, (name, info) in enumerate(get_banking_offers().items()):
            with col1 if i % 2 == 0 else col2:
                st.write(format_offer_details("banking", name))
                st.write("")
    
    elif offer_type == "Produits d'Épargne":
        col1, col2 = st.columns(2)
        for i, (name, info) in enumerate(get_savings_products().items()):
            with col1 if i % 2 == 0 else col2:
                st.write(format_offer_details("savings", name))
                st.write("")
    
    elif offer_type == "Produits de Crédit":
        col1, col2 = st.columns(2)
        for i, (name, info) in enumerate(get_credit_products().items()):
            with col1 if i % 2 == 0 else col2:
                st.write(format_offer_details("credit", name))
                st.write("")

# --- CONSEILLER AI BOX ---
st.divider()
st.subheader("💡 Conseil du Coach Financier")

if 'advisor_msg' not in st.session_state:
    st.session_state.advisor_msg = None

# Interface pour poser une question au conseiller
col_advisor1, col_advisor2 = st.columns([3, 1])

with col_advisor1:
    advisor_question = st.text_input(
        "Pose une question au coach :",
        placeholder="Ex: Comment bien gérer mon épargne ? Dois-je prendre un crédit ?",
        key="advisor_question_input"
    )

with col_advisor2:
    ask_advisor_btn = st.button("📢 Demander Conseil", key="get_advice_btn")

if ask_advisor_btn:
    if advisor_question.strip():
        question_to_use = advisor_question
    else:
        question_to_use = "Bilan général de ma situation financière"
    
    with st.spinner("Le coach réfléchit à ta question..."):
        advisor_feedback = get_advisor_advice(question_to_use, game.get_json())
        st.session_state.advisor_msg = advisor_feedback

# Afficher le conseil si disponible
if st.session_state.advisor_msg:
    st.info(st.session_state.advisor_msg)

# --- SECTION GAMEPLAY ---
st.divider()
st.header("🎮 Actions")

# Affichage de l'historique du chat
st.subheader("Historique des Actions")
for sender, msg in st.session_state.history:
    with st.chat_message(sender):
        st.write(msg)

# Input Utilisateur (Action Libre)
user_input = st.chat_input("Ex: J'achète un scooter, Je demande une augmentation...")

if user_input:
    # A. Afficher le message user
    st.session_state.history.append(("user", user_input))
    
    # Sauvegarder les anciennes stats
    old_balance = game.state["finance"]["balance"]
    old_stress = game.state["profile"]["stress"]
    old_fun = game.state["profile"]["fun"]
    old_salary = game.state.get("employment", {}).get("salary", SALARY)
    old_rent = game.state.get("housing", {}).get("rent", MONTHLY_RENT)
    
    # B. Appel Narrateur
    with st.spinner("Le Maître du jeu réfléchit..."):
        ai_response = get_narrator_response(user_input, game.get_json())
    
    # C. Mise à jour du jeu
    narrative = ai_response["narrative"]
    game.update_from_ai(ai_response["updates"])
    
    # D. Ajouter les stats modifiées à la narration
    if "stats_summary" in ai_response:
        stats = ai_response["stats_summary"]
        narrative += f"\n\n📊 **Vos nouvelles stats :**"
        if "new_balance" in stats:
            new_balance = stats["new_balance"]
            balance_change = new_balance - old_balance
            change_symbol = "📈" if balance_change > 0 else "📉" if balance_change < 0 else "➡️"
            narrative += f"\n💰 Solde : {new_balance:.2f}€ ({change_symbol} {balance_change:+.2f}€)"
        if "new_stress" in stats:
            new_stress = stats["new_stress"]
            stress_change = new_stress - old_stress
            change_symbol = "📈" if stress_change > 0 else "📉" if stress_change < 0 else "➡️"
            narrative += f"\n😰 Stress : {new_stress}/100 ({change_symbol} {stress_change:+d})"
        if "new_fun" in stats:
            new_fun = stats["new_fun"]
            fun_change = new_fun - old_fun
            change_symbol = "📈" if fun_change > 0 else "📉" if fun_change < 0 else "➡️"
            narrative += f"\n😄 Fun : {new_fun}/100 ({change_symbol} {fun_change:+d})"
        if "new_salary" in stats:
            new_salary = stats["new_salary"]
            salary_change = new_salary - old_salary
            change_symbol = "📈" if salary_change > 0 else "📉" if salary_change < 0 else "➡️"
            narrative += f"\n💼 Salaire : {new_salary:.0f}€/mois ({change_symbol} {salary_change:+.0f}€)"
        if "new_rent" in stats:
            new_rent = stats["new_rent"]
            rent_change = new_rent - old_rent
            change_symbol = "📈" if rent_change > 0 else "📉" if rent_change < 0 else "➡️"
            narrative += f"\n🏠 Loyer : {new_rent:.0f}€/mois ({change_symbol} {rent_change:+.0f}€)"
    
    st.session_state.history.append(("assistant", narrative))
    
    st.rerun()

# Bouton Avance Rapide
if st.button("⏩ Terminer le mois (+ Salaire & Loyers)", key="advance_month_btn"):
    stats = game.advance_month()
    summary = f"📅 **Mois terminé !** Salaire reçu ({stats['current_salary']}€). Loyer payé ({stats['current_rent']}€). Intérêts gagnés : {stats['interests_earned']:.2f}€."
    
    # Ajouter les rendements d'investissement
    if stats['investment_returns'] > 0:
        summary += f"\n💰 Rendements d'investissements : +{stats['investment_returns']:.2f}€"
    elif stats['investment_returns'] < 0:
        summary += f"\n⚠️ Pertes d'investissements : {stats['investment_returns']:.2f}€"
    
    # Afficher les résolutions de demandes
    if stats['request_resolutions']:
        summary += "\n\n📬 **Réponses à vos demandes :**"
        for res in stats['request_resolutions']:
            request = res['request']
            summary += f"\n- **{request['type'].upper()}** : {request['description']}"
    
    # Afficher l'événement si un s'est produit
    if stats['event']:
        event = stats['event']
        summary += f"\n\n🎲 **Événement : {event['name']}**\n{event['description']}"
        summary += f"\n- Balance : {event['impact']['balance_change']:+.0f}€"
        if event['impact']['stress_change'] != 0:
            summary += f"\n- Stress : {event['impact']['stress_change']:+d}"
        if event['impact'].get('fun_change', 0) != 0:
            summary += f"\n- Fun : {event['impact']['fun_change']:+d}"
    
    st.session_state.history.append(("assistant", summary))
    st.rerun()