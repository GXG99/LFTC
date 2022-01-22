class Automata:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
        self.states = [state for state in lines[0].split(' ')]
        self.final_states = [final_state for final_state in lines[1].split(' ')]
        self.alphabet = [symbol for symbol in lines[2].split(' ')]
        self.transition_lines = lines[3:]
        self.state_transition_table = []
        for line in self.transition_lines:
            self.state_transition_table.append([symbol for symbol in line.split(' ')])

    def transition(self, k, symbol):
        if symbol in self.alphabet and k != "*":
            return self.state_transition_table[self.states.index("q" + str(k))][self.alphabet.index(symbol)]
        else:
            return "INVALID SYMBOL"

    def accepts(self, string):
        k = 0
        counter = 0
        for symbol in string:
            k = self.transition(k, symbol)
            counter += 1
            if k == "INVALID SYMBOL":
                return False
        if counter > 250:
            return False
        return 'q' + k in self.final_states


