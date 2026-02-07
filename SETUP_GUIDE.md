# 📖 GUIDA SETUP COMPLETA - Multi-AI Chat System

**Guida passo-passo per principianti assoluti**

---

## ⏱️ TEMPO TOTALE: 25 MINUTI

- Parte 1: Generazione credenziali (5 min)
- Parte 2: Upload GitHub (5 min)
- Parte 3: Deploy Render (10 min)
- Parte 4: Test sistema (5 min)

---

# PARTE 1: Generazione Credenziali (5 minuti)

## Step 1.1: Estrai File Progetto

1. [ ] Estrai `multi-ai-chat-secure.zip` sul Desktop
2. [ ] Apri la cartella `multi-ai-chat-secure/`
3. [ ] Verifica presenza file:
   - `app_multimode_chat.py`
   - `generate_credentials.py`
   - `requirements.txt`
   - `README.md`
   - `SETUP_GUIDE.md` (questo file)

---

## Step 1.2: Configura Utenti

1. [ ] Apri `generate_credentials.py` con editor testo (Notepad/TextEdit)
2. [ ] Trova sezione (circa riga 35):

```python
users = [
    {"id": "user001", "email": "mario@gmail.com", "password": "MarioPass2025!"},
    {"id": "user002", "email": "luca@yahoo.it", "password": None},
    {"id": "user003", "email": "famiglia@outlook.com", "password": "FamigliaSecure!"},
]
```

3. [ ] **MODIFICA con i tuoi utenti:**

```python
users = [
    {"id": "user001", "email": "TUA_EMAIL@gmail.com", "password": "TuaPassword123!"},
    {"id": "user002", "email": "amico@email.com", "password": None},  # Auto-genera
    {"id": "user003", "email": "famiglia@email.com", "password": "AltraPassword!"},
]
```

⚠️ **IMPORTANTE:**
- `"id"`: Usa `user001`, `user002`, etc. (NON cambiare formato)
- `"email"`: Email reale dell'utente
- `"password"`: Password personalizzata O `None` per auto-generare

4. [ ] Salva file

---

## Step 1.3: Esegui Script

### Su Windows:

1. [ ] Apri **Command Prompt** (cmd)
2. [ ] Naviga alla cartella:
   ```
   cd Desktop\multi-ai-chat-secure
   ```
3. [ ] Esegui script:
   ```
   python generate_credentials.py
   ```

### Su Mac/Linux:

1. [ ] Apri **Terminal**
2. [ ] Naviga:
   ```bash
   cd ~/Desktop/multi-ai-chat-secure
   ```
3. [ ] Esegui:
   ```bash
   python3 generate_credentials.py
   ```

---

## Step 1.4: Salva Output

Lo script mostra:

```
================================================================================
1️⃣  COPIA QUESTE STRINGHE SU RENDER ENVIRONMENT VARIABLES
================================================================================

Variabile: USER_CREDENTIALS
--------------------------------------------------------------------------------
user001:8d969eef...,user002:f6e0a1e2...,user003:5e884898...

Variabile: USER_EMAILS
--------------------------------------------------------------------------------
user001:mario@gmail.com,user002:luca@yahoo.it,user003:famiglia@outlook.com

================================================================================
2️⃣  CONDIVIDI QUESTE CREDENZIALI CON GLI UTENTI
================================================================================

👤 User ID:  user001
📧 Email:    mario@gmail.com
🔑 Password: MarioPass2025!
...
```

**AZIONI:**

1. [ ] Copia **TUTTA** la stringa `USER_CREDENTIALS` (può essere molto lunga)
2. [ ] Incolla in file `credentials.txt` sul Desktop
3. [ ] Copia **TUTTA** la stringa `USER_EMAILS`
4. [ ] Incolla sotto `USER_CREDENTIALS`
5. [ ] Copia tutte le password utenti
6. [ ] Incolla sotto

**File `credentials.txt` finale:**

```
USER_CREDENTIALS=user001:hash1,user002:hash2,user003:hash3

USER_EMAILS=user001:email1@gmail.com,user002:email2@yahoo.it

UTENTI:
user001: mario@gmail.com - Password: MarioPass2025!
user002: luca@yahoo.it - Password: vK9$mP2xL4wR8nQ3
user003: famiglia@outlook.com - Password: FamigliaSecure!
```

6. [ ] Salva `credentials.txt` in posto sicuro

⚠️ **NON caricare `credentials.txt` su GitHub!**

---

# PARTE 2: Upload su GitHub (5 minuti)

## Step 2.1: Crea Repository

1. [ ] Vai su **github.com** → Login
2. [ ] Clicca **'+'** in alto a destra → **'New repository'**
3. [ ] Configura:
   - Repository name: `multi-ai-chat`
   - Description: `Sistema chat multi-AI sicuro`
   - **Public** ← IMPORTANTE
   - **NON** spuntare "Add README" (ce l'hai già)
4. [ ] Clicca **'Create repository'**

---

## Step 2.2: Upload File

1. [ ] Nella pagina nuova repository, clicca **'uploading an existing file'**
2. [ ] Trascina questi file dalla cartella `multi-ai-chat-secure/`:
   - `app_multimode_chat.py`
   - `requirements.txt`
   - `README.md`
   - `SETUP_GUIDE.md`
3. [ ] **NON caricare:**
   - ❌ `generate_credentials.py` (solo uso locale)
   - ❌ `credentials.txt` (se creato)
4. [ ] Commit message: `Initial commit - Secure chat system`
5. [ ] Clicca **'Commit changes'**
6. [ ] Verifica 4 file visibili nel repository ✅

---

# PARTE 3: Deploy su Render (10 minuti)

## Step 3.1: Connetti Repository

1. [ ] Vai su **render.com** → Login (con GitHub)
2. [ ] Dashboard → Clicca **'New +'** → **'Web Service'**
3. [ ] Render mostra lista repository GitHub
4. [ ] Trova **'multi-ai-chat'** → Clicca **'Connect'**

---

## Step 3.2: Configura Servizio

**Compila ESATTAMENTE:**

| Campo | Valore |
|-------|--------|
| **Name** | `multi-ai-chat` |
| **Region** | Frankfurt (o più vicino) |
| **Branch** | `main` |
| **Root Directory** | *(lascia vuoto)* |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app_multimode_chat.py --server.port $PORT --server.address 0.0.0.0` |
| **Instance Type** | **Free** ⚠️ IMPORTANTE |

---

## Step 3.3: Environment Variables

**CRITICO - Configura con attenzione!**

1. [ ] Scorri a sezione **'Environment Variables'**
2. [ ] Clicca **'Add Environment Variable'** (3 volte)

### Variabile 1: GROQ_API_KEY

```
Key: GROQ_API_KEY
Value: [TUA CHIAVE GROQ - gsk_xxxxx]
```

💡 Se non hai chiave Groq:
1. Vai su console.groq.com
2. Sign up → API Keys → Create
3. Copia chiave

### Variabile 2: USER_CREDENTIALS

```
Key: USER_CREDENTIALS
Value: [COPIA DA credentials.txt]
```

⚠️ **IMPORTANTE:**
- Copia TUTTA la stringa hash (può essere 500+ caratteri)
- NON aggiungere spazi
- NON andare a capo

**Esempio:**
```
user001:8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92,user002:f6e0a1e2ac41945a9aa7ff8a8aaa0cebc12a3bcc981a929ad5cf810a090e11ae
```

### Variabile 3: USER_EMAILS

```
Key: USER_EMAILS
Value: [COPIA DA credentials.txt]
```

**Esempio:**
```
user001:mario@gmail.com,user002:luca@yahoo.it,user003:famiglia@outlook.com
```

3. [ ] Verifica tutte e 3 le variabili
4. [ ] Clicca **'Save Changes'**

---

## Step 3.4: Deploy!

1. [ ] Scorri in fondo
2. [ ] Clicca **'Create Web Service'** (pulsante blu grande)
3. [ ] **Attendi deploy** (2-4 minuti)
   - Vedrai console con log di installazione
   - Quando appare **'Live'** con pallino verde → PRONTO ✅
4. [ ] **COPIA URL** che appare in alto
   - Esempio: `https://multi-ai-chat-xxxx.onrender.com`
5. [ ] Salva URL in `credentials.txt`

---

# PARTE 4: Test Sistema (5 minuti)

## Step 4.1: Primo Accesso

1. [ ] Apri URL app nel browser
2. [ ] **Prima apertura**: attendi 30-60 secondi (servizio si attiva)
3. [ ] Dovresti vedere **pagina login** con:
   - Header gradient viola "Multi-AI Chat System"
   - Campo "Email o User ID"
   - Campo "Password"
   - Pulsante "Inizia Conversazione"

Se vedi questa pagina → **Setup OK!** ✅

---

## Step 4.2: Test Login

**Test Utente 1:**

1. [ ] Email: `[email primo utente da credentials.txt]`
2. [ ] Password: `[password primo utente]`
3. [ ] Clicca **'Inizia Conversazione'**
4. [ ] Dovresti vedere:
   - ✅ "Accesso effettuato!"
   - ✅ Interfaccia chat
   - ✅ Sidebar con nome utente
   - ✅ Campo input "Scrivi la tua domanda..."

Se vedi interfaccia chat → **Login OK!** ✅

---

## Step 4.3: Test Chat

1. [ ] Sidebar → Modalità: **STANDARD** (default)
2. [ ] Campo input → Scrivi: `Cos'è l'intelligenza artificiale?`
3. [ ] Premi Enter
4. [ ] Dovresti vedere:
   - ✅ Tuo messaggio appare in chat
   - ✅ "🤔 Elaborazione STANDARD..."
   - ✅ Dopo 20-30 sec: risposta AI appare
   - ✅ Caption: "🎯 STANDARD | 🤖 3 modelli + sintesi"

Se ricevi risposta → **Sistema funziona!** ✅

---

## Step 4.4: Test Modalità

**Test Quick (veloce):**

1. [ ] Sidebar → Seleziona **QUICK**
2. [ ] Domanda: `Cosa significa blockchain?`
3. [ ] Risposta in ~10 secondi ✅

**Test Deep (approfondito):**

1. [ ] Sidebar → Seleziona **DEEP**
2. [ ] Domanda: `Dovrei investire in criptovalute?`
3. [ ] Vedi progress bar con agenti
4. [ ] Risposta in ~60 secondi ✅

---

## Step 4.5: Test Sicurezza

### Test 1: Email Non Autorizzata

1. [ ] Logout (sidebar → pulsante Logout)
2. [ ] Login con email NON in lista utenti
3. [ ] Password qualsiasi
4. [ ] Dovresti vedere: **❌ Credenziali errate** ✅

### Test 2: Password Sbagliata

1. [ ] Email corretta (utente autorizzato)
2. [ ] Password SBAGLIATA
3. [ ] Dovresti vedere: **❌ Credenziali errate. Tentativi rimasti: 4** ✅

### Test 3: Rate Limiting

1. [ ] Prova 5 volte con password sbagliata
2. [ ] Al 6° tentativo: **🚫 Troppi tentativi. Riprova tra 60 minuti** ✅

---

## Step 4.6: Verifica Log Anonimi

**Su Render:**

1. [ ] Dashboard → Servizio `multi-ai-chat`
2. [ ] Tab laterale → **Logs**
3. [ ] Scorri e cerca righe tipo:

```
✅ LOGIN | User: user001 | Session: a3b5c7d9
QUERY | User: user001 | Session: a3b5c7d9 | Mode: STANDARD | Q: Cos'è...
```

**Verifica:**
- ✅ Vedi `user001` (NON email)
- ✅ Privacy garantita
- ✅ Domande tracciate
- ✅ Session ID univoco

---

# PARTE 5: Condividi con Utenti (5 minuti)

## Step 5.1: Prepara Email

Per ogni utente, invia:

```
Oggetto: Accesso Multi-AI Chat System

Ciao [Nome],

Hai accesso al sistema Multi-AI Chat! Ecco le tue credenziali:

🌐 URL: https://multi-ai-chat-xxxx.onrender.com

Puoi accedere con:
📧 Email: tua.email@example.com
🔐 User ID: user001

🔑 Password: [Password Personale]

COME FUNZIONA:
1. Apri URL
2. Inserisci email (o user_id) e password
3. Scegli modalità AI (Quick/Standard/Deep/Expert)
4. Inizia a chattare!

MODALITÀ:
- QUICK: Risposte veloci (10s)
- STANDARD: Uso normale (30s)
- DEEP: Analisi profonda (60s)
- EXPERT: Massima qualità (2min)

💰 Servizio gratuito
🔒 Chat privata e sicura
📱 Funziona su qualsiasi dispositivo

Per domande: rispondi a questa email

Buona chat! 🚀
```

---

## Step 5.2: Istruzioni Utente

Includi queste istruzioni base:

```
GUIDA RAPIDA:

1. LOGIN
   - Vai su [URL app]
   - Inserisci email e password
   - Clicca "Inizia Conversazione"

2. CHAT
   - Scrivi domanda nel campo in basso
   - Premi Enter
   - Attendi risposta AI

3. MODALITÀ (seleziona in sidebar):
   - Quick = veloce
   - Standard = bilanciato (consigliato)
   - Deep = approfondito
   - Expert = massima qualità

4. NUOVA CHAT
   - Clicca "Nuova Chat" in sidebar
   - Cancella cronologia

5. LOGOUT
   - Clicca "Logout" in sidebar quando finito

PROBLEMI?
- Password dimenticata? Contattami
- App non carica? Attendi 30 secondi e ricarica
- Altro? Scrivi a [tua email]
```

---

# ✅ CHECKLIST FINALE

Prima di considerare setup completato:

## GitHub
- [ ] Repository creato
- [ ] 4 file caricati (app, requirements, README, SETUP_GUIDE)
- [ ] Repository pubblico
- [ ] NO file credenziali caricati

## Render
- [ ] Servizio web creato
- [ ] Instance Type = FREE
- [ ] 3 Environment Variables configurate:
  - [ ] GROQ_API_KEY
  - [ ] USER_CREDENTIALS
  - [ ] USER_EMAILS
- [ ] Deploy completato (status "Live")
- [ ] URL copiato e salvato

## Test
- [ ] Login con email funziona
- [ ] Login con user_id funziona
- [ ] Chat riceve risposte
- [ ] Modalità QUICK testata
- [ ] Modalità STANDARD testata
- [ ] Email NON autorizzata rifiutata
- [ ] Password sbagliata rifiutata
- [ ] Rate limiting attivo dopo 5 tentativi
- [ ] Log mostrano user_id (NON email)

## Sicurezza
- [ ] Password salvate in luogo sicuro
- [ ] `credentials.txt` NON su GitHub
- [ ] `generate_credentials.py` NON su GitHub
- [ ] Log verificati (solo user_id visibili)

## Utenti
- [ ] Email con credenziali preparata
- [ ] Istruzioni utente incluse
- [ ] URL app condiviso
- [ ] Password individuali comunicate

---

# 🎉 CONGRATULAZIONI!

Hai completato il setup di un sistema di chat AI:

✅ **Sicuro** - Password hash, user ID anonimi, rate limiting
✅ **Privato** - Email nascoste, log anonimi
✅ **Potente** - Fino a 6 modelli AI consultabili
✅ **Gratuito** - $0/mese per uso normale
✅ **Professionale** - Interfaccia moderna ChatGPT-style
✅ **Multi-utente** - Gestione granulare utenti
✅ **Tracciabile** - Log completi ma anonimi

---

# 🆘 TROUBLESHOOTING

## Problema: Deploy Fallisce

**Sintomi:** Render mostra "Deploy failed"

**Soluzioni:**
1. Verifica `requirements.txt` caricato correttamente
2. Check Start Command corretto:
   ```
   streamlit run app_multimode_chat.py --server.port $PORT --server.address 0.0.0.0
   ```
3. Verifica nome file: `app_multimode_chat.py` (non `app.py`)

---

## Problema: Login Non Funziona

**Sintomi:** Sempre "Credenziali errate"

**Soluzioni:**
1. Verifica Environment Variables su Render:
   - USER_CREDENTIALS ha hash corretti
   - USER_EMAILS ha mappature corrette
2. Password è case-sensitive (maiuscole/minuscole)
3. Prova con user_id invece di email
4. Rigenera credenziali se necessario

---

## Problema: Chat Non Risponde

**Sintomi:** Spinner infinito o errore

**Soluzioni:**
1. Verifica GROQ_API_KEY valida:
   - Vai su console.groq.com
   - Verifica chiave attiva
   - Genera nuova se necessario
2. Check quota Groq non esaurita:
   - console.groq.com → Usage
   - Limite: 14,400 richieste/giorno
3. Prova modalità QUICK (più semplice)
4. Check log Render per errori API

---

## Problema: "App Unavailable"

**Sintomi:** Schermata grigia "Application Error"

**Soluzioni:**
1. Servizio in sleep mode (free tier):
   - Attendi 30-60 secondi
   - Ricarica pagina
2. Check Render dashboard:
   - Servizio deve essere "Live"
   - Se "Deploying", attendi
3. Verifica log per errori startup

---

## Problema: Rate Limiting Bloccato

**Sintomi:** "Bloccato per 60 minuti" ma sei tu

**Soluzioni:**
1. Attendi effettivamente 60 minuti
2. Oppure: contatta admin per reset
3. Usa email diversa temporaneamente
4. In app, cambia `LOCKOUT_DURATION_MINUTES` se necessario

---

# 📞 SUPPORTO

Se problemi persistono:

1. **Check log Render:**
   - Dashboard → Servizio → Logs
   - Cerca righe con "ERROR"
   - Copia e conserva per debug

2. **Verifica configurazione:**
   - GitHub: 4 file presenti
   - Render: 3 environment variables
   - Groq: API key valida

3. **Test base:**
   - Esegui `generate_credentials.py` di nuovo
   - Verifica hash generati correttamente
   - Riconfigura Render se necessario

---

# 📚 PROSSIMI PASSI

Ora che hai il sistema funzionante:

1. **Personalizza**
   - Cambia colori gradient nel CSS
   - Aggiungi modelli AI
   - Modifica timeout sessione

2. **Espandi**
   - Aggiungi più utenti
   - Crea gruppi utenti
   - Integra altri servizi

3. **Monitora**
   - Check log regolarmente
   - Verifica utilizzo Groq
   - Aggiorna credenziali periodicamente

4. **Migliora**
   - Raccogli feedback utenti
   - Ottimizza prompt AI
   - Aggiungi features

---

**Fine Guida Setup** ✅

Buon utilizzo del tuo sistema Multi-AI Chat! 🚀
