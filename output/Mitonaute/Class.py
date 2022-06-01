import pandas as pd
import Fastaboy
import TargetP

""" not used but saved as archive for future modifications"""


def class_predictor(seq_dict):
    id_list_class_1 = []
    id_list_class_2 = []
    id_list_class_3 = []

    predictor_list_1 = []
    predictor_list_2 = []

    for current_id in seq_dict.keys():
        predictor_name_1 = []
        predictor_name_2 = []

        seq_dict[current_id]['score'] = 0
        seq_dict[current_id]['class'] = 'Other'
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
            if seq_dict[current_id]['targetp_pred'] != 'MT':
                if tm_pred.count('M') == 1:

                    id_list_class_1.append(current_id)
                    predictor_name_1.append(program_name)
                elif tm_pred.count('M') == 2:

                    id_list_class_2.append(current_id)
                    predictor_name_2.append(program_name)
            else:
                if tm_pred.count('M') > 1:
                    id_list_class_3.append(current_id)
        predictor_list_1 += predictor_name_1
        predictor_list_2 += predictor_name_2

    for current_id in seq_dict.keys():
        bias = []
        bias_results = []
        keys = seq_dict[current_id]

        for key in keys:
            if 'charge_bias' in key:  # we search the charge bias column
                bias.append(key)

        for bias_column in bias:
            bias_results.append(seq_dict[current_id][bias_column])

        if 'c-in bias' in bias_results:
            seq_dict[current_id]['score'] += 0.25
            if bias_results.count('c-in bias') > 1:
                seq_dict[current_id]['score'] += 0.25

        if current_id in id_list_class_1 and current_id not in id_list_class_2:
            seq_dict[current_id]['class'] = 'class 1'
            seq_dict[current_id]['score'] += 0.5

        elif current_id in id_list_class_2 and current_id not in id_list_class_1:
            seq_dict[current_id]['class'] = 'class 2'
            seq_dict[current_id]['score'] += 0.5

        elif current_id in id_list_class_2 and current_id in id_list_class_1:
            seq_dict[current_id]['class'] = 'ambiguous : class 1 and 2'
            seq_dict[current_id]['score'] += 0.25

        elif current_id in id_list_class_3:
            seq_dict[current_id]['class'] = 'class 3'
            seq_dict[current_id]['score'] += 0.5



        """id_list_class_2 = list(dict.fromkeys(id_list_class_2))
            id_list_class_1 = list(dict.fromkeys(id_list_class_1))"""

        """table_values = []
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
        content.to_csv('Class1.csv', sep=";")"""

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
    return seq_dict


if __name__ == "__main__":
    seq_dict = Fastaboy.fasta_reader("Yeast_proteome.txt")

    seq_dict = TargetP.parse_targetp(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\scere_summary.targetp2",
                                     seq_dict)
    # seq_dict = TargetP.parse_targetp(r"D:\Bureau\Cours\M1\pythonProject\Mylib\PTUT\scere_summary.targetp2",
    # seq_dict)
    seq_dict = Fastaboy.csv_parser(seq_dict, r'C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.csv',
                                   sep=";")
    seq_dict = class_predictor(seq_dict)
    print(seq_dict)
