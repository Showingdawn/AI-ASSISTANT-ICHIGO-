# voice_assistant_gui.py
import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
from assistant import (
    setup_conversation,
    start_conversation,
    stop_conversation,
    ask_openai,
    ask_document_question
)

# GUI settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("ICHIGO")
app.geometry("850x700")

# Initial values
user_name = "Aayush"
schedule = "vella"
personality_style = ctk.StringVar(value="BHAICHARRA")

# Setup convo
conversation = setup_conversation(user_name, schedule, personality_style.get())

# --- Functions ---
def update_text(widget, text):
    widget.configure(state="normal")
    widget.insert("end", text + "\n")
    widget.configure(state="disabled")
    widget.see("end")

def start_voice():
    update_text(transcript_box, "[System] Starting voice assistant...")
    threading.Thread(target=lambda: start_conversation(conversation, transcript_box)).start()

def stop_voice():
    stop_conversation(conversation)
    update_text(transcript_box, "[System] Voice assistant stopped.")

def ask_chat():
    query = chat_entry.get()
    if query:
        update_text(chat_display, f"You: {query}")
        response = ask_openai(query, personality_style.get())
        update_text(chat_display, f"ICHIGO: {response}")
        chat_entry.delete(0, 'end')

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text/PDF Files", "*.txt *.pdf")])
    if filepath:
        file_label.configure(text=os.path.basename(filepath))
        file_label.filepath = filepath

def ask_doc():
    if hasattr(file_label, 'filepath'):
        question = doc_entry.get()
        if question:
            update_text(doc_display, f"You: {question}")
            response = ask_document_question(file_label.filepath, question, personality_style.get())
            update_text(doc_display, f"ICHIGO: {response}")
            doc_entry.delete(0, 'end')
    else:
        update_text(doc_display, "Please upload a document first.")

# --- Layout ---
ctk.CTkLabel(app, text="🧠 ICHIGO", font=("Segoe UI", 24, "bold"), text_color="cyan").pack(pady=10)

# Tabs
tabs = ctk.CTkTabview(app, width=820, height=600)
tabs.pack()
tabs.add("🎙 Voice Assistant")
tabs.add("💬 Chat")
tabs.add("📄 Document Q&A")

# --- Voice Assistant Tab ---
voice_tab = tabs.tab("🎙 Voice Assistant")
ctk.CTkLabel(voice_tab, text="Live Voice Assistant", font=("Segoe UI", 16)).pack(pady=5)
transcript_box = ctk.CTkTextbox(voice_tab, height=400, width=780, state="disabled")
transcript_box.pack(pady=10)

ctk.CTkButton(voice_tab, text="Start", command=start_voice, fg_color="green").pack(side="left", padx=10, pady=10)
ctk.CTkButton(voice_tab, text="Stop", command=stop_voice, fg_color="red").pack(side="left", padx=10)

# Personality toggle
toggle_frame = ctk.CTkFrame(voice_tab)
toggle_frame.pack(pady=10)
ctk.CTkLabel(toggle_frame, text="Personality:").pack(side="left", padx=10)
ctk.CTkOptionMenu(toggle_frame, variable=personality_style, values=["Friendly", "Professional", "Funny", "JARVIS"]).pack(side="left")

# --- Chat Tab ---
chat_tab = tabs.tab("💬 Chat")
ctk.CTkLabel(chat_tab, text="Type your question", font=("Segoe UI", 16)).pack(pady=5)
chat_display = ctk.CTkTextbox(chat_tab, height=400, width=780, state="disabled")
chat_display.pack(pady=10)

chat_entry = ctk.CTkEntry(chat_tab, width=600, placeholder_text="Ask me anything...")
chat_entry.pack(side="left", padx=10, pady=5)
ctk.CTkButton(chat_tab, text="Send", command=ask_chat).pack(side="left")

# --- Document Q&A Tab ---
doc_tab = tabs.tab("📄 Document Q&A")
ctk.CTkLabel(doc_tab, text="Upload PDF/TXT & Ask", font=("Segoe UI", 16)).pack(pady=5)
doc_display = ctk.CTkTextbox(doc_tab, height=400, width=780, state="disabled")
doc_display.pack(pady=10)

browse_btn = ctk.CTkButton(doc_tab, text="Upload Document", command=browse_file)
browse_btn.pack(pady=5)
file_label = ctk.CTkLabel(doc_tab, text="No file selected")
file_label.pack()

doc_entry = ctk.CTkEntry(doc_tab, width=600, placeholder_text="Ask a question from the document...")
doc_entry.pack(side="left", padx=10, pady=5)
ctk.CTkButton(doc_tab, text="Ask", command=ask_doc).pack(side="left")

app.mainloop()
