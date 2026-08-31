# Should print:  Hit rate: 0.5
#
# Two of these four questions are answered by the chunk. The comparison is
# too strict.

CHUNKS = [
    "Claims are submitted monthly and must be in by the Fifth Of The Following Month.",
    "The on-call rotation is One Week Long and runs from Wednesday morning.",
]

GOLDEN = [
    ("when are claims due", "fifth of the following month"),
    ("how long is the rotation", "one week long"),
    ("what is the entertainment limit", "eighty pounds per head"),
    ("when are deployments blocked", "fridays after two"),
]

hits = 0
for question, expected in GOLDEN:
    if any(expected in chunk for chunk in CHUNKS):
        hits += 1

print("Hit rate:", hits / len(GOLDEN))
