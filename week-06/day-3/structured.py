# build_extraction_system(model_class)
#     a system prompt listing the model's field names
#     (model_class.model_fields gives you them)
#
# extract_one(client, text, model_class)
#     a validated instance, or None
#
# extract_with_retry(client, text, model_class, attempts=3)
#     the same, retrying and telling the model what was wrong last time
#
# attempts_taken(client, text, model_class, attempts=3)
#     how many calls it took
#
# Use temperature=0. The retry prompt must not be identical to the first.
