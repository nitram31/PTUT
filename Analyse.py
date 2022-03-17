<<<<<<< HEAD
import pandas as pd

df = pd.read_csv(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.csv", sep=";")
charge = df["targetp_pred"]
# print(df[(df["TMsegment_pred"].str.count("M") == 2) | (df["Tmhmm_pred"].str.count("M") == 2)])
inter = df[(df["TMsegment_pred"].str.count("M") > 3) | (df["Tmhmm_pred"].str.count("M") > 3)]
print(inter[inter["TMsegment_pred"].str.count("M") % 2 == 0 | (inter["Tmhmm_pred"].str.count("M") % 2 == 0)])
=======
import pandas as pd

df = pd.read_csv(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.csv", sep=";")
charge = df["targetp_pred"]
# print(df[(df["TMsegment_pred"].str.count("M") == 2) | (df["Tmhmm_pred"].str.count("M") == 2)])
inter = df[(df["TMsegment_pred"].str.count("M") > 3) | (df["Tmhmm_pred"].str.count("M") > 3)]
print(inter[inter["TMsegment_pred"].str.count("M") % 2 == 0 | (inter["Tmhmm_pred"].str.count("M") % 2 == 0)])
>>>>>>> 6a34a981f7b8455fc4ed8f75400a4f5d49269aaf
