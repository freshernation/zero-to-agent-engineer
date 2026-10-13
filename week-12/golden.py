"""The golden question set. Given to you, and the most valuable file this week.

Twenty questions, each with a phrase that MUST appear in a retrieved chunk for the
retrieval to count as a hit. Writing one of these for your own corpus is the
single highest-value thing you can do to a RAG system, and it takes an afternoon.

The last six are deliberately hard: they ask in words the documents do not use.
TF-IDF matches words, so it will miss some of them however well you chunk. That
is not a bug in your code - it is the honest limit of word matching, and it is
exactly why neural embeddings exist. Knowing WHICH questions fail, and why, is
worth more than a higher score.
"""

GOLDEN = [
    ("when must expense claims be submitted", "fifth of the following month"),
    ("how much can I spend without pre-approval", "two hundred pounds"),
    ("what is the client entertainment limit", "eighty pounds per head"),
    ("when are deployments blocked", "Fridays after two"),
    ("how long is the previous version kept warm", "one hour after"),
    ("how long is the on-call rotation", "one week long"),
    ("what should I do first when paged", "acknowledge it"),
    ("when does escalation reach the manager", "after twenty"),
    ("how many reviewers does billing code need", "two reviewers"),
    ("how big should a pull request be", "four hundred lines"),
    ("what do I need to collect my laptop", "signed offer letter"),
    ("who is my buddy chosen from", "different team"),
    ("do I need a hardware key for production", "hardware key"),
    ("can I copy customer data to my laptop", "may not be copied"),
    # harder: asked in words the documents do not use
    ("I accidentally pushed a password to git, what now", "rotate the credential"),
    ("is there a budget for a desk chair", "five hundred pounds"),
    ("my alarm went off but nothing was wrong, do I still write it up",
     "still worth recording"),
    ("what happens if I ignore the pager", "secondary after ten minutes"),
    ("am I paid extra for a broken night", "time off in lieu"),
    ("who fixes indentation complaints", "formatter runs automatically"),
]
