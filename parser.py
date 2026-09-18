import re 

# Commands that will translate to actions!
COMMANDS = {
    # Basic app commands
    "open": "open",
    "launch": "open",
    "start": "open",
    "kill": "kill",
    "stop": "kill",

    "restart": "restart",

    # "switch": "switch", Left out for later!
    
    # Basic power commands
    "reboot": "reboot",
    "shutdown": "shutdown",
    "poweroff": "shutdown",
    "lock": "lock",
}

# Parser function
def parse_cmd(text):
    # Normalizes, and simplifies the transcription
    text = text.lower().strip()
    text = re.sub(r"\bjarvis\b", "", text).strip()

    words = text.split()

    if not words:
        return None
    
    # Specifications of the action
    action = None 
    action_index = None

    for i, word in enumerate(words):
        if word in COMMANDS:
            action = COMMANDS[word]
            action_index = i 
            break

    if action is None:
        return None

    target = words[action_index + 1] if action_index + 1 < len(words) else ""

    return {
        "action": action,
        "target": target,
    }
