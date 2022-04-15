import pandas as pd

def presequence(df):
    # looking for protein with a predicted presequence
    df_preseq = df[df['targetp_pred'].str.contains('MT')]
    return df_preseq

def numberTM(df): 
    # looking for third class protein with more than 2 TM segments
    df_class3 = df[(df['tmhmm_TM_pred'].str.count('M')>=2) | (df['DeltaG_TM_pred'].str.count('M')>=2) | (df['HMMTOP_TM_pred'].str.count('M')>=2)]
    return df_class3

if __name__ == "__main__":
    df = pd.read_csv('output.csv', sep=';') # read fichier input, containing yeast mitochondria preteome
    
    df_presequence = presequence(df) # apply first fonction => filter on tragetP_pred => only protein with 'MT' (== presequence)
    df_presequence.to_csv("preseq_prot.csv", sep=';', index=False) # export file of protein WITH a presequence only
    
    df_class3 = numberTM(df_presequence) # apply second fonction => filter on # of TM (at least 2)
    
    df_class3.to_csv("classe3.csv", sep=";", index=False)  # export file protein with a presequence AND at least 2TM. 

