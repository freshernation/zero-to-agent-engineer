"""Week 9, Day 1 - chunking.

Run me:  pytest week-09/day-1 -v
"""

import pytest

TEXT = (
    "Claims are submitted monthly and must be in by the fifth of the following "
    "month. Claims submitted after the fifth are paid in the next cycle. "
    "Receipts are required for everything over ten pounds."
)


class TestFixedChunks:
    def test_splits_evenly(self, load):
        chunks = load("chunking.py").fixed_chunks("abcdefghij", 3)
        assert chunks == ["abc", "def", "ghi", "j"]

    def test_nothing_is_lost(self, load):
        chunks = load("chunking.py").fixed_chunks(TEXT, 50)
        assert "".join(chunks) == TEXT

    def test_text_shorter_than_the_size(self, load):
        assert load("chunking.py").fixed_chunks("short", 400) == ["short"]

    def test_empty_text(self, load):
        assert load("chunking.py").fixed_chunks("", 400) == []


class TestOverlap:
    def test_chunks_repeat_the_previous_tail(self, load):
        chunks = load("chunking.py").fixed_chunks_with_overlap("abcdefghij", 5, 2)
        assert chunks[0] == "abcde"
        assert chunks[1].startswith("de"), (
            f"Second chunk was {chunks[1]!r}. With an overlap of 2 it should "
            "start with the last 2 characters of the first."
        )

    def test_covers_everything(self, load):
        chunks = load("chunking.py").fixed_chunks_with_overlap(TEXT, 60, 15)
        joined = "".join(chunks)
        for sentence_part in ["fifth of the following", "ten pounds"]:
            assert sentence_part in joined

    def test_refuses_an_overlap_that_cannot_advance(self, load):
        """overlap >= size means start never moves. That is an infinite loop."""
        with pytest.raises(ValueError) as caught:
            load("chunking.py").fixed_chunks_with_overlap("abcdefghij", 5, 5)
        assert "Overlap must be smaller than size" in str(caught.value)

    def test_refuses_a_bigger_overlap(self, load):
        with pytest.raises(ValueError):
            load("chunking.py").fixed_chunks_with_overlap("abcdefghij", 5, 9)

    def test_terminates(self, load):
        chunks = load("chunking.py").fixed_chunks_with_overlap("a" * 1000, 100, 90)
        assert len(chunks) < 200, "This looks like it nearly ran away."


class TestSentences:
    def test_splits_on_full_stops(self, load):
        assert load("chunking.py").split_sentences("One. Two. Three.") == [
            "One.", "Two.", "Three.",
        ]

    def test_handles_question_and_exclamation(self, load):
        assert len(load("chunking.py").split_sentences("Really? Yes! Fine.")) == 3

    def test_no_empties(self, load):
        assert load("chunking.py").split_sentences("  ") == []

    def test_keeps_the_punctuation(self, load):
        assert load("chunking.py").split_sentences("One. Two.")[0].endswith(".")


class TestSentenceChunks:
    def test_never_cuts_a_sentence(self, load):
        mod = load("chunking.py")
        chunks = mod.sentence_chunks(TEXT, max_chars=80, overlap_sentences=0)
        sentences = mod.split_sentences(TEXT)
        for chunk in chunks:
            assert any(s in chunk for s in sentences), (
                f"Chunk {chunk!r} contains no whole sentence. Group sentences - "
                "do not slice through them."
            )

    def test_respects_the_size_roughly(self, load):
        chunks = load("chunking.py").sentence_chunks(TEXT, max_chars=80, overlap_sentences=0)
        assert len(chunks) >= 2

    def test_overlap_repeats_a_sentence(self, load):
        mod = load("chunking.py")
        chunks = mod.sentence_chunks(TEXT, max_chars=80, overlap_sentences=1)
        assert len(chunks) >= 2
        first_sentences = set(mod.split_sentences(chunks[0]))
        second_sentences = set(mod.split_sentences(chunks[1]))
        assert first_sentences & second_sentences, (
            "With overlap_sentences=1 the last sentence of one chunk should "
            "reappear at the start of the next."
        )

    def test_no_overlap_means_no_repeats(self, load):
        mod = load("chunking.py")
        chunks = mod.sentence_chunks(TEXT, max_chars=80, overlap_sentences=0)
        seen = []
        for chunk in chunks:
            seen.extend(mod.split_sentences(chunk))
        assert len(seen) == len(set(seen))

    def test_everything_appears_somewhere(self, load):
        mod = load("chunking.py")
        chunks = mod.sentence_chunks(TEXT, max_chars=80, overlap_sentences=1)
        for sentence in mod.split_sentences(TEXT):
            assert any(sentence in chunk for chunk in chunks), (
                f"{sentence!r} is in no chunk at all - it can never be retrieved."
            )


class TestStats:
    def test_stats(self, load):
        stats = load("chunking.py").chunk_stats(["ab", "abcd", "abcdef"])
        assert stats["count"] == 3
        assert stats["shortest"] == 2
        assert stats["longest"] == 6
        assert stats["mean_length"] == 4

    def test_stats_of_nothing(self, load):
        stats = load("chunking.py").chunk_stats([])
        assert stats["count"] == 0


class TestLoading:
    def test_loads_every_document(self, load, corpus_dir):
        documents = load("loading.py").load_documents(corpus_dir)
        assert len(documents) == 6
        assert {d["source"] for d in documents} == {
            "onboarding.md", "expenses.md", "deployment.md",
            "oncall.md", "code_review.md", "security.md",
        }

    def test_sorted_by_source(self, load, corpus_dir):
        documents = load("loading.py").load_documents(corpus_dir)
        assert [d["source"] for d in documents] == sorted(
            d["source"] for d in documents
        )

    def test_text_is_there(self, load, corpus_dir):
        documents = load("loading.py").load_documents(corpus_dir)
        expenses = next(d for d in documents if d["source"] == "expenses.md")
        assert "fifth of the following month" in expenses["text"]

    def test_chunk_documents(self, load, corpus_dir):
        mod = load("loading.py")
        chunking = load("chunking.py")
        documents = mod.load_documents(corpus_dir)
        chunks = mod.chunk_documents(
            documents, lambda text: chunking.fixed_chunks(text, 300)
        )
        assert len(chunks) > 6
        assert all({"source", "text", "index"} <= set(c) for c in chunks)

    def test_index_counts_within_its_own_document(self, load, corpus_dir):
        mod = load("loading.py")
        chunking = load("chunking.py")
        documents = mod.load_documents(corpus_dir)
        chunks = mod.chunk_documents(
            documents, lambda text: chunking.fixed_chunks(text, 300)
        )
        for source in mod.sources_of(chunks):
            indexes = [c["index"] for c in mod.chunks_from(chunks, source)]
            assert indexes == list(range(len(indexes))), (
                f"{source} has indexes {indexes}. Each document numbers its own "
                "chunks from 0 - that is what makes a citation readable."
            )

    def test_the_chunker_is_swappable(self, load, corpus_dir):
        """Passing the strategy in is what makes Thursday's comparison possible."""
        mod = load("loading.py")
        chunking = load("chunking.py")
        documents = mod.load_documents(corpus_dir)
        small = mod.chunk_documents(
            documents, lambda t: chunking.fixed_chunks(t, 150)
        )
        large = mod.chunk_documents(
            documents, lambda t: chunking.fixed_chunks(t, 600)
        )
        assert len(small) > len(large)

    def test_sources_and_chunks_from(self, load, corpus_dir):
        mod = load("loading.py")
        chunking = load("chunking.py")
        chunks = mod.chunk_documents(
            mod.load_documents(corpus_dir), lambda t: chunking.fixed_chunks(t, 300)
        )
        assert mod.sources_of(chunks) == sorted(mod.sources_of(chunks))
        assert all(
            c["source"] == "expenses.md"
            for c in mod.chunks_from(chunks, "expenses.md")
        )
        assert mod.chunks_from(chunks, "nothing.md") == []
