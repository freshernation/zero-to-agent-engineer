# run_tool_async(name, arguments)     async - returns the result string
# run_all_async(calls)                async - [(id, name, args), ...]
#                                     -> [(id, result), ...] in the SAME order
# run_all(calls)                      the ordinary function to call from normal code
# run_all_sequential(calls)           the same, one after another, for comparison
#
# asyncio.to_thread(function, **arguments) runs a blocking function without
# blocking the loop.
