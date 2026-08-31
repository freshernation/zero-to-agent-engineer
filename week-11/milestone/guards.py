"""Thursday's guards, given to you complete."""


class BudgetExceeded(Exception):
    pass


def check_question(text, max_chars):
    """Refuse anything too long to be worth paying a model to read."""
    if not text.strip():
        return False, "Question is empty"
    if len(text) > max_chars:
        return False, f"Question is too long ({len(text)} > {max_chars})"
    return True, ""


class Budget:
    def __init__(self, limit):
        self.limit = limit
        self._spent = 0.0

    @property
    def spent(self):
        return round(self._spent, 6)

    @property
    def remaining(self):
        return round(self.limit - self._spent, 6)

    def would_exceed(self, amount):
        """Ask before spending, so the caller can degrade rather than fail."""
        return self._spent + amount > self.limit

    def spend(self, amount):
        """Record a spend, or refuse it. A refused spend is not recorded."""
        if self.would_exceed(amount):
            raise BudgetExceeded(
                f"Spending {amount} would exceed the limit of {self.limit} "
                f"(already spent {self.spent})"
            )
        self._spent += amount
        return self.spent

    def reset(self):
        """Start the day again."""
        self._spent = 0.0
