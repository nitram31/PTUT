from Bio import SeqIO


def fasta_reader(path):
    with open(path) as file:
        Seq_dict = SeqIO.to_dict(SeqIO.parse(file, "fasta"))
        return Seq_dict



