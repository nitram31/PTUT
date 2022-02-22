import pyTMHMM as tm
import biolib


def str_to_pos(annotation):
    """reformat the annotation output from pytmhmm to a list by counting the number of letters in the string and
    recording it as [letter_corresponding_to_subcellular_localisation, first_position, last_position]"""
    last_pos = annotation[0]
    pos_list = []
    pos_list.append(last_pos)
    pos_list.append(1)

    for i in range(1, len(annotation)):
        current_pos = annotation[i]

        if last_pos != current_pos:
            pos_list.append(i)  # add last position to the list to record the end of segment
            pos_list.append(current_pos)
            pos_list.append(i + 1)

        if i + 1 == len(annotation):
            pos_list.append(i + 1)
        last_pos = current_pos
    return pos_list


def tmhmm_read(seq_dict):
    """takes a sequence dictionnary and adds the pytmhmm prediction"""

    for current_id in seq_dict.keys():
        annotation = tm.predict(seq_dict[current_id]['seq'], compute_posterior=False)
        if current_id == 'sp|P32839|BCS1_YEAST':
            print(annotation)
        pos_list = str_to_pos(annotation)  # reformat the raw results to a better form
        seq_dict[current_id]['TMsegment_pred'] = pos_list

    return seq_dict


def reformat_result(pos_list):
    annotation = ""
    for i in range(0, len(pos_list), 3):
        annotation += str(pos_list[i + 1]) \
                      + "-" \
                      + str(pos_list[i + 2]) \
                      + " : "
        if pos_list[i] == 'i':
            annotation += "inside "
        elif pos_list[i] == 'M':
            annotation += "transmembrane helix "
        else:
            annotation += "outside "


def sort_dict(seq_dict):
    temp_seq_dict = {}
    for current_id in seq_dict.keys():
        try:
            if seq_dict[current_id]['targetp_pred'][0] != 'MT' and seq_dict[current_id]['TMsegment_pred'].count(
                    'M') == 1:
                temp_seq_dict[current_id] = seq_dict[current_id]
            '''if seq_dict[current_id]['targetp_pred'][0] == 'MT' and seq_dict[current_id]['TMsegment_pred'].count('M') >= 2:
                temp_seq_dict[current_id] = seq_dict[current_id]'''
        except:
            print("protein does not exist : ", current_id)

    seq_dict = temp_seq_dict
    return seq_dict


def orientation_sort(seq_dict):
    temp_dict = {}
    for current_id in seq_dict.keys():
        if seq_dict[current_id]['TMsegment_pred'][0] == 'O':
            temp_dict[current_id] = seq_dict[current_id]

    seq_dict = temp_dict
    return seq_dict
