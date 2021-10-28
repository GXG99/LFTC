import re

f = open("source.txt")
lines = f.readlines()
f.close()

f = open("parsed.txt", "w")

key_words = ["int", "float", "struct", "while", "if", "else", "double", "main()"]
relations = ["==", "!=", "<", ">", "<=", ">="]
operators = ["+", "-", "/", "*", "="]
separators = ["(", ")", "{", "}", " ", ";", '\n']
id_regex = re.compile('^[a-z]{1,250}[;)+-/=* ]')
const_regex = re.compile('^[1-90]*[;=)+-/* ]')
include_regex = re.compile('^#include ((<[^>]+>)|("[^"]+"))')

subject = ""
x = 0

for line in lines:
    x += 1
    y = 0

    for atom in line:
        y += 1
        subject += atom
        if (include_regex.match(subject)):
            include_text = subject.split(" ")
            print(include_text[0])
            print(include_text[1])
            f.write(include_text[0] + "\n")
            f.write(include_text[1] + "\n")
            subject = ""
        elif (subject in key_words or subject in separators or subject in relations or subject in operators):
            if (subject != '\n' and subject != " "):
                print(subject)
                f.write(subject + '\n')
            subject = ""
        elif (id_regex.match(subject) or const_regex.match(subject)):
            print(subject[0:len(subject) - 1])
            f.write(subject[0:-1] + '\n')
            if (subject[-1] != '\n' and subject[-1] != ' '):
                print(subject[-1])
                f.write(subject[-1] + '\n')
            subject = ""

        elif (subject[-1] in separators and subject[0] != '#' and subject != "main("):
            print("Parsing impossible at line {line}, character {char} -> {subject} cannot be parsed"
                  .format(line=str(x), char=str(y - len(subject)), subject=subject[0:-1]))
            f.write("Parsing impossible at line {line}, character {char} -> {subject} cannot be parsed"
                    .format(line=str(x), char=str(y - len(subject)), subject=subject[0:-1]))
            subject = ""
            break
