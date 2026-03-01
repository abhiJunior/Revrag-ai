# 🤖 Medha — Real-Time Voice Agent

Medha is a real-time voice AI agent built with LiveKit and Google Gemini Live. It joins a LiveKit room, listens to the user via microphone, and responds with voice in the character of a witty, sarcastic butler.

---

## 📋 Features

- 🎙️ **Full voice interaction** — Speech-to-text, AI response, and text-to-speech in one pipeline
- 🔇 **No overlap** — Gemini Live's built-in VAD ensures the agent never speaks while the user is talking and stops immediately on interruption
- ⏱️ **Silence detection** — If the user is silent for 20+ seconds, Medha delivers a sarcastic reminder that it's still waiting
- 🔊 **Noise cancellation** — Background noise filtered via LiveKit's BVC plugin
- 🎭 **Butler persona** — Witty, sarcastic, classy one-liner responses

---

## 🛠️ Setup Instructions

### 1. Prerequisites

Make sure you have the following installed:

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended package manager)

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/revrage-ai.git
cd revrage-ai
```

### 3. Install Dependencies

```bash
uv sync
```

Or with pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project:

```env
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
GOOGLE_API_KEY=your_google_api_key
```

See the **Required Environment Variables** section below for details on where to get each value.

---

## ▶️ How to Run

### Console Mode (for local testing)

```bash
uv run agent.py console
```

This runs the agent locally using your microphone and speakers — no LiveKit room required.

### Production Mode (connects to LiveKit room)

```bash
uv run agent.py start
```

Then open the [LiveKit Playground](https://agents-playground.livekit.io/) and connect using your LiveKit URL and credentials to speak with the agent.

---

## 🔑 Required Environment Variables

| Variable | Description | Where to Get It |
|---|---|---|
| `LIVEKIT_URL` | WebSocket URL of your LiveKit server | [LiveKit Cloud Dashboard](https://cloud.livekit.io) → Your Project |
| `LIVEKIT_API_KEY` | LiveKit API key for authentication | [LiveKit Cloud Dashboard](https://cloud.livekit.io) → Settings → Keys |
| `LIVEKIT_API_SECRET` | LiveKit API secret for authentication | Same as above |
| `GOOGLE_API_KEY` | Google Gemini API key for Live audio model | [Google AI Studio](https://aistudio.google.com) → Get API Key |

> ⚠️ **Important:** The `GOOGLE_API_KEY` must have access to the **Gemini Live API** (`gemini-2.0-flash-live-001`). Free-tier keys may not have `bidiGenerateContent` support. If you get a `1008` error, generate a new key from Google AI Studio on a paid project.

---

## 📦 SDK Used

| SDK / Library | Version | Purpose |
|---|---|---|
| `livekit-agents` | 1.4.x | Core agent framework and session management |
| `livekit-plugins-google` | latest | Gemini Live realtime model integration |
| `livekit-plugins-noise-cancellation` | latest | Background Voice Cancellation (BVC) |
| `python-dotenv` | latest | Environment variable management |

---

## 🌐 External Services

| Service | Purpose | Free Tier Available |
|---|---|---|
| [LiveKit Cloud](https://cloud.livekit.io) | Hosts the LiveKit room server for real-time audio transport | ✅ Yes |
| [Google Gemini Live API](https://aistudio.google.com) | Powers STT, LLM response, and TTS via `gemini-2.0-flash-live-001` | ⚠️ Limited |
| [LiveKit Agents Playground](https://agents-playground.livekit.io/) | Browser-based UI to connect and test the voice agent | ✅ Yes |

---

## ⚙️ How No-Overlap & Interruption Works

This agent uses **Gemini Live's native Voice Activity Detection (VAD)** built into the `gemini-2.0-flash-live-001` model. No external VAD library (like Silero) is needed.

Gemini Live handles:
- **Turn detection** — knows when the user has finished speaking before responding
- **Barge-in / interruption** — if the user starts speaking while Medha is talking, the agent stops immediately
- **No overlap** — the agent will never talk over the user

This is handled at the model level via the `bidiGenerateContent` WebSocket API, making it low-latency and CPU-efficient.

---

## ⚠️ Known Limitations

- **Gemini Live API access** — The `gemini-2.0-flash-live-001` model requires a Google API key with Live API access enabled. Free-tier keys may not work.
- **Console mode microphone** — In `console` mode on Windows, there can occasionally be audio device conflicts depending on your default microphone setup.
- **Silence reminder is session-wide** — The 20-second silence timer starts from the last user speech. If the agent itself speaks (e.g. the greeting), the timer is not reset — only user speech resets it.
- **No persistent memory** — Medha does not remember previous conversations. Each session starts fresh.
- **Single room only** — The agent is designed to handle one LiveKit room at a time per worker process.
- **Internet required** — Both LiveKit and Gemini Live require an active internet connection. Offline mode is not supported.

---

## 📁 Project Structure

```
revrage-ai/
├── agent.py          # Main agent logic, session setup, silence monitor
├── prompts.py        # Medha persona instructions and session greeting
├── .env              # Environment variables (never commit this)
├── .env.example      # Example env file for reference
├── pyproject.toml    # Project dependencies
└── README.md         # This file
```

---

## 🧪 Testing the Agent

1. Run `uv run agent.py console` for a quick local test
2. Speak into your microphone — Medha will respond via your speakers
3. For full room testing, run `uv run agent.py start` and connect via [LiveKit Playground](https://agents-playground.livekit.io/)

---

## 📄 License

MIT License — free to use and modify.