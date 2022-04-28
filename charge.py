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
    """Takes a dictionary and adds the cumulative charge of the amino acids before and after the predicted
    transmembrane segment"""
    for current_id in seq_dict.keys():
        seq = seq_dict[current_id]['seq']
        keys = seq_dict[current_id]
        TM_results = []
        for key in keys:
            if 'TM_pred' in key:
                TM_results.append(key)

        for software_TM_pred in TM_results:
            program_name = ""

            TM_pred = seq_dict[current_id][software_TM_pred]
            j = 0
            while software_TM_pred[j] != '_':
                program_name += software_TM_pred[j]
                j += 1

            plus_10_after_TM_charge = program_name + '_plus_10_after_TM_charge'
            plus_10_after_TM_sequence = program_name + '_plus_10_after_TM_sequence'
            plus_5_after_TM_charge = program_name + '_plus_5_after_TM_charge'
            minus_10_before_TM_charge = program_name + '_minus_10_before_TM_charge'
            minus_5_before_TM_charge = program_name + '_minus_5_before_TM_charge'
            tm_segment_length = program_name + '_tm_segment_length'

            seq_dict[current_id][tm_segment_length] = []
            seq_dict[current_id][plus_10_after_TM_charge] = []
            seq_dict[current_id][plus_5_after_TM_charge] = []
            seq_dict[current_id][plus_10_after_TM_sequence] = []
            seq_dict[current_id][minus_5_before_TM_charge] = []
            seq_dict[current_id][minus_10_before_TM_charge] = []

            for i in range(0, len(TM_pred), 3):  # iterate on the length of the pos_list, to select the letter
                if TM_pred[i] == 'M':

                    ten_after_tm_segment = ""
                    five_after_tm_segment = ""
                    five_before_tm_segment = ""
                    ten_before_tm_segment = ""

                    try:
                        for l in range(TM_pred[i + 2] - 1, TM_pred[i + 2] + 9):
                            ten_after_tm_segment += seq[l]
                            five_after_tm_segment += seq[l]
                            five_after_tm_segment = five_after_tm_segment[0:4]

                        for l in range(TM_pred[i - 1] - 9, TM_pred[i - 1] - 1):
                            five_before_tm_segment += seq[l]
                            five_before_tm_segment = five_before_tm_segment[0:4]
                            ten_before_tm_segment += seq[l]

                    except IndexError:
                        for l in range(TM_pred[i + 2] - 1, len(TM_pred)):
                            five_after_tm_segment += seq[l]
                            five_after_tm_segment = five_after_tm_segment[0:4]
                            ten_after_tm_segment += seq[l]
                            five_before_tm_segment += seq[l]
                            five_before_tm_segment = five_before_tm_segment[0:4]
                            ten_before_tm_segment += seq[l]

                    seq_dict[current_id][tm_segment_length].append(TM_pred[i + 2] - TM_pred[i + 1])
                    seq_dict[current_id][plus_10_after_TM_charge].append(wagdalena(ten_after_tm_segment))
                    seq_dict[current_id][plus_5_after_TM_charge].append(wagdalena(five_after_tm_segment))
                    seq_dict[current_id][plus_10_after_TM_sequence].append(ten_after_tm_segment)
                    seq_dict[current_id][minus_5_before_TM_charge].append(wagdalena(five_before_tm_segment))
                    seq_dict[current_id][minus_10_before_TM_charge].append(wagdalena(ten_before_tm_segment))

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
    print("charge nette =", wagdalena("ARKGVQLGLV"))
