# build_classifier_system(categories)
#     a system prompt naming the allowed answers
#
# classify(client, text, categories)
#     the category, or "unknown" if the model answered something not on the list
#
# Do not send temperature - current models reject it. Do not trust the reply.
