# Settings   api_key: str
#            model                 default "claude-sonnet-4-5"
#            environment           default "development"
#            max_question_length   1-5000, default 500
#            request_timeout       1-120, default 30
#
# load_settings(env=None)   build from a mapping, defaulting to os.environ.
#                           RuntimeError naming the variable when the key is
#                           missing or empty. Rejects an environment that is not
#                           development / staging / production.
# mask(secret)              "sk-ant-abc123xyz" -> "sk-a...3xyz"
#                           anything under 8 characters -> "****"
# redacted(settings)        the settings as a dict, api_key masked
# is_production(settings)   True when environment is production
