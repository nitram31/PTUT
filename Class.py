import pandas as pd
""" not used but saved as archive for future modifications"""

def class_predictor(seq_dict):
    id_list_class_1 = []
    id_list_class_2 = []
    for current_id in seq_dict.keys():
        keys = seq_dict[current_id]
        tm_results = []
        for key in keys:
            if 'TM_pred' in key:
                tm_results.append(key)

        for software_TM_pred in tm_results:
            program_name = ""

            tm_pred = seq_dict[current_id][software_TM_pred]
            j = 0
            while software_TM_pred[j] != '_':
                program_name += software_TM_pred[j]
                j += 1

            if tm_pred.count('M') == 1:
                try:
                    if seq_dict[current_id][program_name + '_plus_10_after_TM_charge'][0] > 0:
                        if seq_dict[current_id]['targetp_pred'] != 'MT':
                            id_list_class_1.append(current_id)
                except IndexError:
                    pass

            if tm_pred.count('M') == 2:
                try:
                    if seq_dict[current_id][program_name + '_plus_10_after_TM_charge'][0] > 0:
                        if seq_dict[current_id]['targetp_pred'] != 'MT':
                            id_list_class_2.append(current_id)
                except IndexError:
                    pass

    id_list_class_2 = list(dict.fromkeys(id_list_class_2))
    id_list_class_1 = list(dict.fromkeys(id_list_class_1))

    table_values = []
    col_names = []

    first_prot = list(seq_dict.keys())[0]
    for col in seq_dict[first_prot]:
        col_names.append(col)
    col_names[0] = 'name'

    for key in id_list_class_1:
        line = []
        key_list = [key]
        for variable_names in seq_dict[key]:
            if variable_names != 'seq':
                key_list.append(seq_dict[key][variable_names])
        line.append(key_list)
        table_values += line
    content = pd.DataFrame(table_values, columns=col_names)
    content.to_csv('Class1.csv', sep=";")

    for key in id_list_class_2:
        line = []
        key_list = [key]
        for variable_names in seq_dict[key]:
            if variable_names != 'seq':
                key_list.append(seq_dict[key][variable_names])
        line.append(key_list)
        table_values += line
    content = pd.DataFrame(table_values, columns=col_names)
    content.to_csv('Class2.csv', sep=";")














    """if seq_dict[current_id]['tmhmm_TM_pred'].count('M') == 2 \
    or seq_dict[current_id]['HMMTOP_TM_pred'].count('M') == 2 \
    or seq_dict[current_id]['DeltaG_TM_pred'].count('M') == 2:
        try:

            if seq_dict[current_id]['tmhmm_plus_10_after_TM_charge'][0] > 0 \
            or seq_dict[current_id]['HMMTOP_plus_10_after_TM_charge'][0] > 0 \
            or  seq_dict[current_id]['DeltaG_plus_10_after_TM_charge'][0] > 0:
                if seq_dict[current_id]['targetp_pred'] != 'MT':
                    cpt += 1
                    print(cpt)
        except IndexError:
            pass"""

