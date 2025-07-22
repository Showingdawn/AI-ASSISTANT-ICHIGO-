@echo off
title 💬 BANKAIIIIIIIIIIIIIIIIIIIIIIIII
cd /d %~dp0

:: ▶ Set fullscreen or minimized
mode con: cols=100 lines=30
powershell -Command "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys('% ')"

:: ▶ Play sound or voice
echo [🔊] Playing startup sound...
powershell -c "[console]::beep(800,400)"
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak('Jarvis is now ready.')"

:: ▶ Check and activate virtual environment
echo [🧠] Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [❌] venv not found. Creating new one...
    python -m venv venv
    call venv\Scripts\activate.bat
)

:: ▶ Auto-install dependencies if needed
echo [📦] Checking dependencies...
pip show openai >nul 2>&1 || (
    echo [⬇️] Installing required packages...
    pip install -r requirements.txt
)

:: ▶ Launch the GUI
echo [🚀] Starting Voice Assistant GUI...
python voice_assistant_gui.py

echo ------------------------------------------------------
echo [✔️] ICHIGO closed. Press any key to exit.
pause
