import pandas as pd 

# Input : fichier 
df = pd.read_excel("results_full.xlsx")
df_csv = df.to_csv(index=False)


# Filtre sur colonne 2 - targetpred sélectionné se qui n'est pas MT

def nopreseq(dataframe = df): 
    nopreseq = df[df['targetp_pred'].str.contains('SP') | df['targetp_pred'].str.contains('OTHER')]
    return(nopreseq)

# Decompte du nombre de TM

def numberTM(dataframe = df): 
    # first class protein with one TM
    numberTM_1 =  df[(df['TMsegment_pred'].str.count('M')==1) | (df['Tmhmm_pred'].str.count('M')==1)]

    return(numberTM)

if __name__ == "__main__":
    print(numberTM(df))
    print(nopreseq(df))