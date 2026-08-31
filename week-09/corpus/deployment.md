# Deployment

Deployments happen automatically when a pull request is merged to the main branch. There
is no separate deploy step and no deploy button.

Every merge runs the full test suite first. A failing suite blocks the merge, and there
is no way to override it without an incident declared. This is intentional and has been
questioned twice; both times the team voted to keep it.

Deployments are blocked on Fridays after two in the afternoon, and for the whole of the
last week of each quarter. The Friday rule exists because the on-call rotation is
thinnest at weekends.

Rollback is a single command, and the previous version is kept warm for one hour after
each deploy. After that hour a rollback becomes a redeploy of the old commit, which
takes about six minutes rather than twenty seconds.

Database migrations are deployed separately from application code, and always before it.
A migration that cannot be applied while the old code is still running is not accepted.
