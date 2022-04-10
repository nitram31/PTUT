import pandas as pd


def creertable(path):
    prot = pd.read_csv(path, sep=";")
    prot.columns = prot.columns.str.strip()
    col_name = ["Mitochondrial outer membrane [GO:0005741]", "Mitochondrial intermembrane space [GO:0005758]",
                "Mitochondrial inner membrane [GO:0005743]",
                "Mitochondrial matrix [GO:0005759]", "Cytosol [GO:0005829]", "ER & Golgi [GO:0005783] [GO:0005794]",
                "Plasma membrane [GO:0005886]",
                "Vacuole [GO:0005773]", "Peroxisome [GO:0005777]"]
    res = []
    resDict = {}
    for line in range(0, len(prot)):
        prot_id = prot.iloc[line, 1]
        resDict[prot_id] = []
        for column in range(3, 12):

            if str(prot.iloc[line, column]) == "1.0":
                # print(col_name[column-3])
                # print(line, column)
                res.append([prot_id, col_name[column - 3]])
                resDict[prot_id].append(col_name[column - 3])

                # prot.iloc[line, -1] = col_name[column]
    return resDict


if __name__ == "__main__":
    prot = pd.read_csv("tab_localizations_copy.csv", sep=";")

    # creertable(prot).to_csv("tab_localizations02.csv", sep=";", index=False)  # export file
    print(creertable(prot))
