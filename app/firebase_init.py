# firebase_init.py
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase (se ainda não foi inicializado)
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\Thais\OneDrive\Área de Trabalho\First\NeoAgent\app\credentials.json")
    firebase_admin.initialize_app(cred)
    
    # Exporta o Firestore
db = firestore.client()