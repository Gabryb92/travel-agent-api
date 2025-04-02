# 📦Avvio del progetto con Poetry

Questo progetto utilizza Poetry per la gestione delle dipendenze e dell’ambiente virtuale.

## ⚠️ Attenzione!

Per questo progetto sono previste delle chiavi api di **OpenAi** e di **SerpApi**, non puoi procedere senza! Successivamente trovi i passaggi per crearle e inserire nel .env

---

## ✅ Requisiti comuni

- Python 3.8 o superiore

- Git

### 🪟 Windows

#### 1. Installa Python

- Scaricalo da python.org

- ✅ Spunta “Add Python to PATH” durante l’installazione

#### 2. Installa Poetry

- Apri PowerShell e lancia:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Chiudi e riapri il terminale per aggiornare il PATH.

#### 3. Avvia il progetto

```powershell
git clone https://github.com/Gabryb92/travel-agent-api
cd travel-agent-api
poetry install
poetry env activate
```

---

### 🍏 macOS

#### 1. Installa Python (se non lo hai già)

Con Homebrew:

```bash
brew install python
```

#### 2. Installa Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Assicurati che ~/.local/bin sia nel tuo PATH:**

```bash

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

#### 3. Avvia il progetto

```bash
git clone https://github.com/Gabryb92/travel-agent-api
cd travel-agent-api
poetry install
eval $(poetry env activate)
```

---

### 🐧 Linux

#### 1. Installa Python

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

#### 2. Installa Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 3.Aggiungi Poetry al PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

(o .zshrc se usi Zsh)

#### 4. Avvia il progetto

```bash
git clone https://github.com/Gabryb92/travel-agent-api
cd travel-agent-api
poetry install
eval $(poetry env activate)
```

---

# 🔐 Configurazione delle API

Questo progetto richiede due chiavi API:

1. OpenAI API Key – per generare contenuti

2. SerpAPI API Key – per effettuare ricerche Google

## 📝 Come ottenerle

**OpenAI**

- Vai su 👉 https://platform.openai.com/account/api-keys

- Accedi con il tuo account

- Clicca su "Create new secret key"

- Copia la chiave generata

**SerpAPI**

- Vai su 👉 https://serpapi.com/manage-api-key

- Crea un account (se non ne hai uno)

- Segui la procedure per il piano free e troverai la tua chiave nella dashboard

## 📁 Inseriscile nel file .env

Copia il .env.example nella root del progetto con il comando:

```bash
cp .env.example .env
```

Aggiungi le chiavi generate:

```dotenv
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
SERPAPI_API_KEY="YOUR_SERPAPI_API_KEY"
```

---

# 🌐 Configurazione dei domini frontend (CORS)

Per motivi di sicurezza, il backend accetta richieste solo da determinati domini (origins). Puoi specificare i tuoi domini frontend autorizzati nel file .env.

🔧 Esempio
Nel file .env, aggiungi o modifica questa riga:

```env
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Puoi elencare più domini separati da virgole, ad esempio:

```env
CORS_ORIGINS=https://ilmiosito.it,https://frontend.local
```

### 📌 Se lasci la variabile vuota o ometti il campo, nessun dominio sarà autorizzato.

---
