from datastructures.BinarySearchTree import BinarySearchTree
from utils.Automata import Automata
import re

f = open("parsed.txt")
items = f.readlines()
f.close()

key_words = ["int", "float", "struct", "while", "if", "else", "double", "main()", "cin", "cout", "#include",
             "<iostream>", "using", "namespace", "std", "return"]
relations = ["==", "!=", "<", ">", "<=", ">="]
operators = ["+", "-", "/", "*", "="]
separators = ["(", ")", "{", "}", " ", ";", '\n']
id_regex = re.compile('^[a-z]{1,250}')
const_regex = re.compile('^[0-9]*([,.][0-9]{1,2})?$')

f = open("FIP.txt", "w")

g = open("idTS.txt", "w")

m = open("consTS.txt", "w")


def main():
    id_table = BinarySearchTree()
    const_table = BinarySearchTree()

    constants_automata = Automata("DFA_Constants.txt")
    id_automata =  Automata("DFA_ID.txt")

    id_indexes = []
    const_indexes = []
    table = []
    index = 0
    for item in items:
        item = item[0:-1]
        if item in key_words or item in separators or item in relations or item in operators:
            if item in key_words:
                table.append(item + ' ' + str(key_words.index(item)) + '\n')
            else:
                table.append(item + ' ' + '-1' + '\n')
        elif id_automata.accepts(item):
            table.append(item)
            id_indexes.append(index)
            id_table.insert(item)
        elif constants_automata.accepts(item):
            table.append(item)
            const_indexes.append(index)
            const_table.insert(item)
        else:
            print("Error at item: " + item)
        index += 1

    for identifier in id_indexes:
        table[identifier] = table[identifier] + " " + str(id_table.inorder([]).index(table[identifier])) + '\n'
    for identifier in const_indexes:
        table[identifier] = table[identifier] + " " + str(const_table.inorder([]).index(table[identifier])) + '\n'

    for identifier in id_table.inorder([]):
        g.write(identifier + " " + str(id_table.inorder([]).index(identifier)) + '\n')

    for identifier in const_table.inorder([]):
        m.write(identifier + " " + str(const_table.inorder([]).index(identifier)) + '\n')

    # print(const_table.inorder([]))
    for item in table:
        f.write(item)


main()
