# build_system(role, rules, output_format)
#     a system prompt containing the role, a "Rules:" section with each rule on
#     its own line starting with "- ", and a "Format:" line
#
# few_shot_messages(examples, question)
#     [(input, output), ...] as alternating user/assistant turns,
#     then the real question as a final user turn
#
# fence(label, content)
#     fence("review", "text")  ->  "<review>\ntext\n</review>"
#
# with_context(instruction, label, content)
#     the instruction, a blank line, then the fenced content
