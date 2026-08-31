# Code review

Every change is reviewed by at least one other engineer. Changes touching billing or
authentication need two reviewers.

Reviews are expected within one working day. If you cannot review something within a
day, say so rather than leaving it silent, so the author can find somebody else.

Reviewers comment on correctness, tests, and clarity. Style is not reviewed by humans
because the formatter runs automatically on every commit; a comment about formatting is
a comment about the formatter's configuration and belongs in a separate discussion.

Authors are expected to keep changes small. A pull request over four hundred lines will
usually get a worse review than two of two hundred, and the guidance is to split rather
than to apologise in the description.

Disagreements that survive two rounds of comments move to a conversation rather than a
third round. The person who calls for the conversation is doing everyone a favour.
