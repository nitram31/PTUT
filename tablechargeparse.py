import pandas as pd

df = pd.read_excel("results_full.xlsx")
df_csv = df.to_csv(index=False)

# returns rows with charge discard
def chargeparse(df, classe):
    if classe == "classe1":
        classe = df[df['charge'].astype(int) > 0 ]
    elif classe == "classe2":
        classe = df[df['charge'].astype(int) > 1 ]
    return (classe)


print(chargeparse(df, "classe2"))
