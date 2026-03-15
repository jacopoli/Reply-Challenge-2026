"""
Module de gestion persistante des données utilisateur (JSON)
Permet de sauvegarder et charger l'état du jeu dans des fichiers JSON
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# Répertoire de stockage des données
DATA_DIR = Path("./user_data")

def ensure_data_dir():
    """Crée le répertoire de stockage s'il n'existe pas"""
    DATA_DIR.mkdir(exist_ok=True)

def get_user_file(user_id: str) -> Path:
    """Retourne le chemin du fichier utilisateur"""
    ensure_data_dir()
    return DATA_DIR / f"{user_id}.json"

def save_game_state(user_id: str, game_state: Dict[str, Any]) -> bool:
    """
    Sauvegarde l'état du jeu dans un fichier JSON
    
    Args:
        user_id: Identifiant unique de l'utilisateur
        game_state: Dictionnaire contenant l'état du jeu
        
    Returns:
        bool: True si succès, False si erreur
    """
    try:
        file_path = get_user_file(user_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def load_game_state(user_id: str) -> Dict[str, Any] | None:
    """
    Charge l'état du jeu depuis un fichier JSON
    
    Args:
        user_id: Identifiant unique de l'utilisateur
        
    Returns:
        dict: L'état du jeu, ou None si le fichier n'existe pas
    """
    try:
        file_path = get_user_file(user_id)
        if not file_path.exists():
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return None

def delete_user_data(user_id: str) -> bool:
    """
    Supprime les données d'un utilisateur
    
    Args:
        user_id: Identifiant unique de l'utilisateur
        
    Returns:
        bool: True si succès, False si erreur
    """
    try:
        file_path = get_user_file(user_id)
        if file_path.exists():
            file_path.unlink()
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        return False

def list_users() -> list[str]:
    """
    Liste tous les utilisateurs sauvegardés
    
    Returns:
        list: Liste des user_id
    """
    ensure_data_dir()
    return [f.stem for f in DATA_DIR.glob("*.json")]

def user_exists(user_id: str) -> bool:
    """Vérifie si un utilisateur existe"""
    return get_user_file(user_id).exists()
