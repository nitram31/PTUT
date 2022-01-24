def wagdalena(seq):
    dico = {"A":0, "G":0, "V":0, "L":0, "M":0, "I":0, "S":0, "T":0, "C":0, "P":0, "Q":0, "F":0, "Y":0, "W":0,
           "N":0, "K":1, "H":1, "R":1, "E":-1, "D":-1}
    res = 0
    for aa in seq:
        if aa in dico.keys():
            res += dico[aa]
    return res

print(wagdalena("CSHWQLTQMFQRFYPGQAPSLAENFAEHVLRATNQISKNDPVGAIHNAE"))
