import pandas as pd

df = pd.read_excel("results_full.xlsx")
df_csv = df.to_csv(index=False)


# Filter on  column 2 - targetpred selection which is not MT
def nopreseq(dataframe = df):
    nopreseq = df[df['targetp_pred'].str.contains('SP') | df['targetp_pred'].str.contains('OTHER')]
    return(nopreseq)

def chargeparse(df, classe):
    if classe == "classe1":
        classe = df[df['charge'].astype(int) > 0 ]
    elif classe == "classe2":
        classe = df[df['charge'].astype(int) > 1 ]
    return (classe)


print(chargeparse(df, "classe2"))