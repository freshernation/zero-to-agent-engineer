# PROJECTS   your three, each a dict with:
#            name, one_line, decision, alternative, broke, next_step
#
# one_liner(project)   the resume line
# story(project)       the four beats as a numbered string
# check(project)       {"ok": bool, "problems": [...]}
#
# check complains when:
#   - the one-liner has no number in it
#   - any beat is under eight words
#   - `broke` names no specific error or symptom
