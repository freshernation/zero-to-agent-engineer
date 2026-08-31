"""Wednesday's tracer, given to you complete."""

from contextlib import contextmanager


class Span:
    def __init__(self, name, started_at, metadata):
        self.name = name
        self.started_at = started_at
        self.ended_at = None
        self.metadata = dict(metadata)
        self.children = []

    def set(self, key, value):
        """Add metadata while the span is still running."""
        self.metadata[key] = value

    @property
    def duration_ms(self):
        if self.ended_at is None:
            return 0
        return int(round((self.ended_at - self.started_at) * 1000))

    def to_dict(self):
        return {
            "name": self.name,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
            "children": [child.to_dict() for child in self.children],
        }


class Tracer:
    def __init__(self, request_id, clock):
        self.request_id = request_id
        self.clock = clock
        self.spans = []
        self._stack = []

    @contextmanager
    def span(self, name, **metadata):
        """Open a span, nested inside whatever is already open."""
        span = Span(name, self.clock(), metadata)

        if self._stack:
            self._stack[-1].children.append(span)
        else:
            self.spans.append(span)

        self._stack.append(span)
        try:
            yield span
        except Exception as error:
            span.metadata["error"] = str(error)
            raise
        finally:
            # Closed either way - the runs worth seeing are the ones that failed.
            span.ended_at = self.clock()
            self._stack.pop()

    def to_dict(self):
        """The whole trace as a tree."""
        return {
            "request_id": self.request_id,
            "spans": [span.to_dict() for span in self.spans],
        }

    def total_ms(self):
        """How long the whole request took."""
        return sum(span.duration_ms for span in self.spans)

    def flatten(self):
        """(depth, name, duration_ms) in the order the spans started."""
        rows = []

        def walk(span, depth):
            rows.append((depth, span.name, span.duration_ms))
            for child in span.children:
                walk(child, depth + 1)

        for span in self.spans:
            walk(span, 0)

        return rows

    def slowest(self):
        """The top-level span that took longest - where to look first."""
        if not self.spans:
            return None
        return max(self.spans, key=lambda span: span.duration_ms).name
