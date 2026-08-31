# Note   title: str (>=1 char), body: str (>=1 char),
#        tags: list[str] = [], priority: int 1-3 = 2
#
# build_note_system()                    system prompt naming every field
# extract_note(client, text, attempts=2) a validated Note, or None
#
# Retry once, telling the model what was wrong. temperature=0.
