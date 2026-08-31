# call_with_retry(client, prompt, attempts=3, delay=0.01)   reply text, or None
# attempts_used(client, prompt, attempts=3, delay=0.01)     how many calls
# safe_call(client, prompt, fallback="Sorry, I could not answer that.")
#
# Retry ModelError from fake_model. safe_call must never raise.
