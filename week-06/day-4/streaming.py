# stream_reply(client, prompt)          the full text, assembled from chunks
# stream_to(client, prompt, write)      the same, calling write(chunk) per chunk
# stream_with_usage(client, prompt)     (text, usage)
#
# with client.messages.stream(...) as stream:
#     for chunk in stream.text_stream: ...
#     final = stream.get_final_message()
