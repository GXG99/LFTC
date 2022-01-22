from gramatica import Gramatica


def first_follow(G):
    # Functie care returneaza true daca uniunea a schimbat prima multime sau false altfel.
    def union(set_1, set_2):
        set_1_len = len(set_1)
        set_1 |= set_2
        return set_1_len != len(set_1)

    first = {symbol: set() for symbol in G.simboluri}
    first.update((terminal, {terminal}) for terminal in G.terminale)
    follow = {symbol: set() for symbol in G.non_terminale}
    follow[G.start].add('$')

    while True:
        schimbat = False
        for stanga, dreapta in G.gramatica.items():
            for element in dreapta:
                for symbol in element:
                    if symbol != '^':
                        schimbat |= union(first[stanga], first[symbol] - set('^'))

                        if '^' not in first[symbol]:
                            break
                    else:
                        schimbat |= union(first[stanga], set('^'))
                else:
                    schimbat |= union(first[stanga], set('^'))
                aux = follow[stanga]
                for symbol in reversed(element):
                    if symbol == '^':
                        continue
                    if symbol in follow:
                        schimbat |= union(follow[symbol], aux - set('^'))
                    if '^' in first[symbol]:
                        aux = aux | first[symbol]
                    else:
                        aux = first[symbol]

        if not schimbat:
            return first, follow


class SLR:
    def __init__(self, G):
        self.G_imbogatit = Gramatica(f"{G.start}' -> {G.start}\n{G.text_gramatica}")

        # Pentru formatarea fisierului
        self.max_G_imbogatit_len = len(max(self.G_imbogatit.gramatica))

        self.G_indexat = []

        for stanga, dreapta in self.G_imbogatit.gramatica.items():
            for element in dreapta:
                self.G_indexat.append([stanga, element])

        # First - Follow
        self.first, self.follow = first_follow(self.G_imbogatit)
        self.C = self.items(self.G_imbogatit)
        self.action = list(self.G_imbogatit.terminale) + ['$']
        self.goto = list(self.G_imbogatit.non_terminale - {self.G_imbogatit.start})
        self.tabel_parsat_simboluri = self.action + self.goto
        self.tabel_parsat = self.construct_table()

    def items(self, G_impogatit):
        C = [self.CLOSURE({G_impogatit.start: {('.', G_impogatit.start[:-1])}})]

        while True:
            lungime = len(C)

            for I in C.copy():
                for X in G_impogatit.simboluri:
                    goto = self.GOTO(I, X)

                    if goto and goto not in C:
                        C.append(goto)

            if lungime == len(C):
                return C

    def CLOSURE(self, I):
        J = I

        while True:
            lungime = len(J)

            for stanga, dreapta in J.copy().items():
                for element in dreapta.copy():
                    if '.' in element[:-1]:
                        symbol_dupa_punct = element[element.index('.') + 1]

                        if symbol_dupa_punct in self.G_imbogatit.non_terminale:
                            for G_element in self.G_imbogatit.gramatica[symbol_dupa_punct]:
                                J.setdefault(symbol_dupa_punct, set()).add(
                                    ('.',) if G_element == ('^',) else ('.',) + G_element)

            if lungime == len(J):
                return J

    def construct_table(self):
        tabel_parsat = {r: {c: '' for c in self.tabel_parsat_simboluri} for r in range(len(self.C))}

        for i, I in enumerate(self.C):
            for stanga, dreapta in I.items():
                for element in dreapta:
                    if '.' in element[:-1]:  # CASE 2 a
                        simbol_dupa_punct = element[element.index('.') + 1]

                        if simbol_dupa_punct in self.G_imbogatit.terminale:
                            s = f's{self.C.index(self.GOTO(I, simbol_dupa_punct))}'

                            if s not in tabel_parsat[i][simbol_dupa_punct]:
                                if 'r' in tabel_parsat[i][simbol_dupa_punct]:
                                    tabel_parsat[i][simbol_dupa_punct] += '/'

                                tabel_parsat[i][simbol_dupa_punct] += s

                    elif element[-1] == '.' and stanga != self.G_imbogatit.start:  # CASE 2 b
                        for j, (G_head, G_body) in enumerate(self.G_indexat):
                            if G_head == stanga and (G_body == element[:-1] or G_body == ('^',) and element == ('.',)):
                                for f in self.follow[stanga]:
                                    if tabel_parsat[i][f]:
                                        tabel_parsat[i][f] += '/'

                                    tabel_parsat[i][f] += f'r{j}'

                                break

                    else:  # CASE 2 c
                        tabel_parsat[i]['$'] = 'acc'

            for A in self.G_imbogatit.non_terminale:  # CASE 3
                j = self.GOTO(I, A)

                if j in self.C:
                    tabel_parsat[i][A] = self.C.index(j)

        return tabel_parsat

    def GOTO(self, I, X):
        goto = {}

        for stanga, dreapta in I.items():
            for element in dreapta:
                if '.' in element[:-1]:
                    pozitie_punct = element.index('.')

                    if element[pozitie_punct + 1] == X:
                        replaced_dot_body = element[:pozitie_punct] + (X, '.') + element[pozitie_punct + 2:]

                        for C_stanga, C_dreapta in self.CLOSURE({stanga: {replaced_dot_body}}).items():
                            goto.setdefault(C_stanga, set()).update(C_dreapta)
        return goto

    def print_info(self):
        def fprint(text, variable):
            print(f'{text:>12}: {", ".join(variable)}')

        def print_line():
            print(f'+{("-" * width + "+") * (len(list(self.G_imbogatit.simboluri) + ["$"]))}')

        def symbols_width(symbols):
            return (width + 1) * len(symbols) - 1

        print('Gramatica imbogatita')

        for i, (stanga, dreapta) in enumerate(self.G_indexat):
            print(
                f'{i:>{len(str(len(self.G_indexat) - 1))}}: {stanga:>{self.max_G_imbogatit_len}} -> {" ".join(dreapta)}'
            )

        print()
        fprint('Terminale', self.G_imbogatit.terminale)
        fprint('Nonterminale', self.G_imbogatit.non_terminale)
        fprint('Simboluri', self.G_imbogatit.simboluri)

        print('\nFirst:')
        for stanga in self.G_imbogatit.gramatica:
            print(f'{stanga:>{self.max_G_imbogatit_len}} = {{ {", ".join(self.first[stanga])} }}')

        print('\nFollow:')
        for stanga in self.G_imbogatit.gramatica:
            print(f'{stanga:>{self.max_G_imbogatit_len}} = {{ {", ".join(self.follow[stanga])} }}')

        width = max(len(c) for c in {'ACTION'} | self.G_imbogatit.simboluri) + 2
        for r in range(len(self.C)):
            max_len = max(len(str(c)) for c in self.tabel_parsat[r].values())

            if width < max_len + 2:
                width = max_len + 2

        print('\nTabel parsare: ')
        print(f'+{"-" * width}+{"-" * symbols_width(self.action)}+{"-" * symbols_width(self.goto)}+')
        print(f'|{"":{width}}|{"Action":^{symbols_width(self.action)}}|{"Goto":^{symbols_width(self.goto)}}|')
        print(f'|{"Stare":^{width}}+{("-" * width + "+") * len(self.tabel_parsat_simboluri)}')
        print(f'|{"":^{width}}|', end=' ')

        for symbol in self.tabel_parsat_simboluri:
            print(f'{symbol:^{width - 1}}|', end=' ')

        print()
        print_line()

        for r in range(len(self.C)):
            print(f'|{r:^{width}}|', end=' ')

            for c in self.tabel_parsat_simboluri:
                print(f'{self.tabel_parsat[r][c]:^{width - 1}}|', end=' ')

            print()

        print_line()
        print()

    def SLR_parser(self, secventa):
        buffer = f'{secventa} $'.split()
        print(buffer)
        ok = False
        pointer = 0
        a = buffer[pointer]
        stiva = ['0']
        simboluri = ['']
        rezultate = {'step': [''], 'stack': ['Stiva'] + stiva, 'symbols': ['Simboluri'] + simboluri, 'input': ['Input'],
                   'action': ['Action']}

        step = 0
        while True:
            s = int(stiva[-1])
            step += 1
            rezultate['step'].append(f'({step})')
            rezultate['input'].append(' '.join(buffer[pointer:]))

            if a not in self.tabel_parsat[s]:
                rezultate['action'].append(f'ERROR: unrecognized symbol {a}')

                break

            elif not self.tabel_parsat[s][a]:
                rezultate['action'].append('ERROR: input cannot be parsed by given grammar')

                break

            elif '/' in self.tabel_parsat[s][a]:
                action = 'reduce' if self.tabel_parsat[s][a].count('r') > 1 else 'shift'
                rezultate['action'].append(f'ERROR: {action}-reduce conflict at state {s}, symbol {a}')

                break

            elif self.tabel_parsat[s][a].startswith('s'):
                rezultate['action'].append('shift')
                stiva.append(self.tabel_parsat[s][a][1:])
                simboluri.append(a)
                rezultate['stack'].append(' '.join(stiva))
                rezultate['symbols'].append(' '.join(simboluri))
                pointer += 1
                a = buffer[pointer]

            elif self.tabel_parsat[s][a].startswith('r'):
                head, body = self.G_indexat[int(self.tabel_parsat[s][a][1:])]
                rezultate['action'].append(f'reduce by {head} -> {" ".join(body)}')

                if body != ('^',):
                    stiva = stiva[:-len(body)]
                    simboluri = simboluri[:-len(body)]

                stiva.append(str(self.tabel_parsat[int(stiva[-1])][head]))
                simboluri.append(head)
                rezultate['stack'].append(' '.join(stiva))
                rezultate['symbols'].append(' '.join(simboluri))

            elif self.tabel_parsat[s][a] == 'acc':
                rezultate['action'].append('accept')
                ok = True
                break

        return (ok,rezultate)

    def print_rezultate(self, results):
        results = results[1]
        def print_line():
            print(f'{"".join(["+" + ("-" * (max_len + 2)) for max_len in max_lens.values()])}+')

        max_lens = {key: max(len(value) for value in results[key]) for key in results}
        actions = {'step': '>', 'stack': '', 'simboluri': '', 'input': '>', 'action': ''}

        print_line()
        print(''.join(
            [f'| {history[0]:^{max_len}} ' for history, max_len in zip(results.values(), max_lens.values())]) + '|')
        print_line()
        for i, step in enumerate(results['step'][:-1], 1):
            print(''.join([f'| {history[i]:{just}{max_len}} ' for history, just, max_len in
                           zip(results.values(), actions.values(), max_lens.values())]) + '|')

        print_line()
