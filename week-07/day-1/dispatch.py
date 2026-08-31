# TOOLS                        dict of tool name -> function
# run_tool(name, arguments)    the result as a STRING;
#                              "Unknown tool: xyz" for a name that is not there
# tool_uses(response)          the tool_use blocks, ignoring text blocks
# handle_response(response)    [(tool_use_id, result_string), ...] for every call
#
# Everything comes back as a string - that is what a tool_result block carries.
