"""Wednesday's orchestrator, given to you complete."""

from agent_kit import run_agent
from worker import report, run_worker, worker_schema

ORCHESTRATOR_SYSTEM = (
    "You coordinate a small team. You cannot look anything up or work anything "
    "out yourself - you can only ask a worker.\n\n"
    "Rules:\n"
    "- Give each worker a complete brief: the goal, what is already known, and "
    "what to send back. A worker sees nothing but its brief\n"
    "- Ask the worker whose description fits. Do not ask twice for the same thing\n"
    "- If a worker fails or does not finish, say so rather than guessing\n"
    "- When you have what you need, answer the user in one or two sentences"
)


def run_team(client, question, workers, max_delegations=4, max_steps=8):
    """Run the orchestrator, and every worker it asks, to an answer."""
    delegations = []
    model_calls = {"orchestrator": 0}
    for worker in workers:
        model_calls[worker["name"]] = 0

    def ask(worker):
        def delegate(brief):
            if len(delegations) >= max_delegations:
                answer = f"Refused: delegation limit of {max_delegations} reached."
            else:
                try:
                    result = run_worker(worker, brief)
                    model_calls[worker["name"]] += result["steps"]
                    answer = report(result)
                except Exception as error:
                    answer = f"Worker {worker['name']} failed: {error}"
            delegations.append(
                {"worker": worker["name"], "brief": brief, "report": answer}
            )
            return answer

        return delegate

    schemas = [worker_schema(worker) for worker in workers]
    tools = {f"ask_{worker['name']}": ask(worker) for worker in workers}

    result = run_agent(
        client, ORCHESTRATOR_SYSTEM, schemas, tools, question, max_steps=max_steps
    )
    model_calls["orchestrator"] = result["steps"]

    return {
        "text": result["text"],
        "stopped": result["stopped"],
        "delegations": delegations,
        "model_calls": model_calls,
        "total_calls": sum(model_calls.values()),
    }
