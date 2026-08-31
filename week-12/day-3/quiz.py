"""Quiz yourself, out loud, in a random order.

    python3 week-12/day-3/quiz.py

Say the answer to the wall before pressing Enter. Then read what your answer was
supposed to contain. Being able to recognise a good answer is not the same as
being able to give one, and this is the difference.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from concepts import CONCEPTS


def main():
    order = CONCEPTS[:]
    random.shuffle(order)

    for number, concept in enumerate(order, start=1):
        print(f"\n[{number}/{len(order)}] {concept['question']}")
        input("  ...say it out loud, then press Enter. ")
        print(f"  should contain: {', '.join(concept['must_mention'])}")

    print("\nAnything you fumbled, write out longhand in ANSWERS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
