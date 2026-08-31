# The program a person uses. All the printing and asking lives here.
#
# Load expenses.json at the start, save it on quit. Prompt with "> ".
#
#   add     Description: / Amount: / Category:  ->  Added: Coffee $4.50 (food)
#   list    one format_expense line each, or "No expenses yet."
#   total   Total: $6.50
#   report  {category:<12}${amount:>8.2f} per category, alphabetical,
#           or "No expenses yet."
#   quit    "Saved 1 expense." / "Saved 2 expenses."  then stop
#   other   Unknown command: banana
#
# A bad amount prints the message and abandons that add. It does not
# ask again and does not add anything.
#
# Use expenses.py for all the logic. No arithmetic or file handling here.
