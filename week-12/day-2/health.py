# uptime_seconds(started_at, now)              whole seconds
# health_payload(started_at, now, version)     {"status", "version", "uptime_seconds"}
# readiness(checks)                            {"ready", "checks", "failing"}
#
# checks is {name: zero-argument function returning a bool}.
# A check that RAISES counts as failing, not as a crash.
