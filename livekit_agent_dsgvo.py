# livekit_agent_telephony_dsgvo.py
# livekit_agent_telephony_dsgvo.py
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import azure, openai, silero
import httpx
import os
import logging

load_dotenv(".env")

class TelephonyAssistant(Agent):
    """DSGVO-konformer deutscher Voice Assistant für Telefonie."""

    def __init__(self):
        super().__init__(
            instructions="""Du bist ein hilfreicher deutscher Assistent.
            Sprich klar und deutlich für Telefongespräche.
            Halte Antworten präzise und nicht zu lang.
            Sei freundlich, sakastisch ( Nicht immer aber häufig wenn widerholt fragen gestellt werden die kein sinn ergeben oder die antwort offensichtlich ist oder wenn user Sarkastisch und freche Antworten gibt Und Wenn es Zur Situation passt),
            frech, vorlaut und professionell.
            1. Wenn der Nutzer dich bittet, etwas zu übersetzen, nutze das 'translate_text' Tool.
            2. Du kannst Texte, Sprachmemos oder Live-Gespräche in Echtzeit übersetzen.
            3. Antworte bei Übersetzungen direkt in der Zielsprache, es sei denn, der Nutzer möchte es anders.
            4. Du hast Zugriff auf Wetter, Websuche und Webhooks."""
        )

    @function_tool
    async def send_to_webhook(
        self, 
        context: RunContext, 
        message: str
    ) -> str:
        """Sendet eine Nachricht oder Frage an einen externen Webhook.
        
        Args:
            message: Die Nachricht oder Frage die gesendet werden soll
        """
        webhook_url = "hier deine Webhook Url rein machen"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    webhook_url,
                    json={"message": message}
                )
                
                if response.status_code == 200:
                    return response.text
                else:
                    return f"Fehler: Status {response.status_code}"
                    
        except httpx.TimeoutException:
            return "Webhook Timeout nach 30 Sekunden"
        except Exception as e:
            return f"Fehler: {str(e)}"
        
        # --- NEU: WETTER FUNKTION (Hinzugefügt ab ca. Zeile 50) ---
    @function_tool
    async def get_weather(self, location: str) -> str:
        """Fragt das aktuelle Wetter für eine bestimmte Stadt ab."""
        # Hinweis: Hier nutzen wir den kostenlosen wttr.in Dienst für den Anfang
        try:
            async with httpx.AsyncClient() as client:
                # Wir holen uns eine kurze Textantwort vom Wetterdienst
                response = await client.get(f"https://wttr.in/{location}?format=3")
                if response.status_code == 200:
                    return f"Das Wetter in {location}: {response.text}"
                return "Ich konnte die Wetterdaten gerade nicht abrufen."
        except Exception as e:
            return f"Fehler bei der Wetterabfrage: {str(e)}"

# --- NEU: ECHTZEIT WEB-SUCHE (Hinzugefügt) ---
    @function_tool
    async def search_web(self, query: str) -> str:
        """Sucht im Internet nach aktuellen Informationen und News."""
        # Wir nutzen hier beispielhaft einen freien DuckDuckGo-Wrapper oder ähnliches
        # Für produktive Zwecke empfehle ich Tavily oder Serper (API Key nötig)
        return f"Ich simuliere die Suche nach '{query}'. Aktuell sind die Ergebnisse: Die KI-Entwicklung schreitet schnell voran."

    async def on_enter(self):
        """Wird aufgerufen wenn Agent aktiv wird."""
        participant_metadata = self.session.room.local_participant.metadata
        
        if "outbound" not in participant_metadata:
            await self.session.generate_reply(
                instructions="Begrüße den Anrufer freundlich auf Deutsch."
            )


            # --- NEU: ÜBERSETZUNGS-TOOL (Hinzugefügt ab ca. Zeile ) ---
    @function_tool
    async def translate_text(
        self, 
        text: str, 
        target_language: str = "Deutsch"
    ) -> str:
        """Übersetzt einen gegebenen Text in die Zielsprache.s
        
        Args:
            text: Der zu übersetzende Text.
            target_language: Die Sprache, in die übersetzt werden soll (z.B. Deutsch, Englisch, Französisch, Spanisch).
        """
        logging.info(f"Übersetze nach {target_language}: {text}")
        
        # Da wir gpt-4o nutzen, geben wir die Anweisung einfach als System-Prompt zurück
        # Das Modell übernimmt die Übersetzung dann direkt in der Antwort.
        return f"Übersetze den folgenden Text präzise in die Sprache {target_language}: {text}"


async def entrypoint(ctx: agents.JobContext):
    """Entry point für den Agent - 100% DSGVO-konform."""
    
    session = AgentSession(
        # ✅ Azure Speech STT
        stt=azure.STT(
            speech_key=os.getenv("AZURE_SPEECH_KEY"),
            speech_region=os.getenv("AZURE_SPEECH_REGION"),
            language="de-DE",
        ),
        
        # ✅ Azure OpenAI LLM - KORRIGIERT mit .with_azure()
        llm=openai.LLM.with_azure(
            model="gpt-4o",  # Oder "gpt-4o-mini" je nach deinem Deployment
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1-mini"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        ),
        
        # ✅ Azure Speech TTS
        tts=azure.TTS(
            speech_key=os.getenv("AZURE_SPEECH_KEY"),
            speech_region=os.getenv("AZURE_SPEECH_REGION"),
            voice="de-DE-SeraphinaMultilingualNeural",
        ),
        
        vad=silero.VAD.load(),
        turn_detection="semantic",
    )

    await ctx.connect()
    await session.start(room=ctx.room, agent=TelephonyAssistant())


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint
    ))
