# extract_json(text)    the JSON substring, or None if there is no {...}
# parse_json(text)      the parsed dict, or None if it will not parse
# strip_fences(text)    the text with any ```json fences removed
#
# extract_json must cope with prose before and after, with code fences,
# and with a reply containing no JSON at all.
