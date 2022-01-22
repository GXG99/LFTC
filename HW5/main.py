from gramatica import Gramatica
from slr import SLR


def convert_fip_to_code(fip_file, fip_to_cpp):
    code = []
    with open(fip_file) as f:
        for line in f:
            fip_code = int(line.strip())
            code.append(fip_to_cpp[fip_code])
    return code

def read_ts(ts_file):
    fip_to_cpp = {}
    with open(ts_file) as f:
        for line in f:
            fips = line.strip().split()
            chunk_code = fips[0]
            ts_code = int(fips[1])
            fip_to_cpp[ts_code] = chunk_code
    return fip_to_cpp

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele + " " 
    
    # return string  
    return str1 

def run():
    with open("gramatica.txt") as file:
        G = Gramatica(file.read())
        slr_parser = SLR(G)
        slr_parser.print_info()
        rezultate = slr_parser.SLR_parser(input('Secventa >> '))
        slr_parser.print_rezultate(rezultate)
        fip_to_cpp = read_ts("ts.txt")
        fip_file = input("FIP FILE?: ")
        code = convert_fip_to_code(fip_file, fip_to_cpp)
        ok, rules = slr_parser.SLR_parser(listToString(code))
        if not ok:
            print("RESPINS")
        else:
            print("ACCEPTAT:", rules)

run()
