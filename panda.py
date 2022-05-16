import pandas as pd
import ast

def chargeparse1(df):
    try:
        df[1]['tmhmm_plus_10_after_TM_charge'] = ast.literal_eval(df[1]['tmhmm_plus_10_after_TM_charge'])[0]
        df[1]['tmhmm_plus_5_after_TM_charge'] = ast.literal_eval(df[1]['tmhmm_plus_5_after_TM_charge'])[0]
        df[1]['DeltaG_plus_10_after_TM_charge'] = ast.literal_eval(df[1]['DeltaG_plus_10_after_TM_charge'])[0]
        df[1]['DeltaG_plus_5_after_TM_charge'] = ast.literal_eval(df[1]['DeltaG_plus_5_after_TM_charge'])[0]

        if df[1]['tmhmm_plus_10_after_TM_charge'] > 0 | df[1]['tmhmm_plus_5_after_TM_charge'] > 0 |\
                df[1]['DeltaG_plus_10_after_TM_charge'] > 0 | df[1]['DeltaG_plus_5_after_TM_charge'] > 0 : #for class 1
            return True
        else:
            return False
    except IndexError:
        print("Index error")

def chargeparse2(df):
    try:
        df[1]['tmhmm_plus_10_after_TM_charge'] = ast.literal_eval(df[1]['tmhmm_plus_10_after_TM_charge'])[0]
        df[1]['tmhmm_plus_5_after_TM_charge'] = ast.literal_eval(df[1]['tmhmm_plus_5_after_TM_charge'])[0]
        df[1]['DeltaG_plus_10_after_TM_charge'] = ast.literal_eval(df[1]['DeltaG_plus_10_after_TM_charge'])[0]
        df[1]['DeltaG_plus_5_after_TM_charge'] = ast.literal_eval(df[1]['DeltaG_plus_5_after_TM_charge'])[0]

        if df[1]['tmhmm_plus_10_after_TM_charge'] > 1 | df[1]['tmhmm_plus_5_after_TM_charge'] > 1 | \
                df[1]['DeltaG_plus_10_after_TM_charge'] > 1 | df[1]['DeltaG_plus_5_after_TM_charge'] > 1:  # for class 1
            return True
        else:
            return False
    except IndexError:
        print("Index error")

# Decompte du nombre de TM

def number1TM(df):
    # first class protein with one TM
    if df[1]['DeltaG_TM_pred'].count('M') == 1 | df[1]['DeltaG_TM_pred'].count('M') == 1:
        return True
    else:
        return False

def number2TM(df):
    if df[1]['DeltaG_TM_pred'].count('M') == 2 | df[1]['tmhmm_TM_pred'].count('M') == 2:
        return True
    else:
        return False

def numberplus2TM(df):
    if df[1]['DeltaG_TM_pred'].count('M') >= 2 | df[1]['tmhmm_TM_pred'].count('M') >= 2:
        return True
    else:
        return False

# Filtre sur colonne 2 - targetpred sélectionné se qui n'est pas MT

def nopresequence(df):
    #if df['targetp_pred'].contains('OTHER'):
    if 'OTHER' in df[1]['targetp_pred']:
        return True
    else:
        return False

if __name__ == "__main__":
    df = pd.read_excel(r"/Users/magdalenaszczuka/Desktop/PycharmProjects/PTUT/PTUT/output.xlsx")
    classe = []
    score = []
    for row in df.iterrows():
        #print (row)
        if number1TM(row) and nopresequence(row):
            classe.append("class 1")
            score.append("good")
            if chargeparse1(row):
                score.pop(-1)
                score.append("great")

        elif nopresequence(row) and number2TM(row):
            classe.append("class 2")
            score.append("good")
            if chargeparse2(row):
                score.pop(-1)
                score.append("great")

        elif numberplus2TM(row) and not nopresequence(row):
            classe.append("class 3")
            score.append("good")

        else:
            classe.append("class not identified")
            score.append("null")

    df["class"] = classe
    df["score"] = score
    df.to_csv('classificationMagdalicious.csv', sep=";")
    print("fin")