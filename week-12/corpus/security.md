# Security basics

Credentials are never committed to a repository. If you commit one by accident, treat it
as leaked even if you delete the commit: rotate the credential first, then clean the
history.

Production access requires a hardware key. Passwords alone are not sufficient and there
is no exception process for this.

Customer data may not be copied to a laptop. Analysis happens in the warehouse, where
access is logged. Downloading a sample "just to look at it" is the single most common
policy breach and it is treated seriously.

Third-party libraries are added by pull request like any other change, and new
dependencies get a short note in the description explaining what the library does and
why it is preferred to writing the code. Dependencies with fewer than two maintainers
need a conversation first.

Security questions of any kind go to the security channel. Nobody has ever been made to
feel stupid for asking in there, and asking late is much worse than asking obviously.
