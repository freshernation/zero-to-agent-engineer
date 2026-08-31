# Should print:
#   Turns: 3
#   Starts with: user
#
# Yes, 3 - asking for the last 4 leaves you with 3, because one of them
# has to go for the history to still be valid. That is the lesson.

messages = [
    {"role": "user", "content": "one"},
    {"role": "assistant", "content": "two"},
    {"role": "user", "content": "three"},
    {"role": "assistant", "content": "four"},
    {"role": "user", "content": "five"},
]


def trim(messages, max_turns):
    return messages[-max_turns:]


trimmed = trim(messages, 4)
print("Turns:", len(trimmed))
print("Starts with:", trimmed[0]["role"])
