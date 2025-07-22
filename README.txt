# 🧠 AI Voice Assistant (ICHIGO)

Your personal desktop AI assistant powered by:

* 🎤 Real-time voice with ElevenLabs
* 🤖 Smart answers via OpenAI (ChatGPT)
* 🧠 Memory, documents Q\&A, app launching
* 🎨 Stylish CustomTkinter GUI with profile and command interface

---

## 🚀 Features

| Feature                  | Description                                       |
| ------------------------ | ------------------------------------------------- |
| 🎙️ Voice Input / Output | Talk to your assistant naturally using ElevenLabs |
| 🧠 OpenAI Integration    | ChatGPT-powered smart Q\&A (GPT-3.5 / GPT-4)      |
| 📁 Document Q\&A         | Ask questions about PDFs and .txt files           |
| 🔧 Tools                 | Includes calculator, reminder, local memory, more |
| 🖥️ App Launcher         | "Open Chrome", "Start Notepad", etc.              |
| 💬 Chat GUI              | Beautiful modern chat-like interface with themes  |

---

## 📂 Project Structure

```bash
ai voice/
├── assistant.py              # Core AI logic
├── voice_assistant_gui.py    # CustomTkinter GUI
├── .env                      # API keys (not tracked)
├── .env.template             # Example API config
├── launch_aivoice.bat        # Windows launcher
├── requirements.txt          # Python dependencies
│
├── tools/                    # Extra features
│   ├── document_qna.py       # PDF/text reader
│   ├── memory.py             # Recent message history
│   └── personality.py        # Personality switching logic
│
├── assets/                   # Images/sounds (e.g. gallery.jpg)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. 🧪 Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. 🔐 Add Your API Keys

Create a `.env` file like this:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo
ELEVEN_API_KEY=your_elevenlabs_key
AGENT_ID=your_elevenlabs_agent_id
```

### 4. 🧠 Launch

```bash
python voice_assistant_gui.py
```

OR double-click:

```bash
launch_aivoice.bat
```

---

## 🧠 Personality Modes

Choose how your assistant behaves:

* Friendly
* Professional
* Funny
* Serious

---

## 💡 Coming Soon

* Google Calendar smart planner
* Long-term LangChain memory
* Voice command for tasks, reminders, summaries
* Offline fallback modes

---

## 🙌 Credits

* OpenAI GPT API
* ElevenLabs Voice
* CustomTkinter for GUI
* PyMuPDF for document parsing

---

## ✅ .env.template (example)

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo
ELEVEN_API_KEY=
AGENT_ID=
``



AND BHAICHHAARAA