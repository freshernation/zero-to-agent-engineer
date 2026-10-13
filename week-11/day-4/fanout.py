# from worker import run_worker, report      (given)
#
# A job is a pair: (worker, brief).
#
# run_parallel_async(jobs)   async - runs every job at once and returns the
#                            reports in the SAME order as the jobs
# run_parallel(jobs)         the ordinary function to call from normal code
# run_sequential(jobs)       the same, one after another, for comparison
#
# A worker that RAISES must not lose the others. Its report is
#     "Worker <name> failed: <the error>"
# and every other report still comes back.
#
# run_worker blocks, so awaiting it directly gains nothing:
#     asyncio.to_thread(run_worker, worker, brief)
#
#
# violations(workers, dangerous)
#     the names, sorted, of every worker that BOTH
#       - has "reads_untrusted": True     (the key may be missing: that is False)
#       - holds a tool whose name is in the set `dangerous`
#     A worker that reads text a stranger wrote must not be able to act on it.
