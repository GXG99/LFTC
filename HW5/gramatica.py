class Gramatica:
    def __init__(self, fisier):
        self.text_gramatica = '\n'.join(filter(None, fisier.splitlines()))
        self.gramatica = {}
        self.start = None
        self.terminale = set()
        self.non_terminale = set()

        for productie in fisier.splitlines():
            stanga, _, dreapta = productie.partition(' -> ')

            if not stanga.isupper():
                raise ValueError(f'\'{stanga} -> {dreapta}\' Stanga \'{stanga}\' nu poate incepe cu litera mica.')

            if not self.start:
                self.start = stanga

            self.gramatica.setdefault(stanga, set())

            self.non_terminale.add(stanga)

            dreapta = {tuple(element.split()) for element in ' '.join(dreapta.split()).split('|')}

            for element in dreapta:
                self.gramatica[stanga].add(element)

                for symbol in element:
                    if not symbol.isupper():
                        self.terminale.add(symbol)
                    else:
                        self.non_terminale.add(symbol)

        self.simboluri = self.terminale | self.non_terminale
