from low_coverage_code.is_happy_2 import is_happy

### first llm prompt ###

# def test_short_sequence_returns_false():
#     assert is_happy("ab") is False

# def test_no_matches_returns_false():
#     assert is_happy([1, 2, 3, 4, 5]) is False

# def test_custom_sequence_returns_true():
#     class HappySeq:
#         def __len__(self):
#             return 5
#         def __getitem__(self, idx):
#             if isinstance(idx, slice):
#                 start = idx.start
#                 return self[start + 1]
#             return f"item{idx}"
#     s = HappySeq()
#     assert is_happy(s) is True

### second llm prompt ###

def test_is_happy_true_custom_sequence():
    class Seq:
        def __len__(self): return 5
        def __getitem__(self, idx):
            if isinstance(idx, slice):
                start = idx.start or 0
                return ("VAL", start+1)
            return ("VAL", idx)
    assert is_happy(Seq()) is True

def test_is_happy_false_with_some_matches():
    class Seq2:
        def __len__(self): return 4
        def __getitem__(self, idx):
            if isinstance(idx, slice):
                start = idx.start or 0
                return ("VAL", 1) if start == 0 else ("VAL", 99)
            return ("VAL", 1) if idx == 1 else ("VAL", idx)
    assert is_happy(Seq2()) is False