import pandas as pd

"""
panda doc : https://pandas.pydata.org/docs/user_guide/merging.html#merging-join

def creertable(nosprot, locprot):
    for lineLoc in locprot:
        for lineNosProt in nosprot:
            if lineLoc[2] != lineNosProt[1]:
                locprot = locprot.drop(locprot[lineLoc])
    return(locprot)

def creertable(nosprot, locprot):
    res = pd.merge(locprot, nosprot, on ="UniProt_ID")
    return(res)
def creertable(nosprot, locprot):
    dataframe = [nosprot, locprot]
    res = pd.concat(dataframe, join="inner", keys="UniProt_ID")
    return (res)    
"""

def creertable(nosprot, locprot):
    res = pd.merge(locprot, nosprot, how="inner", on="Uniprot_ID")
    return(res)


if __name__ == "__main__":
    nosprot = pd.read_csv("sequences3.csv", sep=";")
    locprot = pd.read_csv("localisation_S2.csv", sep=";")

    nosprot.columns = nosprot.columns.str.strip()
    locprot.columns = locprot.columns.str.strip()

    print("nosprot : ", nosprot.columns)
    print("locprot : ", locprot.columns)
    creertable(nosprot, locprot).to_csv("tab_localizations.csv", sep=";", index=False) #export file