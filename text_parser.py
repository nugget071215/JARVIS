from parser import parse_cmd


tests = [
    "Jarvis, open Firefox",
    "open firefox",
    "Jarvis launch Steam",
    "Jarvis restart pipewire",
    "Jarvis switch workspace 4",
    "Jarvis reboot",
    "Jarvis shutdown",
]

for text in tests:
    print(f"{text!r} -> {parse_cmd(text)}")
