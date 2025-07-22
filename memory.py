# tools/memory.py
from collections import deque

# Memory buffer (default max 5 exchanges)
context_buffer = deque(maxlen=5)

def add_to_memory(role, content):
    context_buffer.append({"role": role, "content": content})

def get_context():
    return list(context_buffer)

def clear_memory():
    context_buffer.clear()
