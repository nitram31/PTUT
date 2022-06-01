import pandas as pd

""" not used but saved as archive for future modifications"""


def chargeparse(df, classe):
    if classe == 1:
        classe = df[df['charge'].astype(int) > 0]  # for class 1
    elif classe == 2:
        classe = df[df['charge'].astype(int) > 1]  # for class 2
    return (classe)


# Filtre sur colonne 2 - targetpred sélectionné se qui n'est pas MT

def nopresequence(df):
    df_nopreseq = df[(df['targetp_pred'].str.contains('SP')) | (df['targetp_pred'].str.contains('OTHER'))]
    return df_nopreseq


# Decompte du nombre de TM

def numberTM(df):

    # first class protein with one TM
    class_1 = df[(df['DeltaG_TM_pred'].str.count('M') == 1)
                 | (df['tmhmm_TM_pred'].str.count('M') == 1)
                 | (df['HMMTOP_TM_pred'].str.count('M') == 1)]
    print(class_1)
    for index, row in class_1.iterrows():
        df.iloc[index]['class'] = 'class 1'
        print(df.iloc[index])
        break
    class_2 = df[(df['DeltaG_TM_pred'].str.count('M') == 2)
                           | (df['tmhmm_TM_pred'].str.count('M') == 2)
                           | (df['HMMTOP_TM_pred'].str.count('M') == 2)]
    for index, row in class_2.iterrows():
        df.iloc[index]['class'] = 'class 2'
    return df


if __name__ == "__main__":
    df = pd.read_excel(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.xlsx")
    df['class'] = 'Other'
    df = numberTM(df)

    """df_nopreseq = nopresequence(df)
    df_TMclass1 = numberTM(df_nopreseq, prot_class=1)
    df_class1 = chargeparse(df_TMclass1, 1)
    df_TMclass2 = numberTM(df_nopreseq, prot_class=2)
    df_class2 = chargeparse(df_TMclass2, 2)
    df_class1.to_csv("classe1.csv", sep=";", index=False)  # export file
    df_class2.to_csv("classe2.csv", sep=";", index=False)  # export file"""
