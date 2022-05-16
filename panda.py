import pandas as pd 
""" not used but saved as archive for future modifications"""

def chargeparse1(df):
    if df[df['charge'].astype(int) > 0 ]: #for class 1
        return True

def chargeparse2(df):
    if df[df['charge'].astype(int) > 1 ]: #for class 2
        return True


# Filtre sur colonne 2 - targetpred sélectionné se qui n'est pas MT

def nopresequence(df):
    if df[(df['targetp_pred'].str.contains('OTHER'))]:
        return True

# Decompte du nombre de TM

def number1TM(df):
    # first class protein with one TM
    if df[(df['DeltaG+HMMTOP_TM_pred'].str.count('M') == 1) | (df['Tmhmm_pred'].str.count('M') == 1)]:
        return True

def number2TM(df):
    if df[(df['DeltaG+HMMTOP_TM_pred'].str.count('M') == 2) | (df['Tmhmm_pred'].str.count('M') == 2)]:
        return False

if __name__ == "__main__":
    df = pd.read_excel(r"output.csv")
    classe = []
    if chargeparse1()
    df["class"] = classe