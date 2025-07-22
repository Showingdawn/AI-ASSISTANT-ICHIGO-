# assistant.py (with generalized app launcher)
import os
import subprocess
import shutil
from dotenv import load_dotenv
import openai
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig
from tools.memory import add_to_memory, get_context
from tools.personality import get_prompt
from tools.document_qna import extract_text_from_file

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ELEVEN_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# --- GENERALIZED APP LAUNCHER ---
def open_app(app_name):
    app_name = app_name.strip().lower()

    # Shortcuts for popular apps
    shortcuts = {
        "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad",
        "calculator": "calc",
        "vscode": shutil.which("code"),
        "explorer": "explorer",
    }

    if app_name in shortcuts and shortcuts[app_name]:
        try:
            subprocess.Popen(shortcuts[app_name], shell=True)
            return f"✅ Launched {app_name.title()}."
        except Exception as e:
            return f"❌ Failed to launch {app_name}: {e}"

    # Try launching from PATH
    if shutil.which(app_name):
        try:
            subprocess.Popen(app_name, shell=True)
            return f"✅ Launched {app_name} from system PATH."
        except Exception as e:
            return f"❌ Error launching {app_name}: {e}"

    # Try launching as .exe if possible
    try:
        subprocess.Popen(f"{app_name}.exe", shell=True)
        return f"✅ Tried launching {app_name}.exe"
    except Exception as e:
        return f"❌ Could not launch {app_name}: {e}"

    return f"❌ '{app_name}' could not be found or launched."

def try_open_command(user_input):
    for prefix in ["open", "launch", "start"]:
        if user_input.lower().startswith(prefix):
            app = user_input[len(prefix):].strip()
            return open_app(app)
    return None

# Setup ElevenLabs conversation
def setup_conversation(user_name, schedule, personality="Friendly"):
    prompt = get_prompt(personality) + f" The user schedule is: {schedule}."
    first_message = f"Hello {user_name}, how can I help you today?"

    conversation_override = {
        "agent": {
            "prompt": {"prompt": prompt},
            "first_message": first_message,
        },
    }

    config = ConversationConfig(
        conversation_config_override=conversation_override,
        extra_body={},
        dynamic_variables={},
    )

    client = ElevenLabs(api_key=API_KEY)

    conversation = Conversation(
        client,
        AGENT_ID,
        config=config,
        requires_auth=True,
        audio_interface=DefaultAudioInterface(),
    )

    return conversation

# Start voice session
def start_conversation(conversation, textbox=None):
    def print_agent_response(text):
        add_to_memory("assistant", text)
        if textbox:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nJARVIS: {text}")
            textbox.configure(state="disabled")
            textbox.see("end")

    def print_user_transcript(text):
        add_to_memory("user", text)
        if textbox:
            textbox.configure(state="normal")
            textbox.insert("end", f"\nYou: {text}")
            textbox.configure(state="disabled")
            textbox.see("end")

    def print_interrupted_response(original, corrected):
        if textbox:
            textbox.configure(state="normal")
            textbox.insert("end", f"\n[JARVIS Truncated]: {corrected}")
            textbox.configure(state="disabled")
            textbox.see("end")

    conversation.callback_agent_response = print_agent_response
    conversation.callback_agent_response_correction = print_interrupted_response
    conversation.callback_user_transcript = print_user_transcript
    conversation.start_session()

# Stop voice session
def stop_conversation(conversation):
    conversation.end_session()

# GPT Text Q&A with memory & personality
def ask_openai(user_input, personality="Friendly"):
    app_attempt = try_open_command(user_input)
    if app_attempt:
        return app_attempt

    system_prompt = get_prompt(personality)
    add_to_memory("user", user_input)
    context = get_context()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}] + context
        )
        answer = response["choices"][0]["message"]["content"].strip()
        add_to_memory("assistant", answer)
        return answer
    except Exception as e:
        return f"[OpenAI Error] {e}"

# Document Q&A logic
def ask_document_question(filepath, question, personality="Professional"):
    context_text = extract_text_from_file(filepath)
    system_prompt = get_prompt(personality) + " You are answering based on a document provided."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Document:\n{context_text}\n\nQuestion: {question}"}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[DocQnA Error] {e}"
