import pandas as pd

# Filter on  column 2 - targetpred selection which is not MT
def nopreseq(df):
    nopreseq = df[df['targetp_pred'].str.contains('SP') | df['targetp_pred'].str.contains('OTHER')]
    return(nopreseq)

# function for charge discard
def chargeparse(df, classe):
    if classe == "classe1":
        classe = df[df['charge'].astype(int) > 0 ] #for class 1
    elif classe == "classe2":
        classe = df[df['charge'].astype(int) > 1 ] #for class 2
    return (classe)

# number of TM
def numberTM(df):
    # second class protein with one TM
    numberTM = df[(df['DeltaG+HMMTOP_TM_pred'].str.count('M') == 2) | (df['Tmhmm_pred'].str.count('M') == 2)]
    return (numberTM)


if __name__ == "__main__":
    df = pd.read_excel("results_full.xlsx")

    df = chargeparse(df, "classe2")
    df = nopreseq(df)
    df = numberTM(df)

    df.to_csv("classe2.csv", sep="\t", index=False) #export file

