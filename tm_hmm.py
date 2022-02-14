import tmhmm
import Fastaboy


def tmhmm_read(fasta_file):
    seq_dict = Fastaboy.fasta_reader(fasta_file)
    for current_id in seq_dict.keys():
        annotation= tmhmm.predict(seq_dict[current_id]['seq'], compute_posterior=False)
        seq_dict[current_id]["tmhmm_pred"] = annotation
    print(seq_dict)

tmhmm_read(r"D:\Bureau\Cours\M1\S8\Projet_Tut\UP000002311_559292.fasta")


