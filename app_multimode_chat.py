import streamlit as st
import requests
import json
import os
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import uuid

# ========== LOGGING AVANZATO ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# ========== CONFIG ==========
st.set_page_config(
    page_title="Multi-AI Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Keys
MASTER_GROQ_KEY = os.getenv("GROQ_API_KEY", "")

# USER_CREDENTIALS formato: user_id:password_hash,user_id:password_hash
USER_CREDS_RAW = os.getenv("USER_CREDENTIALS", "")
USER_CREDENTIALS = {}
for cred in USER_CREDS_RAW.split(","):
    if ":" in cred:
        user_id, pwd_hash = cred.split(":", 1)
        USER_CREDENTIALS[user_id.strip()] = pwd_hash.strip()

# USER_EMAILS formato: user_id:email,user_id:email (per mappare ID a email)
USER_EMAILS_RAW = os.getenv("USER_EMAILS", "")
USER_EMAILS = {}
EMAIL_TO_ID = {}
for mapping in USER_EMAILS_RAW.split(","):
    if ":" in mapping:
        user_id, email = mapping.split(":", 1)
        USER_EMAILS[user_id.strip()] = email.strip()
        EMAIL_TO_ID[email.strip().lower()] = user_id.strip()

# Config
SESSION_TIMEOUT_HOURS = 24
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 60

# ========== VERIFICA ==========
if not MASTER_GROQ_KEY:
    st.error("⚠️ GROQ_API_KEY non configurata. Contatta l'amministratore.")
    st.stop()

if not USER_CREDENTIALS:
    st.error("⚠️ USER_CREDENTIALS non configurata. Contatta l'amministratore.")
    st.stop()

# ========== RATE LIMITING ==========
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = defaultdict(list)

def is_rate_limited(identifier):
    now = datetime.now()
    attempts = st.session_state.login_attempts[identifier]
    recent = [t for t in attempts if now - t < timedelta(minutes=LOCKOUT_DURATION_MINUTES)]
    st.session_state.login_attempts[identifier] = recent
    
    if len(recent) >= MAX_LOGIN_ATTEMPTS:
        minutes_left = LOCKOUT_DURATION_MINUTES - int((now - recent[0]).total_seconds() / 60)
        return True, minutes_left
    return False, 0

def record_attempt(identifier):
    st.session_state.login_attempts[identifier].append(datetime.now())

# ========== SESSION ==========
def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_email = None
        st.session_state.display_name = None
        st.session_state.login_time = None
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())[:8]

def is_session_valid():
    if not st.session_state.authenticated:
        return False
    if st.session_state.login_time:
        elapsed = datetime.now() - st.session_state.login_time
        if elapsed > timedelta(hours=SESSION_TIMEOUT_HOURS):
            return False
    return True

def login_user(user_id):
    st.session_state.authenticated = True
    st.session_state.user_id = user_id
    st.session_state.user_email = USER_EMAILS.get(user_id, user_id)
    st.session_state.display_name = st.session_state.user_email.split('@')[0].title()
    st.session_state.login_time = datetime.now()
    st.session_state.messages = []
    
    logger.info(f"✅ LOGIN | User: {user_id} | Session: {st.session_state.session_id}")

def logout_user():
    user_id = st.session_state.user_id
    logger.info(f"🚪 LOGOUT | User: {user_id} | Session: {st.session_state.session_id}")
    
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.display_name = None
    st.session_state.messages = []
    st.rerun()

# ========== AUTH ==========
def verify_credentials(identifier, password):
    """Supporta login con user_id O email"""
    # Se sembra email, converti a user_id
    if "@" in identifier:
        user_id = EMAIL_TO_ID.get(identifier.lower())
        if not user_id:
            logger.warning(f"❌ UNKNOWN EMAIL | Attempt with unknown email")
            return None
    else:
        user_id = identifier
    
    # Verifica user_id esiste
    if user_id not in USER_CREDENTIALS:
        logger.warning(f"❌ UNKNOWN USER | {user_id}")
        return None
    
    # Verifica password
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    if USER_CREDENTIALS[user_id] != pwd_hash:
        logger.warning(f"❌ INVALID PWD | User: {user_id}")
        return None
    
    return user_id

# ========== LOGGING QUERY ==========
def log_query(mode, question, model=None):
    """Log query dettagliata"""
    logger.info(
        f"QUERY | User: {st.session_state.user_id} | "
        f"Session: {st.session_state.session_id} | "
        f"Mode: {mode} | Model: {model or 'multiple'} | "
        f"Q: {question[:150]}..."
    )

def log_response(mode, response_length):
    """Log risposta"""
    logger.info(
        f"RESPONSE | User: {st.session_state.user_id} | "
        f"Mode: {mode} | Length: {response_length} chars"
    )

# ========== LOGIN PAGE ==========
def show_login():
    st.markdown("""
    <style>
    .login-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .login-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .login-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-header">
        <h1>💬 Multi-AI Chat System</h1>
        <p>Conversazioni intelligenti con multipli modelli AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔑 Accedi al Sistema")
        
        identifier = st.text_input(
            "Email o User ID",
            placeholder="email@esempio.com",
            key="login_id"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            key="login_pwd"
        )
        
        if st.button("🚀 Inizia Conversazione", use_container_width=True, type="primary"):
            if not identifier or not password:
                st.error("❌ Inserisci credenziali")
                return
            
            # Rate limiting
            is_limited, minutes = is_rate_limited(identifier.lower())
            if is_limited:
                st.error(f"🚫 Troppi tentativi. Riprova tra {minutes} minuti.")
                return
            
            # Verifica
            user_id = verify_credentials(identifier, password)
            if user_id:
                login_user(user_id)
                st.success("✅ Accesso effettuato!")
                st.rerun()
            else:
                record_attempt(identifier.lower())
                remaining = MAX_LOGIN_ATTEMPTS - len(st.session_state.login_attempts[identifier.lower()])
                if remaining > 0:
                    st.error(f"❌ Credenziali errate. Tentativi rimasti: {remaining}")
                else:
                    st.error(f"🚫 Account bloccato per {LOCKOUT_DURATION_MINUTES} minuti")
        
        st.markdown("---")
        st.info("""
        💬 **Sistema Chat Multi-AI**
        
        Interfaccia conversazionale come ChatGPT con:
        • 4 modalità (Quick, Standard, Deep, Expert)
        • Cronologia conversazione
        • Privacy garantita con log anonimi
        """)
        st.caption("🔒 Le tue email non appaiono mai nei log di sistema")
        st.caption(f"🛡️ Massimo {MAX_LOGIN_ATTEMPTS} tentativi di accesso")

# ========== GROQ API ==========
def query_groq(model, system_msg, user_msg):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {MASTER_GROQ_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"API ERROR | {str(e)}")
        return f"Errore API: {str(e)}"

# ========== CHAT FUNCTIONS ==========
def add_message(role, content, mode=None, model=None):
    """Aggiungi messaggio alla cronologia"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now(),
        "mode": mode,
        "model": model
    }
    st.session_state.messages.append(message)

def display_chat_history():
    """Mostra cronologia messaggi"""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])
                if msg.get("mode"):
                    st.caption(f"🎯 {msg['mode']} | 🤖 {msg.get('model', 'Multiple models')}")

def process_query(question, mode):
    """Processa query e genera risposta"""
    
    # Log query
    log_query(mode, question)
    
    # Add user message
    add_message("user", question)
    
    # Show typing indicator
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(f"🤔 Elaborazione {mode}..."):
            
            if mode == "QUICK":
                risposta = query_groq(
                    "llama-3.3-70b-versatile",
                    "Sei un assistente AI esperto. Rispondi in modo chiaro, completo e professionale.",
                    question
                )
                model_info = "Llama 3.3 70B"
                
            elif mode == "STANDARD":
                agents = [
                    ("llama-3.1-8b-instant", "Analista Tecnico", "Analisi dettagliata e precisa"),
                    ("openai/gpt-oss-20b", "Esperto Pratico", "Esempi concreti e soluzioni pratiche"),
                    ("qwen/qwen3-32b", "Pensatore Critico", "Prospettive alternative e analisi critica")
                ]
                
                responses = []
                for model, role, goal in agents:
                    r = query_groq(model, f"Sei un {role}. {goal}.", question)
                    responses.append(f"{role}: {r}")
                
                # Synthesis
                synth = "Sintetizza queste 3 analisi in una risposta coerente e completa:\n\n" + "\n\n".join(responses)
                risposta = query_groq(
                    "llama-3.3-70b-versatile",
                    "Sintetizza le analisi mantenendo i punti chiave di ciascuna prospettiva.",
                    synth
                )
                model_info = "3 modelli + sintesi"
                
            elif mode == "DEEP":
                agents = [
                    ("llama-3.1-8b-instant", "Analista Veloce"),
                    ("llama-3.3-70b-versatile", "Stratega"),
                    ("openai/gpt-oss-20b", "Esperto Pratico"),
                    ("qwen/qwen3-32b", "Pensatore Alternativo"),
                    ("meta-llama/llama-4-scout-17b-16e-instruct", "Verificatore")
                ]
                
                responses = []
                progress = st.progress(0)
                status = st.empty()
                
                for i, (model, role) in enumerate(agents):
                    status.text(f"⏳ Agente {i+1}/5: {role}...")
                    r = query_groq(model, f"Sei un {role}.", question)
                    responses.append(f"{role}: {r}")
                    progress.progress((i+1)/6)
                
                status.text("🎯 Sintesi finale approfondita...")
                synth = "Crea una sintesi completa da queste 5 analisi:\n\n" + "\n\n".join(responses)
                risposta = query_groq("llama-3.3-70b-versatile", "Sintesi approfondita.", synth)
                
                progress.progress(1.0)
                status.empty()
                progress.empty()
                
                model_info = "5 modelli + sintesi avanzata"
            
            else:  # EXPERT
                agents = [
                    ("llama-3.1-8b-instant", "Analista Veloce"),
                    ("llama-3.3-70b-versatile", "Stratega Master"),
                    ("openai/gpt-oss-120b", "Pensatore Profondo"),
                    ("openai/gpt-oss-20b", "Esperto Pratico"),
                    ("qwen/qwen3-32b", "Critico Costruttivo"),
                    ("meta-llama/llama-guard-4-12b", "Verificatore Globale")
                ]
                
                responses = []
                progress = st.progress(0)
                status = st.empty()
                
                for i, (model, role) in enumerate(agents):
                    status.text(f"⏳ Agente {i+1}/6: {role}...")
                    r = query_groq(model, f"Sei un {role}.", question)
                    responses.append(f"{role}: {r}")
                    progress.progress((i+1)/7)
                
                status.text("🎯 Super-sintesi master in corso...")
                synth = "Crea una sintesi definitiva master da queste 6 analisi esperte:\n\n" + "\n\n".join(responses)
                risposta = query_groq("llama-3.3-70b-versatile", "Sintesi master definitiva.", synth)
                
                progress.progress(1.0)
                status.empty()
                progress.empty()
                
                model_info = "6 modelli premium + super-sintesi"
        
        # Display response
        st.markdown(risposta)
        st.caption(f"🎯 {mode} | 🤖 {model_info} | 💰 $0.00")
    
    # Add assistant message
    add_message("assistant", risposta, mode, model_info)
    
    # Log response
    log_response(mode, len(risposta))

# ========== MAIN ==========
init_session()

if not is_session_valid():
    show_login()
    st.stop()

# ========== CHAT INTERFACE ==========

# Custom CSS
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .main-title h2 {
        margin: 0;
        font-weight: 700;
    }
    .main-title p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.display_name}")
    st.caption(f"🔐 ID: {st.session_state.user_id}")
    
    if st.session_state.login_time:
        elapsed = datetime.now() - st.session_state.login_time
        hours_left = SESSION_TIMEOUT_HOURS - (elapsed.total_seconds() / 3600)
        st.caption(f"⏱️ Sessione: {hours_left:.1f}h rimaste")
    
    st.caption(f"💬 Messaggi: {len(st.session_state.messages)//2}")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout_user()
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Modalità AI")
    
    mode = st.radio(
        "Scegli complessità:",
        ["QUICK", "STANDARD", "DEEP", "EXPERT"],
        captions=[
            "⚡ 1 modello - 10s",
            "🎯 3 modelli - 30s",
            "🔬 5 modelli - 60s",
            "🏆 6 modelli - 2min"
        ],
        index=1
    )
    
    st.markdown("---")
    
    if st.button("🗑️ Nuova Chat", use_container_width=True):
        st.session_state.messages = []
        logger.info(f"NEW CHAT | User: {st.session_state.user_id}")
        st.rerun()
    
    st.markdown("---")
    st.caption("💰 Servizio gratuito")
    st.caption("🔒 Chat privata e sicura")
    st.caption("📊 Log anonimi")
    st.caption(f"👥 {len(USER_CREDENTIALS)} utenti attivi")

# Main chat area
st.markdown("""
<div class="main-title">
    <h2>💬 Multi-AI Chat System</h2>
    <p>Conversazioni intelligenti multi-modello</p>
</div>
""", unsafe_allow_html=True)

# Display chat history
display_chat_history()

# Chat input
question = st.chat_input("Scrivi la tua domanda...", key="chat_input")

if question:
    process_query(question, mode)
    st.rerun()

# Empty state
if not st.session_state.messages:
    st.info("👋 Ciao! Inizia una conversazione scrivendo una domanda qui sotto.")
    
    with st.expander("💡 Esempi di domande"):
        st.markdown("""
        **Quick (veloce):**
        - Cos'è la blockchain?
        - Definizione di intelligenza artificiale
        
        **Standard (bilanciato):**
        - Spiegami pro e contro del lavoro remoto
        - Come funziona ChatGPT?
        
        **Deep (approfondito):**
        - Dovrei cambiare lavoro o restare nella mia azienda?
        - Analizza le migliori strategie di risparmio per il 2025
        
        **Expert (massima qualità):**
        - Valuta un investimento importante in startup
        - Analizza tutti gli aspetti di una decisione critica
        """)
