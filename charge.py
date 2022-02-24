def wagdalena(seq):
    """takes an amino acid string and gives the cumulative charge"""
    dico = {"A": 0, "G": 0, "V": 0, "L": 0, "M": 0, "I": 0, "S": 0, "T": 0, "C": 0, "P": 0, "Q": 0, "F": 0, "Y": 0,
            "W": 0,
            "N": 0, "K": 1, "H": 1, "R": 1, "E": -1, "D": -1}
    res = 0
    if seq != None:
        for aa in seq:
            if aa in dico.keys():
                res += dico[aa]
    else:
        res = ""
    return res

def dict_parser(seq_dict):
    """Takes a dictionary and adds the cumulative charge of the 10 amino acids"""
    for current_id in seq_dict.keys():
        seq = seq_dict[current_id]['seq']
        tmhmm_pred = seq_dict[current_id]['TMsegment_pred']
        tm_segment = ""

        for i in range(0, len(tmhmm_pred), 3): #iterate on the length of the pos_list, to select the letter
            if tmhmm_pred[i] == 'M':
                try:
                    for l in range(tmhmm_pred[i + 2]+1, tmhmm_pred[i + 2]+11):
                        tm_segment += seq[l]
                except IndexError:
                    for l in range(tmhmm_pred[i + 2]+1, len(tmhmm_pred)):
                        tm_segment += seq[l]

        seq_dict[current_id]['charge'] = wagdalena(tm_segment)
    return seq_dict

def charge_sort(seq_dict):
    """Takes a dictionary and discard proteins based on the predicted charge"""
    temp_dict = {}
    for current_id in seq_dict.keys():
        if seq_dict[current_id]['charge'] == 2 or seq_dict[current_id]['charge'] == 3:
            temp_dict[current_id] = seq_dict[current_id]
    seq_dict = temp_dict
    return seq_dict



if __name__ == "__main__":
    print(wagdalena("CSHWQLTQMFQRFYPGQAPSLAENFAEHVLRATNQISKNDPVGAIHNAE"))
