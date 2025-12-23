# LiveKit Voice Agents 

Drei verschiedene LiveKit Voice AI Agents für unterschiedliche Anwendungsfälle - von einfach bis DSGVO-konform.

## 🎯 Übersicht

Dieses Projekt enthält drei Voice Agents mit unterschiedlichen Komplexitätsstufen:

| Agent | Use Case | Provider | DSGVO |
|-------|----------|----------|-------|
| **Basic Agent** | Einfacher Test-Agent | OpenAI + Deepgram | ❌ |
| **n8n Tool Agent** | Agent mit n8n Integration | OpenAI + Deepgram | ❌ |
| **DSGVO Agent** | Production-ready für EU | Azure Services | ✅ |

## 📋 Voraussetzungen

- Python 3.9 oder höher
- UV Package Manager (empfohlen) oder pip
- API Keys (je nach Agent)

## 🚀 Quick Start

### 1. Dependencies installieren

```bash
uv sync
```

### 2. Environment Variables einrichten

```bash
cp .env.example .env
```

Trage deine API Keys in `.env` ein (siehe unten für Details)

### 3. Model Files downloaden

```bash
# Für alle Agents einmalig ausführen
uv run python livekit_basic_agent.py download-files
```

### 4. Agent starten

```bash
# Basic Agent (einfachster Start)


# n8n Tool Agent (mit Webhook Integration)
uv run python livekit_agent_n8n_tool.py console

# DSGVO Agent (für Production)
uv run python livekit_agent_dsgvo.py console
```

## 🤖 Die drei Agents

### 1. Basic Agent (`livekit_basic_agent.py`)

**Der einfachste Einstieg** - Minimale Konfiguration für erste Tests.

**Features:**
- ✅ Einfachste Konfiguration
- ✅ Schneller Start ohne viel Setup
- ✅ Deutsche Sprache (Deepgram STT)
- ✅ OpenAI GPT-4.1-mini
- ✅ OpenAI Echo Voice

**Benötigte API Keys:**
- `OPENAI_API_KEY`
- `DEEPGRAM_API_KEY`

**Use Case:** Lokales Testen, Entwicklung, Demos

**Start:**
```bash
uv run python livekit_basic_agent.py console
```

---

### 2. n8n Tool Agent (`livekit_agent_n8n_tool.py`)

**Agent mit Tool Integration** - Verbindung zu n8n Workflows.

**Features:**
- ✅ Webhook Tool für n8n Integration
- ✅ Beispiel: Kalender-Abfragen via n8n
- ✅ Erweiterbar für beliebige Workflows
- ✅ Deutsche Sprache
- ✅ 30 Sekunden Timeout für n8n

**Benötigte API Keys:**
- `OPENAI_API_KEY`
- `DEEPGRAM_API_KEY`
- `N8N_WEBHOOK_URL` (deine n8n Webhook URL)

**Tool Beispiel:**
```python
@function_tool
async def send_to_webhook(self, context: RunContext, message: str) -> str:
    """Nutzen um Auskunft über die nächsten Termine zu bekommen."""
    # Sendet Anfrage an n8n Workflow
```

**Use Case:** Automatisierung mit n8n, Kalender-Integration, Business-Prozesse

**Start:**
```bash
uv run python livekit_agent_n8n_tool.py console
```

---

### 3. DSGVO Agent (`livekit_agent_dsgvo.py`)

**Production-ready & DSGVO-konform** - Komplett mit Azure EU Services.

**Features:**
- ✅ **100% DSGVO-konform** (alle Server in EU)
- ✅ Azure Speech STT (Germany West Central)
- ✅ Azure OpenAI LLM (EUR Region)
- ✅ Azure Speech TTS mit deutschen Stimmen
- ✅ n8n Webhook Integration
- ✅ Bereit für Telefonie-Integration (Twilio SIP)

**Benötigte API Keys:**
- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT_NAME`
- `N8N_WEBHOOK_URL` (optional)

**Deutsche Stimmen (auswählbar):**
- `de-DE-KatjaNeural` (Standard - weiblich, freundlich)
- `de-DE-ConradNeural` (männlich, professionell)
- `de-DE-FlorianMultilingualNeural` (HD Qualität)
- `de-DE-AmalaNeural` (weiblich, warm)
- `de-DE-KasperNeural` (männlich, dynamisch)

**DSGVO Compliance:**
| Service | Region | Status |
|---------|--------|--------|
| Azure Speech STT | Germany West Central | ✅ |
| Azure OpenAI LLM | EUR (Sweden Central) | ✅ |
| Azure Speech TTS | Germany West Central | ✅ |
| Agent Processing | Lokal (dein Mac) | ✅ |

**Use Case:** Production, Telefonie, EU-Kunden, DSGVO-Anforderungen

**Start:**
```bash
uv run python livekit_agent_dsgvo.py console
```

## 🔧 Environment Variables

### .env.example

Kopiere `.env.example` zu `.env` und fülle die Keys aus:

```bash
# ===================================
# Basic Agent + n8n Tool Agent
# ===================================

# OpenAI (Required für Basic + n8n Agent)
OPENAI_API_KEY=dein-openai-key

# Deepgram (Required für Basic + n8n Agent)
DEEPGRAM_API_KEY=dein-deepgram-key

# n8n Webhook (Optional - nur für n8n Tool Agent)
N8N_WEBHOOK_URL=https://deine-n8n-url.com/webhook/deine-id

# ===================================
# DSGVO Agent (Azure Services)
# ===================================

# Azure Speech Services (Germany West Central)
AZURE_SPEECH_KEY=dein-azure-speech-key
AZURE_SPEECH_REGION=germanywestcentral

# Azure OpenAI (EUR Region)
AZURE_OPENAI_API_KEY=dein-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://dein-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# ===================================
# Optional: LiveKit Cloud Deployment
# ===================================

LIVEKIT_URL=wss://dein-projekt.livekit.cloud
LIVEKIT_API_KEY=dein-livekit-key
LIVEKIT_API_SECRET=dein-livekit-secret

# ===================================
# Optional: Development Settings
# ===================================

LLM_CHOICE=gpt-4.1-mini
LOG_LEVEL=INFO
```

## 📦 Dependencies installieren

### Alle Dependencies auf einmal:

```bashuv run python livekit_basic_agent.py console
uv sync
```

### Oder manuell für spezifische Agents:

```bash
# Für Basic + n8n Agent
uv add livekit-agents livekit-plugins-openai livekit-plugins-deepgram livekit-plugins-silero httpx

# Zusätzlich für DSGVO Agent
uv add livekit-plugins-azure
```

## 🎙️ Stimmen ändern (DSGVO Agent)

In `livekit_agent_dsgvo.py` die Stimme ändern:

```python
tts=azure.TTS(
    speech_key=os.getenv("AZURE_SPEECH_KEY"),
    speech_region=os.getenv("AZURE_SPEECH_REGION"),
    voice="de-DE-ConradNeural",  # <- Hier ändern
)
```

**Verfügbare deutsche Stimmen:**
- `de-DE-KatjaNeural` - Freundlich, weiblich
- `de-DE-ConradNeural` - Professionell, männlich
- `de-DE-AmalaNeural` - Warm, weiblich
- `de-DE-TanjaNeural` - Klar, weiblich
- `de-DE-KasperNeural` - Jung, dynamisch, männlich
- `de-DE-FlorianMultilingualNeural` - HD Qualität, männlich
- `de-DE-SeraphinaMultilingualNeural` - HD Qualität, weiblich

## 🛠️ Eigene Tools hinzufügen

Beispiel für ein neues Tool:

```python
from livekit.agents import function_tool, RunContext

class Assistant(Agent):
    @function_tool
    async def get_weather(self, context: RunContext, city: str) -> str:
        """Hole das Wetter für eine Stadt.
        
        Args:
            city: Name der Stadt (z.B. 'Berlin')
        """
        # Deine Logik hier
        return f"Das Wetter in {city} ist sonnig"
```

## 📞 Telephony Integration (nur DSGVO Agent)

Der DSGVO Agent ist bereit für Telefonie-Integration mit Twilio SIP.

**Setup Schritte:**
1. Twilio Account erstellen
2. Telefonnummer kaufen
3. SIP Trunk konfigurieren
4. LiveKit SIP Bridge einrichten
5. Agent mit Twilio verbinden

Siehe [LiveKit Telephony Docs](https://docs.livekit.io/agents/start/telephony/) für Details.

## 🧪 Testing

### Console Mode (Lokal mit Mikrofon):

```bash
# Mit Mikrofon und Lautsprecher testen
uv run python livekit_agent_dsgvo.py console
```

### LiveKit Cloud (Optional):

```bash
# 1. Authentifizieren
lk cloud auth

# 2. Agent starten
uv run python livekit_agent_dsgvo.py start

# 3. Im Browser testen
# https://agents-playground.livekit.io/
```

## 💰 Kosten Übersicht

### Basic + n8n Agent:
- OpenAI GPT-4.1-mini: ~$0.15 / 1M Tokens
- Deepgram Nova-2: ~$0.0043 / Minute
- **Gesamt: ~€0.01-0.02 / Minute**

### DSGVO Agent:
- Azure Speech STT: ~$1 / Stunde
- Azure OpenAI: ~$0.50 / 1M Tokens
- Azure Speech TTS: ~$15 / 1M Zeichen
- **Gesamt: ~€0.02-0.03 / Minute**

**Free Tiers:**
- Azure Speech: 5 Stunden/Monat kostenlos
- Deepgram: 200$/Monat kostenlos für 12 Monate

## 🐛 Troubleshooting

### Python Version Check:
```bash
python --version  # Muss >= 3.9 sein
```

### API Key Fehler:
- Prüfe ob Keys in `.env` eingetragen sind
- Keine Leerzeichen vor/nach dem Key
- Quotes nicht nötig

### Audio Probleme im Console Mode:
- Mikrofon/Lautsprecher Permissions prüfen
- Audio Device korrekt konfiguriert?
- VAD Sensitivity anpassen

### Azure Speech Fehler:
```bash
# Test ob Keys funktionieren
uv run python -c "
from livekit.plugins import azure
import os
from dotenv import load_dotenv
load_dotenv()
stt = azure.STT(
    speech_key=os.getenv('AZURE_SPEECH_KEY'),
    speech_region=os.getenv('AZURE_SPEECH_REGION'),
    language='de-DE'
)
print('✅ Azure Speech konfiguriert')
"
```

## 📚 Projekt Struktur

```
Livekit_Niklas/
├── livekit_basic_agent.py           # Basic Agent
├── livekit_agent_n8n_tool.py        # n8n Tool Agent
├── livekit_agent_dsgvo.py           # DSGVO Agent
├── pyproject.toml                   # Dependencies
├── .env.example                     # Environment Template
├── .env                             # Deine Keys (nicht committen!)
├── README.md                        # Diese Datei
└── uv.lock                          # Dependency Lock
```

## 🔗 Ressourcen

- [LiveKit Agents Docs](https://docs.livekit.io/agents/)
- [LiveKit Python SDK](https://github.com/livekit/agents)
- [Azure Speech Services](https://azure.microsoft.com/de-de/products/ai-services/ai-speech)
- [Azure OpenAI](https://azure.microsoft.com/de-de/products/ai-services/openai-service)
- [OpenAI Platform](https://platform.openai.com/)
- [Deepgram](https://deepgram.com/)

## 📝 Lizenz

MIT License

## 🙋‍♂️ Support

Bei Fragen oder Problemen:
1. Prüfe die Troubleshooting Section
2. Schaue in die [LiveKit Docs](https://docs.livekit.io/agents/)
3. Erstelle ein Issue in diesem Repo

---

**Empfehlung:** 
- Start mit **Basic Agent** für erste Tests
- Nutze **n8n Tool Agent** für Workflow-Integration
- Wechsle zu **DSGVO Agent** für Production und EU-Kunden

Viel Erfolg! 🚀
```
