import pandas as pd

"""
panda doc : https://pandas.pydata.org/docs/user_guide/merging.html#merging-join

def creertable(nosprot, locprot):
    for lineLoc in locprot:
        for lineNosProt in nosprot:
            if lineLoc["Uniprot ID"] != lineNosProt["Uniprot ID"]:
                lineLoc["Uniprot ID"].pop
    return(locprot)
"""
def creertable(nosprot, locprot):
    res = pd.merge(locprot, nosprot, how="inner",on = "Uniprot ID", right_on=True)
    return(res)



if __name__ == "__main__":
    nosprot = pd.read_excel("sequences3.xlsx")
    nosprot.to_csv("sequences3.csv", sep=';', index=False)
    locprot = pd.read_excel("localisation_S2.xlsx")
    locprot.to_csv("localisation_S2.csv", sep=';', index=False)

    creertable(nosprot, locprot).to_csv("tab_localizations.csv", sep="\t", index=False) #export file