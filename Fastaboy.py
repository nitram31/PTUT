from Bio import SeqIO
import ast
import ntpath


def fasta_reader(path):
    seq_dict = {}
    with open(path) as file:
        for record in SeqIO.parse(file, "fasta"):
            residue = record.seq
            current_id = record.id
            seq_dict[current_id] = {"seq" : residue}
    return seq_dict

def final_parser(path, seq_dict):
    with open(path) as file:
        cpt = 1
        for line in file:

            if cpt == 1:
                current_id = line.split("\n")[0]

            elif cpt == 2:
                seq_dict[str(current_id)]["DeltaG+HMMTOP_TM_pred"] = ast.literal_eval(line.split("\n")[0])

            elif cpt == 3:
                if line[0] == "[":
                    seq_dict[current_id]['deltaG_pred_score'] = ast.literal_eval(line.split("\n")[0])
                else:
                    seq_dict[current_id]['deltaG_pred_score'] = line.split("\n")[0]

            elif cpt == 4:
                pass

            else:
                seq_dict[str(current_id)]["tmhmm_pred"] = ast.literal_eval(line.split("\n")[0])
                cpt = 0

            cpt += 1
    return seq_dict

