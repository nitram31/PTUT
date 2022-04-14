def class_predictor(seq_dict):
    cpt = 0
    for current_id in seq_dict.keys():

        if seq_dict[current_id]['tmhmm_TM_pred'].count('M') == 2 \
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
                pass
    return class_1, class_2, class_3
