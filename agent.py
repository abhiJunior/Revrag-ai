from dotenv import load_dotenv
import asyncio

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION

load_dotenv()

SILENCE_TIMEOUT = 20  # seconds before reminder is triggered


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                model="gemini-2.5-flash-native-audio-latest",
                voice="Aoede",
                temperature=0.8,
            ),
        )


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    # --- No Overlap & Interruption Handling ---
    # Gemini Live (gemini-2.0-flash-live-001) has built-in VAD and turn detection.
    # It natively handles:
    #   - Not speaking while the user is speaking
    #   - Stopping immediately if the user interrupts (barge-in)
    # Silero VAD is NOT needed and was causing CPU delays on Windows.
    session = AgentSession()

    # --- Silence Monitoring ---
    # Tracks the last time the user spoke.
    # If 20+ seconds pass with no speech, the agent sends a gentle reminder.
    # The timer resets every time the user speaks.
    last_speech_time = asyncio.get_event_loop().time()
    silence_reminder_sent = False

    @session.on("user_speech_committed")
    def on_user_speech(*args):
        nonlocal last_speech_time, silence_reminder_sent
        last_speech_time = asyncio.get_event_loop().time()
        silence_reminder_sent = False  # reset after user speaks again

    async def silence_monitor():
        nonlocal last_speech_time, silence_reminder_sent
        while True:
            await asyncio.sleep(5)  # check every 5 seconds
            elapsed = asyncio.get_event_loop().time() - last_speech_time
            if elapsed >= SILENCE_TIMEOUT and not silence_reminder_sent:
                silence_reminder_sent = True
                try:
                    await session.generate_reply(
                        instructions=(
                            "The user has been completely silent for over 20 seconds. "
                            "In character as Simii, deliver ONE short sarcastic reminder "
                            "that you are still present and awaiting their command."
                        )
                    )
                except RuntimeError:
                    break  # session ended, stop the monitor cleanly
                last_speech_time = asyncio.get_event_loop().time()

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Start silence monitor as a background task
    asyncio.ensure_future(silence_monitor())

    # Greet the user on join
    await session.generate_reply(instructions=SESSION_INSTRUCTION)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

