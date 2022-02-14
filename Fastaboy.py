from Bio import SeqIO

import ntpath


def fasta_reader(path):
    seq_dict = {}
    with open(path) as file:
        for record in SeqIO.parse(file, "fasta"):
            residue = record.seq
            current_id = record.id
            seq_dict[current_id] = {"seq" : residue}
    return seq_dict



