# APPLICATIONS   at least ten, each with:
#                company, role, source, applied (ISO date), status
#
#   source: referral | direct | board | agency
#   status: applied | screening | interview | offer | rejected | ghosted
#
# count_by_status(apps)            {status: count}
# response_rate(apps)              fraction past "applied", 2dp
# by_source(apps)                  {source: count}
# response_rate_by_source(apps)    {source: rate}
# best_source(apps)                highest response rate; ties alphabetically
# needs_follow_up(apps, today, days=10)
#                                  still "applied" after `days` working days,
#                                  company names in order
#
# "Got past applied" means anything except applied and ghosted.
