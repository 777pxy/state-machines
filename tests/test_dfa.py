import pytest
from DFA.DFA import DFA


@pytest.fixture()
def even_ones_dfa():
    alphabet = ["0", "1"]
    Q = ["q0", "q1"]
    s = "q0"
    F = ["q0"]
    transition_functions = [
        ("q0", "0", "q0"),
        ("q0", "1", "q1"),
        ("q1", "0", "q1"),
        ("q1", "1", "q0"),
    ]
    return DFA(alphabet, transition_functions, Q, F, s)


def test_accepts_even_number_of_ones(even_ones_dfa):
    assert even_ones_dfa.validate_word("1010") is True
    assert even_ones_dfa.validate_word("") is True


def test_rejects_odd_number_of_ones(even_ones_dfa):
    assert even_ones_dfa.validate_word("111") is False


def test_rejects_symbol_not_in_alphabet(even_ones_dfa):
    with pytest.raises(ValueError, match="alphabet"):
        even_ones_dfa.validate_word("10a")


def test_validate_word_resets_state_between_calls(even_ones_dfa):
    assert even_ones_dfa.validate_word("1") is False
    assert even_ones_dfa.current_state == "q1"
    # Should reset to start state before processing the next word.
    assert even_ones_dfa.validate_word("0") is True
    assert even_ones_dfa.current_state == "q0"


def test_validate_alphabet_rejects_multi_char_symbols():
    with pytest.raises(ValueError, match="Alphabet"):
        DFA(["ab"], [("s", "ab", "s")], ["s"], ["s"], "s")


def test_validate_list_of_strings_rejects_non_string_state():
    with pytest.raises(ValueError, match="non-string"):
        DFA(["0"], [("s", "0", "s")], ["s", 1], ["s"], "s")


def test_start_state_must_be_string():
    with pytest.raises(ValueError, match="Start state must be a string"):
        DFA(["0"], [("s", "0", "s")], ["s"], ["s"], 1)


def test_start_state_must_be_in_Q():
    with pytest.raises(ValueError, match="Start state must be in Q"):
        DFA(["0"], [("s", "0", "s")], ["s"], ["s"], "q1")


def test_transition_function_requires_triplets():
    with pytest.raises(ValueError, match="3-tuple"):
        DFA(["0"], [("s", "0")], ["s"], ["s"], "s")


def test_transition_function_states_must_be_in_Q():
    with pytest.raises(ValueError, match="states not defined in Q"):
        DFA(["0"], [("s", "0", "q1")], ["s"], ["s"], "s")


def test_transition_function_symbols_must_be_in_alphabet():
    with pytest.raises(ValueError, match="symbols not defined"):
        DFA(["0"], [("s", "1", "s")], ["s"], ["s"], "s")


def test_transition_function_requires_complete_alphabet():
    with pytest.raises(ValueError, match="transition for each symbol"):
        DFA(
            ["0", "1"],
            [
                ("q0", "0", "q0"),
                ("q0", "1", "q1"),
                ("q1", "0", "q1"),
            ],
            ["q0", "q1"],
            ["q0"],
            "q0",
        )
