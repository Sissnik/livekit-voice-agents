"""
LiveKit Voice Agent - Quick Start
==================================
The simplest possible LiveKit voice agent to get you started.
Requires only OpenAI and Deepgram API keys.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero
from datetime import datetime
import os
import httpx
from typing import Optional

# Load environment variables
load_dotenv(".env")

class Assistant(Agent):
    """Basic voice assistant."""

    def __init__(self):
        super().__init__(
            instructions="""Du bist ein hilfreicher Assistent."""
        )

    @function_tool
    async def send_to_webhook(
        self, 
        context: RunContext, 
        message: str
    ) -> str:
        """Nutzen um Auskunft über die nächsten Termine zu bekommen..
        
        Args:
            message: Die Nachricht oder Frage die gesendet werden soll
        """
        webhook_url = "hier deine Webhook Url rein machen"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:  # <- 10 Sekunden Timeout
                response = await client.post(
                    webhook_url,
                    json={"message": message}
                )
                
                if response.status_code == 200:
                    return response.text
                else:
                    return f"Fehler: {response.status_code}"
        except httpx.TimeoutException:
            return "Timeout: Webhook hat nicht rechtzeitig geantwortet"
        except Exception as e:
            return f"Konnte nicht senden: {str(e)}"
        

async def entrypoint(ctx: agents.JobContext):
    """Entry point for the agent."""

    # Configure the voice pipeline with the essentials
    session = AgentSession()
    stt = deepgram.STT(model="nova-2", language="de")
    llm = openai.realtime.Realtimemode(
        model="gpt-realtime-mini",
        voice="echo",
        temparatur=0.8
    )

    # Start the session
    await session.start(
        room=ctx.room,
        agent=Assistant()
    )


if __name__ == "__main__":
    # Run the agent
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
