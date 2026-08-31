"""A stand-in for the Anthropic client that never touches the network.

Real model calls cost money, need a key, and give a different answer every time -
none of which a test can work with. So every function you write this week takes a
`client` argument, and the tests hand it one of these.

That is not a testing trick. Passing the client in rather than reaching for a
global is called dependency injection, it is how every serious codebase handles
anything external, and it is why your week-7 agent will be testable at all.

    from fake_model import FakeClient, text_reply

    client = FakeClient([text_reply("Hello there")])
    response = client.messages.create(
        model="claude-sonnet-4-5", max_tokens=100,
        messages=[{"role": "user", "content": "Hi"}],
    )
    response.content[0].text        # "Hello there"
    client.calls[0]["messages"]     # what you actually sent

The shape of what comes back matches the real SDK, so the code you write here
works unchanged against the real thing.
"""


class TextBlock:
    """One piece of text in a response."""

    type = "text"

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"TextBlock({self.text!r})"


class ToolUseBlock:
    """The model asking for a tool to be run. Week 7 uses these."""

    type = "tool_use"

    def __init__(self, name, input, id="toolu_fake"):
        self.name = name
        self.input = input
        self.id = id

    def __repr__(self):
        return f"ToolUseBlock({self.name!r}, {self.input!r})"


class Usage:
    def __init__(self, input_tokens, output_tokens):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens

    def __repr__(self):
        return f"Usage(in={self.input_tokens}, out={self.output_tokens})"


class Message:
    """What messages.create() hands back."""

    def __init__(self, content, stop_reason="end_turn", usage=None,
                 model="claude-sonnet-4-5"):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = usage or Usage(10, 20)
        self.model = model
        self.role = "assistant"

    @property
    def text(self):
        """Convenience for tests - the real SDK does not have this."""
        return "".join(b.text for b in self.content if b.type == "text")

    def __repr__(self):
        return f"Message({self.content!r}, stop_reason={self.stop_reason!r})"


def text_reply(text, stop_reason="end_turn", input_tokens=10, output_tokens=20):
    """Build a plain text response."""
    return Message([TextBlock(text)], stop_reason, Usage(input_tokens, output_tokens))


def tool_reply(name, tool_input, id="toolu_fake", text=None):
    """Build a response where the model asks to use a tool."""
    blocks = []
    if text:
        blocks.append(TextBlock(text))
    blocks.append(ToolUseBlock(name, tool_input, id))
    return Message(blocks, stop_reason="tool_use")


_UNSET = object()

_NUMERIC_HINTS = ("priority", "rating", "count", "quantity", "score", "age")
_LIST_HINTS = ("tags", "items", "categories", "labels")


def _default_reply_for(kwargs):
    """What an unscripted call gets back.

    Plain calls get a bland sentence. But a call whose system prompt asks for
    JSON with named keys gets a JSON object with those keys - so a student can
    run their own CLI by hand and watch structured extraction actually work,
    without a key and without the network.

    Tests should script their responses explicitly rather than relying on this.
    """
    system = str(kwargs.get("system") or "")
    if "json" not in system.lower() or "keys:" not in system.lower():
        return "This is a fake reply."

    tail = system.lower().split("keys:", 1)[1]
    line = tail.splitlines()[0]
    names = [part.strip(" `'\"") for part in line.split(",") if part.strip()]
    names = [n for n in names if n and n.replace("_", "").isalnum()]
    if not names:
        return "This is a fake reply."

    import json as _json

    payload = {}
    for name in names:
        if any(hint in name for hint in _NUMERIC_HINTS):
            payload[name] = 2
        elif any(hint in name for hint in _LIST_HINTS):
            payload[name] = ["fake"]
        else:
            payload[name] = f"fake {name}"
    return _json.dumps(payload)


class _Stream:
    """What messages.stream() gives you - a context manager over text chunks."""

    def __init__(self, message, chunk_size=5):
        self._message = message
        self._chunk_size = chunk_size

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def text_stream(self):
        text = self._message.text
        for start in range(0, len(text), self._chunk_size):
            yield text[start:start + self._chunk_size]

    def get_final_message(self):
        return self._message


class _Messages:
    def __init__(self, client):
        self._client = client

    def create(self, **kwargs):
        return self._client._next(kwargs)

    def stream(self, **kwargs):
        return _Stream(self._client._next(kwargs))


class ModelError(Exception):
    """Stands in for anthropic.APIError."""


class FakeClient:
    """A scripted client.

    FakeClient([reply_1, reply_2])   hands those back in order
    FakeClient(reply)                hands the same one back every time
    FakeClient()                     hands back a bland default every time

    Put a ModelError instance in the list to make that call raise, which is how
    you test what your code does when the model is unavailable.
    """

    def __init__(self, responses=None):
        if responses is None:
            self._repeat = False
            self._responses = []
            self._index = 0
            self.calls = []
            self.messages = _Messages(self)
            return
        if responses is _UNSET:
            responses = None
        if responses is not None and not isinstance(responses, list):
            responses = [responses]
            self._repeat = True
        else:
            self._repeat = False
        self._responses = list(responses)
        self._index = 0
        self.calls = []
        self.messages = _Messages(self)

    def _next(self, kwargs):
        self.calls.append(kwargs)
        if not self._responses:
            return text_reply(_default_reply_for(kwargs))
        if self._repeat:
            response = self._responses[0]
        else:
            if self._index >= len(self._responses):
                raise AssertionError(
                    f"The code called the model {self._index + 1} times but only "
                    f"{len(self._responses)} responses were scripted."
                )
            response = self._responses[self._index]
            self._index += 1
        if isinstance(response, Exception):
            raise response
        return response

    @property
    def call_count(self):
        return len(self.calls)

    @property
    def last_call(self):
        return self.calls[-1] if self.calls else None
