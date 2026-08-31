"""Make one real call to the model, to prove the fake is telling the truth.

    export ANTHROPIC_API_KEY=your-key-here
    python3 week-06/try_it.py

Optional and not graded. Do it once. Then look at the response object it prints
next to the one FakeClient gives you and satisfy yourself they are the same shape.
"""

import os
import sys


def main():
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY is not set.")
        print("  export ANTHROPIC_API_KEY=your-key-here")
        print("\nThis script is optional - every exercise this week runs against")
        print("fake_model.py and needs no key at all.")
        return 1

    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        system="You are brief. Two sentences at most.",
        messages=[{"role": "user", "content": "What is a token, in plain English?"}],
    )

    print("--- what came back ---")
    print(response.content[0].text)
    print("\n--- the shape of it ---")
    print(f"stop_reason   {response.stop_reason}")
    print(f"model         {response.model}")
    print(f"input tokens  {response.usage.input_tokens}")
    print(f"output tokens {response.usage.output_tokens}")
    print("\nfake_model.py gives you an object with exactly these fields.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
