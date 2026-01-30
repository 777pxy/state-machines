
class DFA:

    def validate_alphabet(self, alphabet: list[str]):
        for char in alphabet:
            if len(char) > 1:
                raise ValueError("Alphabet must only contain chars")
        
        return True
    
    def validate_list_of_strings(self, string_list: list[str]):
        for thing in string_list:
            if type(thing) != str:
                raise ValueError(f"{string_list} contains non-string elements")
    
        return True
    
    def process_transition_functions(self, transition_functions, Q, alphabet):
        state_transitions = {}
        state_transitions_check_hashmap = {}
        for state in Q:
            state_transitions_check_hashmap[state] = []
            state_transitions[state] = []

        for triplet in transition_functions:
            if len(triplet) != 3:
                raise ValueError("Transition function values must be a 3-tuple")
            if triplet[0] not in Q or triplet[2] not in Q:
                raise ValueError("Transition function cannot contain states not defined in Q")
            if triplet[1] not in alphabet:
                raise ValueError("Transition function cannot contain symbols not defined within the alphabet")
            
            state_transitions_check_hashmap[triplet[0]].append(triplet[1])
            state_transitions[triplet[0]].append((triplet[1], triplet[2]))

        for state in state_transitions_check_hashmap.keys():
            if set(state_transitions_check_hashmap[state]) != set(alphabet):
                raise ValueError(
                            f"All states must have a transition for each symbol in the alphabet: "
                            f"{state} : {state_transitions_check_hashmap[state]}"
                        )            
        return state_transitions

    
    def __init__(self, alphabet, transition_functions, Q, F, s):
        self.validate_alphabet(alphabet)
        self.validate_list_of_strings(Q)
        self.validate_list_of_strings(F)
        
        if type(s) != str:
            raise ValueError("Start state must be a string")

        self.state_transitions = self.process_transition_functions(transition_functions, Q, alphabet)

        if s not in Q:
            raise ValueError("Start state must be in Q")


        self.alphabet = alphabet
        self.Q = Q
        self.F = F
        self.s = s

        self.current_state = s

    def find_transition_function(self, symbol: str, state: str):
        for E_Q in self.state_transitions[state]:
            if E_Q[0] == symbol:
                return E_Q[1]
    
    def validate_symbol(self, symbol: str):
        if symbol not in self.alphabet:
            raise ValueError("word contains symbols not in alphabet")

    def validate_word(self, word: str):
        self.current_state = self.s

        for char in word:
            self.validate_symbol(char)
            self.current_state = self.find_transition_function(char, self.current_state)

        return self.current_state in self.F


# # Alphabet
# alphabet = ["0", "1"]

# # States
# Q = ["q0", "q1"]          # q0 = even number of 1s, q1 = odd number of 1s

# # Start state
# s = "q0"

# # Accepting states
# F = ["q0"]

# # Transition functions (q, symbol, q')
# transition_functions = [
#     ("q0", "0", "q0"),
#     ("q0", "1", "q1"),
#     ("q1", "0", "q1"),
#     ("q1", "1", "q0"),
# ]

# # Instantiate DFA
# dfa = DFA(alphabet, transition_functions, Q, F, s)

# # Valid and invalid words
# valid_word = "1010"     # even number of 1s → accepted
# invalid_word = "111"    # odd number of 1s → rejected

# print(dfa.validate_word(valid_word))    # True
# print(dfa.validate_word(invalid_word))  # False
