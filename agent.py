from dotenv import load_dotenv

from livekit import agents 
from livekit.agents import AgentSession, Agent,RoomInputOptions
from livekit.plugins import noise_cancellation, silero
from livekit.plugins import google
from livekit.plugins.google.beta import realtime
from prompts import AGENT_INSTRUCTION,SESSION_INSTRUCTION

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm= google.beta.realtime.RealtimeModel(
                model = "gemini-2.5-flash-native-audio-latest",
                voice = "Aoede",
                temperature = 0.8
            )
        )

async def entrypoint(ctx : agents.JobContext):
    await ctx.connect()
    
    session = AgentSession()
    await session.start(
        room= ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=False,
            noise_cancellation=noise_cancellation.BVC()
        )
    )

    
    await session.generate_reply(
        instructions= SESSION_INSTRUCTION
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))