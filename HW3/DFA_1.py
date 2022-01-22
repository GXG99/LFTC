filename = "DFA_Integers.txt"


def print_states(states, final_states, alphabet, state_transition_table):
    print("States: ")
    print(states)


def print_alphabet(states, final_states, alphabet, state_transition_table):
    print("Alphabet :")
    print(alphabet)


def print_final_states(states, final_states, alphabet, state_transition_table):
    print("Final states: ")
    print(final_states)


def print_transitions(states, final_states, alphabet, state_transition_table):
    print("State transition table: ")
    print("[    ]", alphabet)
    index = 0
    for line in state_transition_table:
        print([states[index]], line)
        index += 1


def transition(k, symbol, states, final_states, alphabet, state_transition_table):
    if symbol in alphabet and k != "*":
        return state_transition_table[states.index("q" + str(k))][alphabet.index(symbol)]
    else:
        return "INVALID SYMBOL"


def accepts(string, states, final_states, alphabet, state_transition_table):
    k = 0
    for symbol in string:
        k = transition(k, symbol, states, final_states, alphabet, state_transition_table)
        if k == "INVALID SYMBOL":
            return False
    return 'q' + k in final_states


def check_acceptance(states, final_states, alphabet, state_transition_table):
    string = input("Enter string: ")
    if accepts(string, states, final_states, alphabet, state_transition_table):
        print("String {0} is accepted by the FA".format(string))
    else:
        print("String {0} is not accepted by the FA".format(string))


def find_longest_accepted_prefix(states, final_states, alphabet, state_transition_table):
    string = input("Enter string: ")
    index = 0
    while string != "":
        if accepts(string[:(len(string) - index)], states, final_states, alphabet, state_transition_table):
            print("Longest accepted prefix by the FA is {0}".format(string[:(len(string) - index)]))
            return
        else:
            index += 1
    if string == "":
        print("No accepted prefix was found!")


def run():
    text = "Maria si George"
    print(text)
    input_type = input("Keyboard/File: ")
    if input_type == "File":
        states, final_states, alphabet, state_transition_table = read_finite_automata_from_file()
    elif input_type == "Keyboard":
        states, final_states, alphabet, state_transition_table = read_finite_automata_from_keyboard()
    options = "1 - Print states \n" \
              "2 - Print alphabet \n" \
              "3 - Print transitions \n" \
              "4 - Print final states\n" \
              "5 - Run FA\n" \
              "6 - Find longest accepted prefix"
    menu = {
        "1": print_states,
        "2": print_alphabet,
        "3": print_transitions,
        "4": print_final_states,
        "5": check_acceptance,
        "6": find_longest_accepted_prefix
    }
    running = True
    print(options)
    while running:
        cmd = input(">> ")
        if cmd == "0":
            running = False
        elif cmd in menu.keys():
            menu[cmd](states, final_states, alphabet, state_transition_table)
        else:
            print("Invalid command")

def read_finite_automata_from_keyboard():
    temp = input("Enter states separated by ' ' (eg. q0 q1 q2): ")
    states = [state for state in temp.split(' ')]
    temp = input("Enter final states separated by ' ' (eg. q1 q3): ")
    final_states = [final_state for final_state in temp.split(' ')]
    temp = input("Enter alphabet separated by ' ' (eg. q1 q3): ")
    alphabet = [symbol for symbol in temp.split(' ')]
    state_transition_table = []
    for state in states:
        print("Enter transitions for state {0} and alphabet:".format(state))
        print(*alphabet)
        temp = input()
        state_transition_table.append([symbol for symbol in temp.split(' ')])
    return states, final_states, alphabet, state_transition_table


def read_finite_automata_from_file():
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    states = [state for state in lines[0].split(' ')]
    final_states = [final_state for final_state in lines[1].split(' ')]
    alphabet = [symbol for symbol in lines[2].split(' ')]
    transition_lines = lines[3:]
    state_transition_table = []
    for line in transition_lines:
        state_transition_table.append([symbol for symbol in line.split(' ')])
    return states, final_states, alphabet, state_transition_table


run()
