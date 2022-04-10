
import pandas as pd

df = pd.read_csv(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.csv", sep=";")
charge = df["targetp_pred"]
# print(df[(df["DeltaG+HMMTOP_TM_pred"].str.count("M") == 2) | (df["Tmhmm_pred"].str.count("M") == 2)])
inter = df[(df["DeltaG+HMMTOP_TM_pred"].str.count("M") > 3) | (df["Tmhmm_pred"].str.count("M") > 3)]
print(inter[inter["DeltaG+HMMTOP_TM_pred"].str.count("M") % 2 == 0 | (inter["Tmhmm_pred"].str.count("M") % 2 == 0)])


