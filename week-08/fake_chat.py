"""A scripted LangChain chat model. Week 6's FakeClient, in LangChain's shape.

Same idea as before: real model calls cost money, need a key, and answer
differently every time. This one is a genuine `BaseChatModel`, so LangChain and
LangGraph accept it anywhere a real model goes - including `bind_tools`.

    from fake_chat import FakeChat, ai, ai_tool

    model = FakeChat([
        ai_tool("calculate", {"expression": "2+2"}, id="t1"),
        ai("The answer is 4."),
    ])
    model.invoke([HumanMessage("what is 2+2")])

    model.calls          # every list of messages it was sent
    model.bound_tools    # what bind_tools was given

Notice what did NOT change from week 7: a scripted response, a recorded call,
and an assertion about what you sent. Testing an agent is the same problem
whichever framework is on top.
"""

from typing import Any, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult


def ai(text):
    """A plain text reply."""
    return AIMessage(content=text)


def ai_tool(name, args, id="t1", text=""):
    """A reply asking for a tool to be run."""
    return AIMessage(
        content=text,
        tool_calls=[{"name": name, "args": args, "id": id, "type": "tool_call"}],
    )


def ai_tools(calls, text=""):
    """A reply asking for several tools at once.

    calls is [(name, args, id), ...]
    """
    return AIMessage(
        content=text,
        tool_calls=[
            {"name": name, "args": args, "id": call_id, "type": "tool_call"}
            for name, args, call_id in calls
        ],
    )


class ModelError(Exception):
    """Stands in for a provider outage."""


class FakeChat(BaseChatModel):
    """A chat model that answers from a script."""

    responses: list = []
    repeat: bool = False
    calls: list = []
    bound_tools: Optional[list] = None
    index: int = 0

    def __init__(self, responses=None, **kwargs):
        if responses is None:
            responses = [ai("This is a fake reply.")]
            repeat = True
        elif not isinstance(responses, list):
            responses = [responses]
            repeat = True
        else:
            repeat = False
        super().__init__(
            responses=list(responses), repeat=repeat, calls=[], index=0, **kwargs
        )

    @property
    def _llm_type(self) -> str:
        return "fake-chat"

    def bind_tools(self, tools, **kwargs):
        """Record the tools and hand back a model that knows about them."""
        self.bound_tools = list(tools)
        return self

    def _next(self):
        if self.repeat:
            return self.responses[0]
        if self.index >= len(self.responses):
            raise AssertionError(
                f"The graph called the model {self.index + 1} times but only "
                f"{len(self.responses)} responses were scripted."
            )
        response = self.responses[self.index]
        self.index += 1
        return response

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        self.calls.append(list(messages))
        response = self._next()
        if isinstance(response, Exception):
            raise response
        # A fresh copy with a new id every call. A real model never hands back
        # the same message twice, and `add_messages` merges by id - so reusing
        # one would silently replace the previous reply instead of appending.
        response = response.model_copy(update={"id": None}, deep=True)
        return ChatResult(generations=[ChatGeneration(message=response)])

    @property
    def call_count(self):
        return len(self.calls)

    @property
    def last_call(self):
        return self.calls[-1] if self.calls else None
