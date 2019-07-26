import pytest
import numpy
from numpy.testing import assert_equal
from spacy_pytorch_transformers.util import align_word_pieces, pad_batch, batch_by_length


@pytest.mark.parametrize("spacy_tokens,wp_tokens,expected_alignment", [
    (["a"], ["a"], [[0]]),
    (["a", "b", "c"], ["a", "b", "c"], [[0], [1], [2]]),
    (["ab", "c"], ["a", "b", "c"], [[0, 1], [2]]),
    (["a", "b", "c"], ["ab", "c"], [[0], [0], [1]]),
    (["ab", "cd"], ["a", "bc", "d"], [[0, 1], [1, 2]]),
    (["abcd"], ["ab", "##cd"], [[0, 1]]),
    (["d", "e", "f"], ["[CLS]", "d", "e", "f"], [[1], [2], [3]]),
    ([], [], [])
]) 
def test_align_word_pieces(spacy_tokens, wp_tokens, expected_alignment):
    output = align_word_pieces(spacy_tokens, wp_tokens)
    assert output == expected_alignment


@pytest.mark.parametrize("lengths,min_batch,expected", [
    ([1, 2, 2, 4], 1, [[3], [1, 2], [0]]),
    ([1, 2, 2, 4], 2, [[0, 1, 2, 3]]),
    ([4, 2, 2, 1], 2, [[0, 1, 2, 3]]),
    ([4, 4, 2, 2, 1], 2, [[0, 1], [2, 3, 4]]),
    ([10, 7, 2, 2, 1], 2, [[0, 1], [2, 3, 4]])
])
def test_batch_by_length(lengths, min_batch, expected):
    seqs = ['a' * length for length in lengths]
    batches = batch_by_length(seqs, min_batch)
    assert batches == expected


@pytest.mark.parametrize("lengths,expected_shape", [
    ([1, 2], (2, 2)),
    ([1, 2, 3], (3, 3)),
    ([0, 1], (2, 1)),
    ([1], (1, 1)),
    ([1, 5, 2, 4], (4, 5)),
])
def test_pad_batch(lengths, expected_shape):
    seqs = [numpy.ones((length,), dtype="f") for length in lengths]
    padded = pad_batch(seqs)
    for i, seq in enumerate(seqs):
        assert padded[i].sum() == seq.sum()
        assert_equal(padded[i, :len(seq)], seq)
    assert padded.shape == expected_shape