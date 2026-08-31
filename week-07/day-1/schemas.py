# make_schema(name, description, properties, required)   a tool schema dict
# text_param(description)   {"type": "string", "description": ...}
# all_schemas()             a list of three schemas, one per tool in tools.py
#
# A schema looks like:
#   {"name": ..., "description": ...,
#    "input_schema": {"type": "object", "properties": {...}, "required": [...]}}
