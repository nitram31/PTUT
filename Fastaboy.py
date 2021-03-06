from Bio import SeqIO
import ast
import pandas as pd

"""getting fasta sequences and protein names"""
def fasta_reader(path):
    seq_dict = {}
    with open(path) as file:
        for record in SeqIO.parse(file, "fasta"): #Biopython module functionnality
            residue = record.seq
            current_id = record.id
            seq_dict[current_id] = {"seq": residue}
    return seq_dict

def csv_parser(seq_dict, path, sep=";"):
    df = pd.read_csv(path, sep=sep)
    for line in range(0, len(df)):
        seq_dict[df.iloc[line, 1]]["targetp_pred"] = df.iloc[line, 2]
        seq_dict[df.iloc[line, 1]]["targetp_pred_score"] = df.iloc[line, 3]

        if df.iloc[line, 4] != "No tm":
            seq_dict[df.iloc[line, 1]]["tmhmm_TM_pred"] = ast.literal_eval(df.iloc[line, 4])
        else:
            seq_dict[df.iloc[line, 1]]["tmhmm_TM_pred"] = df.iloc[line, 4]

        if df.iloc[line, 5] != "No tm":
            seq_dict[df.iloc[line, 1]]["HMMTOP_TM_pred"] = ast.literal_eval(df.iloc[line, 5])
        else:
            seq_dict[df.iloc[line, 1]]["HMMTOP_TM_pred"] = df.iloc[line, 5]

        if df.iloc[line, 6] != "No tm":
            seq_dict[df.iloc[line, 1]]["DeltaG_TM_pred"] = ast.literal_eval(df.iloc[line, 6])
        else:
            seq_dict[df.iloc[line, 1]]["DeltaG_TM_pred"] = df.iloc[line, 6]

        if df.iloc[line, 7] != "No tm":
            seq_dict[df.iloc[line, 1]]["deltaG_pred_score"] = ast.literal_eval(df.iloc[line, 7])
        else:
            seq_dict[df.iloc[line, 1]]["deltaG_pred_score"] = df.iloc[line, 7]


    return seq_dict


if __name__ == "__main__":
    df = csv_parser(r"C:\Users\Martin\PycharmProjects\pythonProject\Mylib\PTUT\output.csv", sep=";")
