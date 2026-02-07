# 💬 Multi-AI Chat System - Sistema Sicuro

Sistema di chat intelligente con multipli modelli AI, privacy garantita e interfaccia conversazionale.

## 🌟 Features

### ✅ Sicurezza Avanzata
- **User ID anonimi** - Email nascoste nei log
- **Password hash SHA-256** - Nessuna password in chiaro
- **Rate limiting** - Protezione anti-brute-force
- **Session timeout** - Scadenza automatica sessioni
- **Logging dettagliato** - Tracciamento completo ma anonimo

### ✅ Interfaccia Chat
- **Stile ChatGPT** - Interfaccia conversazionale moderna
- **Cronologia messaggi** - Durante la sessione
- **4 Modalità AI** - Quick, Standard, Deep, Expert
- **Progress indicators** - Feedback in tempo reale

### ✅ Multi-Modello
- **QUICK**: 1 modello (Llama 3.3 70B) - 10 secondi
- **STANDARD**: 3 modelli + sintesi - 30 secondi
- **DEEP**: 5 modelli + sintesi avanzata - 60 secondi
- **EXPERT**: 6 modelli + super-sintesi - 2 minuti

### ✅ Privacy
- Email utenti **MAI** visibili nei log
- Solo user_id anonimi
- Groq API key nascosta
- Nessun dato memorizzato permanentemente

---

## 📦 Contenuto Pacchetto

```
multi-ai-chat-secure/
├── app_multimode_chat.py        # App principale
├── generate_credentials.py      # Script generazione password
├── requirements.txt             # Dipendenze Python
├── README.md                    # Questa guida
└── SETUP_GUIDE.md              # Guida setup dettagliata
```

---

## 🚀 Quick Start

### 1. Genera Credenziali

**Sul tuo computer locale:**

```bash
python generate_credentials.py
```

Questo genera:
- `USER_CREDENTIALS` (user_id:hash)
- `USER_EMAILS` (user_id:email)
- Password per ogni utente

### 2. Configura Render

**Environment Variables:**

```
GROQ_API_KEY = gsk_xxxxx
USER_CREDENTIALS = user001:hash1,user002:hash2,...
USER_EMAILS = user001:email1@example.com,user002:email2@example.com,...
```

### 3. Deploy

```bash
git add .
git commit -m "Initial commit - Multi-AI Chat"
git push
```

Render deploya automaticamente.

### 4. Condividi Credenziali

Invia a ogni utente:
- Email o User ID
- Password personale
- URL app

---

## 📊 Log Format

I log sono completamente anonimi:

```
2026-02-07 10:30:15 | INFO | ✅ LOGIN | User: user001 | Session: a3b5c7d9
2026-02-07 10:30:45 | INFO | QUERY | User: user001 | Session: a3b5c7d9 | Mode: STANDARD | Model: multiple | Q: Dovrei cambiare lavoro?...
2026-02-07 10:31:20 | INFO | RESPONSE | User: user001 | Mode: STANDARD | Length: 1547 chars
2026-02-07 10:35:10 | INFO | QUERY | User: user001 | Session: a3b5c7d9 | Mode: QUICK | Model: llama-3.3-70b | Q: Cos'è Bitcoin?...
2026-02-07 10:40:00 | INFO | 🚪 LOGOUT | User: user001 | Session: a3b5c7d9
```

**Privacy:**
- ❌ Email MAI visibili
- ✅ Solo user_id anonimi
- ✅ Domande complete tracciate
- ✅ Session tracking con UUID

---

## 🔐 Sicurezza

### User ID Anonimi

```
LOGIN: mario@gmail.com → Convertito a → user001
LOG:   User: user001 ← Nessuna email visibile
```

### Password Hash

```
Password: MarioPass2025!
Hash: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

Impossibile recuperare password dall'hash.

### Rate Limiting

- Max 5 tentativi di login
- Blocco 60 minuti dopo superamento
- Protezione brute-force

### Session Timeout

- Sessione valida 24 ore
- Logout automatico scadenza
- Logout manuale disponibile

---

## 👥 Gestione Utenti

### Aggiungere Utente

1. Esegui `generate_credentials.py` con nuovo utente
2. Copia nuovi hash su Render
3. Salva (no redeploy necessario)

### Rimuovere Utente

1. Render → Environment → USER_CREDENTIALS
2. Rimuovi `user_id:hash`
3. Salva

### Cambiare Password

1. Genera nuovo hash per l'utente
2. Sostituisci vecchio hash con nuovo
3. Comunica nuova password all'utente

---

## 📱 Utilizzo

### Login

```
Email: mario@gmail.com
Password: MarioPass2025!
```

Oppure:

```
User ID: user001
Password: MarioPass2025!
```

### Chat

1. Seleziona modalità AI (sidebar)
2. Scrivi domanda
3. Ricevi risposta multi-modello
4. Continua conversazione

### Modalità

- **Quick**: Domande semplici, risposte veloci
- **Standard**: Uso normale, risposta bilanciata
- **Deep**: Analisi complesse, più prospettive
- **Expert**: Decisioni critiche, massima qualità

---

## 🛠️ Configurazione Avanzata

### Modificare Timeout Sessione

Nel file `app_multimode_chat.py`:

```python
SESSION_TIMEOUT_HOURS = 24  # Cambia qui
```

### Modificare Rate Limiting

```python
MAX_LOGIN_ATTEMPTS = 5  # Max tentativi
LOCKOUT_DURATION_MINUTES = 60  # Durata blocco
```

### Aggiungere Modelli

Nella funzione `process_query()`, aggiungi nuovi modelli:

```python
agents.append(("nuovo-modello-id", "Ruolo", "Obiettivo"))
```

---

## 💰 Costi

**Totale: $0/mese**

- Groq API: 14,400 richieste/giorno gratis
- Render: 750 ore/mese gratis
- Nessun costo nascosto

**Se superi limiti gratuiti:**
- Groq: ~$0.27 per 1M token extra
- Render: $7/mese per always-on

---

## ❓ FAQ

**Q: Le email sono sicure?**
A: Sì, mai visibili nei log. Solo user_id anonimi.

**Q: Posso recuperare una password persa?**
A: No, ma puoi generare nuova password e aggiornarla.

**Q: Quanti utenti posso avere?**
A: Illimitati. Nessun limite tecnico.

**Q: I messaggi sono salvati?**
A: Solo durante la sessione. Alla chiusura vengono eliminati.

**Q: Posso vedere cosa chiedono gli utenti?**
A: Sì, nei log Render. Ma non vedi quale utente (email) specifico.

---

## 🆘 Troubleshooting

### Login non funziona

1. Verifica user_id/email corretti
2. Verifica password corretta (case-sensitive)
3. Check rate limiting (max 5 tentativi)

### App non carica

1. Render service in sleep (attendi 30 sec)
2. Check environment variables configurate
3. Verifica log Render per errori

### Errore API

1. Verifica GROQ_API_KEY valida
2. Check quota Groq non esaurita
3. Riprova dopo qualche secondo

---

## 📞 Supporto

Problemi? Verifica:

1. Environment variables corrette
2. Log Render per errori specifici
3. Groq API key valida e attiva
4. Credenziali utente corrette

---

## 📄 Licenza

Uso personale e aziendale consentito.
Non rivendere come servizio standalone.

---

## 🎉 Conclusione

Hai creato un sistema di chat AI:

✅ Sicuro (password hash, user ID anonimi)
✅ Privato (email nascoste, log anonimi)
✅ Potente (fino a 6 modelli AI)
✅ Gratuito ($0/mese uso normale)
✅ Professionale (interfaccia ChatGPT-style)

**Buon utilizzo! 🚀**
