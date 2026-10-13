"""Monday's worker, given to you complete."""

from agent_kit import run_agent

BRIEF_DESCRIPTION = (
    "Everything the worker needs: the goal, what is already known, and what "
    "to send back. It sees nothing else."
)


def make_worker(name, description, system, schemas, tools, client):
    """Bundle up what one worker is: its instructions, its tools, its model."""
    return {
        "name": name,
        "description": description,
        "system": system,
        "schemas": schemas,
        "tools": tools,
        "client": client,
    }


def worker_schema(worker):
    """How this worker looks to an orchestrator: one tool, one argument."""
    return {
        "name": f"ask_{worker['name']}",
        "description": worker["description"],
        "input_schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string", "description": BRIEF_DESCRIPTION}
            },
            "required": ["brief"],
        },
    }


def run_worker(worker, brief, max_steps=6):
    """Run the worker on a brief. It starts from nothing every time."""
    result = run_agent(
        worker["client"],
        worker["system"],
        worker["schemas"],
        worker["tools"],
        brief,
        max_steps=max_steps,
    )
    result["worker"] = worker["name"]
    return result


def report(result):
    """The only thing that crosses back to whoever asked."""
    if result["stopped"] == "answered":
        return result["text"]
    return f"Worker {result['worker']} did not finish: {result['text']}"
