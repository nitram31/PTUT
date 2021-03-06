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
            if 'TM_pred' in key:  # condition that we need a transmembrane segment present to continue and costruct the key
                TM_results.append(key)

        for software_TM_pred in TM_results:  # software can be TMHMM, HMMTOP or deltaG
            program_name = ""

            TM_pred = seq_dict[current_id][software_TM_pred]  # deltaG, TMHMM and HMMTOP treated simultanously
            j = 0
            while software_TM_pred[j] != '_':
                program_name += software_TM_pred[j]
                j += 1

            # initialization of charge variables for each software
            plus_10_after_TM_charge = program_name + '_10_aa_C_ter_side_of_TM_charge'
            plus_10_after_TM_sequence = program_name + '_10_aa_C_ter_side_of_TM_sequence'
            plus_5_after_TM_charge = program_name + '_5_aa_C_ter_side_of_TM_charge'
            minus_10_before_TM_charge = program_name + '_10_aa_N_ter_side_of_TM_charge'
            minus_5_before_TM_charge = program_name + '_5_aa_N_ter_side_of_TM_charge'
            tm_segment_length = program_name + '_TM_segment_length'

            # initialization of dictionnary with empty lists
            seq_dict[current_id][tm_segment_length] = []
            seq_dict[current_id][plus_10_after_TM_charge] = []
            seq_dict[current_id][plus_5_after_TM_charge] = []
            seq_dict[current_id][plus_10_after_TM_sequence] = []
            seq_dict[current_id][minus_5_before_TM_charge] = []
            seq_dict[current_id][minus_10_before_TM_charge] = []

            for i in range(0, len(TM_pred), 3):  # iterate on the length of the pos_list, to select the letter
                # the iteration is made on every part of the molecule (inside, membrane, outside)
                if TM_pred[i] == 'M':
                    # initialization
                    ten_after_tm_segment = ""
                    five_after_tm_segment = ""
                    five_before_tm_segment = ""
                    ten_before_tm_segment = ""

                    try:
                        for l in range(TM_pred[i + 2] - 1, TM_pred[i + 2] + 9):
                            """
                            [i + 2] : is the last aminoacid of TM segment
                            TM_pred[i + 2] - 1 : is the first aminoacid of TM segment
                            TM_pred[i + 2] + 9 : we calculate charge on the last aminoacid of TM +9 aminoacids after TM segment
                            """
                            ten_after_tm_segment += seq[l]
                            five_after_tm_segment = ten_after_tm_segment[0:4]
                            # first 5 aminoacids after TM segment
                    except IndexError:
                        ten_after_tm_segment = ""
                        five_after_tm_segment = ""
                        for l in range(TM_pred[i + 2] - 1, len(TM_pred)):
                            """we make this calculation if the sequence between two TM is smaller then 10 aminoacids"""
                            ten_after_tm_segment += seq[l]
                            five_after_tm_segment = ten_after_tm_segment[0:4]

                    try:
                        for l in range(TM_pred[i - 1] - 9, TM_pred[i + 1]):

                            if l > 0:
                                ten_before_tm_segment += seq[l]
                                five_before_tm_segment = ten_before_tm_segment[0:4]

                            else:
                                raise IndexError

                    except IndexError:
                        five_before_tm_segment = ""
                        ten_before_tm_segment = ""
                        for l in range(0, TM_pred[i + 1]):
                            """we make this calculation if the sequence between two TM is smaller then 10 aminoacids"""
                            ten_before_tm_segment += seq[l]
                            five_before_tm_segment = ten_before_tm_segment[0:4]

                    # results are saved in main dictionnary with corresponding column name
                    # and the charge is calculated on selected part of the sequence

                    seq_dict[current_id][tm_segment_length].append(TM_pred[i + 2] - TM_pred[i + 1])
                    seq_dict[current_id][plus_10_after_TM_charge].append(wagdalena(ten_after_tm_segment))
                    seq_dict[current_id][plus_5_after_TM_charge].append(wagdalena(five_after_tm_segment))
                    seq_dict[current_id][plus_10_after_TM_sequence].append(ten_after_tm_segment)
                    seq_dict[current_id][minus_5_before_TM_charge].append(wagdalena(five_before_tm_segment))
                    seq_dict[current_id][minus_10_before_TM_charge].append(wagdalena(ten_before_tm_segment))
            seq_dict[current_id][program_name + ' charge_bias'] = \
                charge_bias(seq_dict, current_id, program_name)

    return seq_dict


def charge_sort(seq_dict):
    """Takes a dictionary and discard proteins based on the predicted charge"""
    temp_dict = {}
    for current_id in seq_dict.keys():
        if seq_dict[current_id]['charge'] == 2 or seq_dict[current_id]['charge'] == 3:
            temp_dict[current_id] = seq_dict[current_id]
    seq_dict = temp_dict
    return seq_dict


def charge_bias(seq_dict, seq_id, program):
    best_minus_charge = 0
    best_plus_charge = 0
    if seq_dict[seq_id][program + '_TM_pred'].count('M') == 1:
        best_minus_charge = max(
            seq_dict[seq_id][program + '_10_aa_N_ter_side_of_TM_charge'],
            seq_dict[seq_id][program + '_5_aa_N_ter_side_of_TM_charge'])
        best_plus_charge = max(
            seq_dict[seq_id][program + '_10_aa_C_ter_side_of_TM_charge'],
            seq_dict[seq_id][program + '_5_aa_C_ter_side_of_TM_charge'])

    elif seq_dict[seq_id][program + '_TM_pred'].count('M') == 2:

        best_minus_charge = \
            max(seq_dict[seq_id][program + '_10_aa_N_ter_side_of_TM_charge'][0],
                seq_dict[seq_id][program + '_5_aa_N_ter_side_of_TM_charge'][0]) \
            + max(
                seq_dict[seq_id][program + '_10_aa_C_ter_side_of_TM_charge'][1],
                seq_dict[seq_id][program + '_5_aa_N_ter_side_of_TM_charge'][1])

        best_plus_charge = \
            max([seq_dict[seq_id][program + '_10_aa_N_ter_side_of_TM_charge'][1],
                 seq_dict[seq_id][program + '_5_aa_N_ter_side_of_TM_charge'][1]]) \
            + max(
                [seq_dict[seq_id][program + '_10_aa_C_ter_side_of_TM_charge'][0],
                 seq_dict[seq_id][program + '_5_aa_N_ter_side_of_TM_charge'][0]])
    if best_plus_charge == best_minus_charge:
        return 'neutral'
    elif best_plus_charge > best_minus_charge:
        return "c-in bias"
    else:
        return "n-in bias"


if __name__ == "__main__":
    print("charge nette =", wagdalena("MVLP"))
